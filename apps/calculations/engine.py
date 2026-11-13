"""
Graph calculation engine.
Walks the decision model DAG in topological order and executes methods.
"""
from __future__ import annotations

import logging
from collections import defaultdict, deque
from typing import Any
from uuid import UUID

from apps.decision_models.schemas import DecisionModelSchema, Node, NodeType
from apps.methods.base import MethodInput, MethodResult
from apps.methods.services import ensure_methods_loaded, run_method

logger = logging.getLogger(__name__)


class EngineError(Exception):
    def __init__(self, message: str, node_id: str | None = None):
        super().__init__(message)
        self.node_id = node_id


def _topo_sort(schema: DecisionModelSchema) -> list[UUID]:
    """Kahn topological sort. Raises EngineError on cycle."""
    graph: dict[UUID, list[UUID]] = defaultdict(list)
    in_degree: dict[UUID, int] = {n.id: 0 for n in schema.nodes}

    for edge in schema.edges:
        graph[edge.source].append(edge.target)
        in_degree[edge.target] = in_degree.get(edge.target, 0) + 1
        if edge.source not in in_degree:
            in_degree[edge.source] = 0

    queue = deque([nid for nid, deg in in_degree.items() if deg == 0])
    order: list[UUID] = []

    while queue:
        current = queue.popleft()
        order.append(current)
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) != len(in_degree):
        raise EngineError("Decision model graph contains a cycle")

    return order


def _node_map(schema: DecisionModelSchema) -> dict[UUID, Node]:
    return {n.id: n for n in schema.nodes}


def _incoming_edges(schema: DecisionModelSchema, node_id: UUID):
    return [e for e in schema.edges if e.target == node_id]


def _collect_inputs(
    node: Node,
    schema: DecisionModelSchema,
    node_results: dict[UUID, dict[str, Any]],
) -> dict[str, Any]:
    """
    Gather data from upstream nodes based on connected ports.
    Returns a dict that can feed MethodInput.
    """
    collected: dict[str, Any] = {
        "matrix": None,
        "criteria_types": None,
        "weights": None,
        "preference": None,
        "ranking": None,
        "extras": {},
    }

    # Start with node's own data (e.g. matrix block stores matrix in data)
    data = node.data or {}
    if "matrix" in data:
        collected["matrix"] = data["matrix"]
    if "criteria_types" in data:
        collected["criteria_types"] = data["criteria_types"]
    if "weights" in data:
        collected["weights"] = data["weights"]
    if "n_alternatives" in data:
        collected["extras"]["n_alternatives"] = data["n_alternatives"]
    if "n_criteria" in data:
        collected["extras"]["n_criteria"] = data["n_criteria"]

    # Overlay data coming from connected parents
    for edge in _incoming_edges(schema, node.id):
        parent_out = node_results.get(edge.source, {})
        port = edge.source_port

        # Map common port names / data produced by parent
        if "matrix" in (port or "") or parent_out.get("matrix") is not None:
            if collected["matrix"] is None and parent_out.get("matrix") is not None:
                collected["matrix"] = parent_out["matrix"]
            if collected["criteria_types"] is None and parent_out.get("criteria_types") is not None:
                collected["criteria_types"] = parent_out["criteria_types"]

        if "weight" in (port or "").lower() or parent_out.get("weights") is not None:
            if collected["weights"] is None and parent_out.get("weights") is not None:
                collected["weights"] = parent_out["weights"]

        if "preference" in (port or "").lower() or parent_out.get("preference") is not None:
            if parent_out.get("preference") is not None:
                collected["preference"] = parent_out["preference"]
                collected["extras"]["preference"] = parent_out["preference"]

        if "ranking" in (port or "").lower() or parent_out.get("ranking") is not None:
            if parent_out.get("ranking") is not None:
                collected["ranking"] = parent_out["ranking"]
                # For correlation – collect multiple rankings
                rankings = collected["extras"].setdefault("rankings", [])
                rankings.append(
                    {
                        "node_id": str(edge.source),
                        "ranking": parent_out["ranking"],
                        "preference": parent_out.get("preference"),
                    }
                )

        # Pass through mcda config for sensitivity blocks
        if node.type == NodeType.SENSITIVITY:
            parent_node = _node_map(schema).get(edge.source)
            if parent_node and parent_node.type == NodeType.MCDA:
                collected["extras"]["mcda_method"] = parent_node.method
                collected["extras"]["mcda_extension"] = parent_node.extension.value

    return collected


def _execute_node(
    node: Node,
    inputs: dict[str, Any],
) -> dict[str, Any]:
    """
    Execute a single node and return a result dict stored in node_results.
    """
    out: dict[str, Any] = {
        "node_id": str(node.id),
        "numeric_id": node.numeric_id,
        "type": node.type.value,
        "method": node.method,
        "extension": node.extension.value,
        "label": node.label,
    }

    # Matrix / input blocks – just expose their data
    if node.type in {NodeType.MATRIX, NodeType.INPUT}:
        out["matrix"] = inputs.get("matrix") or (node.data or {}).get("matrix")
        out["criteria_types"] = inputs.get("criteria_types") or (node.data or {}).get(
            "criteria_types"
        )
        out["weights"] = inputs.get("weights") or (node.data or {}).get("weights")
        out["success"] = True
        return out

    # Visualization – no computation, pass through
    if node.type == NodeType.VISUALIZATION:
        out["success"] = True
        out["passthrough"] = {
            k: inputs.get(k)
            for k in ("preference", "ranking", "weights", "matrix")
            if inputs.get(k) is not None
        }
        return out

    # Methods that need the factory
    method_name = node.method
    if not method_name:
        # Ranking without explicit method → default
        if node.type == NodeType.RANKING:
            method_name = "RANK_DESC"
        else:
            out["success"] = False
            out["error"] = f"Node {node.label or node.id} has no method set"
            return out

    extras = dict(inputs.get("extras") or {})
    if inputs.get("preference") is not None:
        extras["preference"] = inputs["preference"]

    result: MethodResult = run_method(
        name=method_name,
        extension=node.extension.value,
        matrix=inputs.get("matrix"),
        criteria_types=inputs.get("criteria_types"),
        weights=inputs.get("weights"),
        params=node.params or {},
        extras=extras,
    )

    out["success"] = result.success
    out["error"] = result.error
    out["preference"] = result.preference
    out["ranking"] = result.ranking
    out["weights"] = result.weights
    out["correlation"] = result.correlation
    out["sensitivity"] = result.sensitivity
    out["extras"] = result.extras
    return out


def run_decision_model(schema_dict: dict[str, Any]) -> dict[str, Any]:
    """
    Main entry point.
    Returns:
    {
      "success": bool,
      "nodes": [ { node_id, type, method, preference, ranking, ... }, ... ],
      "order": [node_id, ...],
      "error": str | None
    }
    """
    ensure_methods_loaded()

    try:
        schema = DecisionModelSchema.model_validate(schema_dict)
    except Exception as exc:
        return {"success": False, "nodes": [], "order": [], "error": f"Invalid schema: {exc}"}

    try:
        order = _topo_sort(schema)
    except EngineError as exc:
        return {"success": False, "nodes": [], "order": [], "error": str(exc)}

    nodes = _node_map(schema)
    node_results: dict[UUID, dict[str, Any]] = {}
    all_success = True

    for node_id in order:
        node = nodes[node_id]
        try:
            inputs = _collect_inputs(node, schema, node_results)
            result = _execute_node(node, inputs)
        except Exception as exc:
            logger.exception("Node %s failed", node_id)
            result = {
                "node_id": str(node_id),
                "type": node.type.value,
                "method": node.method,
                "success": False,
                "error": str(exc),
            }
        node_results[node_id] = result
        if not result.get("success", False):
            all_success = False

    return {
        "success": all_success,
        "nodes": [node_results[nid] for nid in order],
        "order": [str(nid) for nid in order],
        "error": None if all_success else "One or more nodes failed",
    }
