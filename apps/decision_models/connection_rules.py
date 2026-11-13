"""
Connection rules and graph validation for Decision Model schemas.
"""
from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Iterable
from uuid import UUID

from .schemas import (
    DataType,
    DecisionModelSchema,
    Extension,
    Node,
    NodeType,
)


# ===== Allowed data_type flow =====
# source_data_type → set of accepted target data_types

ALLOWED_DATA_TYPE_FLOW: dict[DataType, set[DataType]] = {
    DataType.MATRIX: {
        DataType.MATRIX,
        DataType.ANY,
    },
    DataType.CRITERIA_TYPES: {
        DataType.CRITERIA_TYPES,
        DataType.ANY,
    },
    DataType.WEIGHTS: {
        DataType.WEIGHTS,
        DataType.ANY,
    },
    DataType.PREFERENCE: {
        DataType.PREFERENCE,
        DataType.ANY,
    },
    DataType.RANKING: {
        DataType.RANKING,
        DataType.ANY,
    },
    DataType.RANKING_SET: {
        DataType.RANKING_SET,
        DataType.ANY,
    },
    DataType.CORRELATION: {
        DataType.CORRELATION,
        DataType.ANY,
    },
    DataType.SENSITIVITY: {
        DataType.SENSITIVITY,
        DataType.ANY,
    },
    DataType.MCDA_CONFIG: {
        DataType.MCDA_CONFIG,
        DataType.ANY,
    },
    DataType.REFERENCE_POINTS: {
        DataType.REFERENCE_POINTS,
        DataType.ANY,
    },
    DataType.ANY: set(DataType),
}


# Which node types typically produce / consume which data types
# (used for higher-level checks and documentation)

NODE_OUTPUT_TYPES: dict[NodeType, set[DataType]] = {
    NodeType.MATRIX: {DataType.MATRIX, DataType.CRITERIA_TYPES},
    NodeType.WEIGHTS: {DataType.WEIGHTS},
    NodeType.MCDA: {DataType.PREFERENCE, DataType.RANKING, DataType.MCDA_CONFIG},
    NodeType.RANKING: {DataType.RANKING},
    NodeType.CORRELATION: {DataType.CORRELATION},
    NodeType.VISUALIZATION: set(),
    NodeType.SENSITIVITY: {DataType.SENSITIVITY, DataType.RANKING_SET},
    NodeType.INPUT: {
        DataType.WEIGHTS,
        DataType.PREFERENCE,
        DataType.REFERENCE_POINTS,
        DataType.MATRIX,
    },
}


@dataclass
class ConnectionError:
    code: str
    message: str
    edge_id: UUID | None = None
    source_node: UUID | None = None
    target_node: UUID | None = None
    details: dict = field(default_factory=dict)


@dataclass
class ValidationResult:
    is_valid: bool
    errors: list[ConnectionError] = field(default_factory=list)

    def add(self, error: ConnectionError) -> None:
        self.errors.append(error)
        self.is_valid = False


def _get_node_map(schema: DecisionModelSchema) -> dict[UUID, Node]:
    return {node.id: node for node in schema.nodes}


def _get_port(node: Node, port_id: str, direction: str):
    ports = node.ports.inputs if direction == "input" else node.ports.outputs
    for port in ports:
        if port.id == port_id or port.name == port_id:
            return port
    return None


def _check_data_type_compatibility(
    source_type: DataType, target_type: DataType
) -> bool:
    allowed = ALLOWED_DATA_TYPE_FLOW.get(source_type, set())
    return target_type in allowed or target_type == DataType.ANY


def _check_extension_compatibility(source: Node, target: Node) -> bool:
    # Same extension is always ok
    if source.extension == target.extension:
        return True
    # Visualization and some correlation blocks can accept mixed (future)
    if target.type in {NodeType.VISUALIZATION, NodeType.CORRELATION}:
        return True
    return False


def _extract_dimensions(node: Node) -> tuple[int | None, int | None]:
    """
    Returns (n_alternatives, n_criteria) from node data if available.
    """
    data = node.data or {}
    n_alt = data.get("n_alternatives")
    n_crit = data.get("n_criteria")

    if n_alt is None and "matrix" in data and data["matrix"]:
        matrix = data["matrix"]
        try:
            n_alt = len(matrix)
            n_crit = len(matrix[0]) if matrix else None
        except (TypeError, IndexError):
            pass

    if n_crit is None and "criteria_types" in data:
        try:
            n_crit = len(data["criteria_types"])
        except TypeError:
            pass

    if n_crit is None and "weights" in data:
        try:
            n_crit = len(data["weights"])
        except TypeError:
            pass

    return n_alt, n_crit


def _has_cycle(schema: DecisionModelSchema) -> bool:
    """Kahn's algorithm for cycle detection."""
    graph: dict[UUID, list[UUID]] = defaultdict(list)
    in_degree: dict[UUID, int] = {node.id: 0 for node in schema.nodes}

    for edge in schema.edges:
        graph[edge.source].append(edge.target)
        if edge.target in in_degree:
            in_degree[edge.target] += 1
        else:
            in_degree[edge.target] = 1
        if edge.source not in in_degree:
            in_degree[edge.source] = 0

    queue = deque([nid for nid, deg in in_degree.items() if deg == 0])
    visited = 0

    while queue:
        current = queue.popleft()
        visited += 1
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return visited != len(in_degree)


def validate_connections(schema: DecisionModelSchema) -> ValidationResult:
    """
    Full validation of edges against ports, data types, extensions,
    dimensions and graph structure (no cycles).
    """
    result = ValidationResult(is_valid=True)
    node_map = _get_node_map(schema)

    # 1. Basic referential integrity
    for edge in schema.edges:
        if edge.source not in node_map:
            result.add(
                ConnectionError(
                    code="SOURCE_NODE_NOT_FOUND",
                    message=f"Source node {edge.source} does not exist",
                    edge_id=edge.id,
                    source_node=edge.source,
                    target_node=edge.target,
                )
            )
            continue

        if edge.target not in node_map:
            result.add(
                ConnectionError(
                    code="TARGET_NODE_NOT_FOUND",
                    message=f"Target node {edge.target} does not exist",
                    edge_id=edge.id,
                    source_node=edge.source,
                    target_node=edge.target,
                )
            )
            continue

        source_node = node_map[edge.source]
        target_node = node_map[edge.target]

        source_port = _get_port(source_node, edge.source_port, "output")
        target_port = _get_port(target_node, edge.target_port, "input")

        if source_port is None:
            result.add(
                ConnectionError(
                    code="SOURCE_PORT_NOT_FOUND",
                    message=(
                        f"Output port '{edge.source_port}' not found "
                        f"on node {source_node.label or source_node.id}"
                    ),
                    edge_id=edge.id,
                    source_node=edge.source,
                    target_node=edge.target,
                )
            )
            continue

        if target_port is None:
            result.add(
                ConnectionError(
                    code="TARGET_PORT_NOT_FOUND",
                    message=(
                        f"Input port '{edge.target_port}' not found "
                        f"on node {target_node.label or target_node.id}"
                    ),
                    edge_id=edge.id,
                    source_node=edge.source,
                    target_node=edge.target,
                )
            )
            continue

        # 2. Data type compatibility
        if not _check_data_type_compatibility(
            source_port.data_type, target_port.data_type
        ):
            result.add(
                ConnectionError(
                    code="DATA_TYPE_MISMATCH",
                    message=(
                        f"Cannot connect {source_port.data_type.value} "
                        f"→ {target_port.data_type.value}"
                    ),
                    edge_id=edge.id,
                    source_node=edge.source,
                    target_node=edge.target,
                    details={
                        "source_data_type": source_port.data_type.value,
                        "target_data_type": target_port.data_type.value,
                    },
                )
            )

        # 3. Extension compatibility
        if not _check_extension_compatibility(source_node, target_node):
            result.add(
                ConnectionError(
                    code="EXTENSION_MISMATCH",
                    message=(
                        f"Extension mismatch: {source_node.extension.value} "
                        f"→ {target_node.extension.value}"
                    ),
                    edge_id=edge.id,
                    source_node=edge.source,
                    target_node=edge.target,
                )
            )

        # 4. Dimensionality (when both sides expose dimensions)
        src_alt, src_crit = _extract_dimensions(source_node)
        tgt_alt, tgt_crit = _extract_dimensions(target_node)

        if src_crit is not None and tgt_crit is not None and src_crit != tgt_crit:
            result.add(
                ConnectionError(
                    code="CRITERIA_COUNT_MISMATCH",
                    message=(
                        f"Number of criteria differs: "
                        f"{src_crit} (source) vs {tgt_crit} (target)"
                    ),
                    edge_id=edge.id,
                    source_node=edge.source,
                    target_node=edge.target,
                    details={"source_criteria": src_crit, "target_criteria": tgt_crit},
                )
            )

        if src_alt is not None and tgt_alt is not None and src_alt != tgt_alt:
            # Only relevant for certain flows (e.g. ranking comparison)
            if target_node.type in {NodeType.CORRELATION, NodeType.SENSITIVITY}:
                result.add(
                    ConnectionError(
                        code="ALTERNATIVES_COUNT_MISMATCH",
                        message=(
                            f"Number of alternatives differs: "
                            f"{src_alt} (source) vs {tgt_alt} (target)"
                        ),
                        edge_id=edge.id,
                        source_node=edge.source,
                        target_node=edge.target,
                        details={
                            "source_alternatives": src_alt,
                            "target_alternatives": tgt_alt,
                        },
                    )
                )

    # 5. Multiple connections to non-multiple ports
    incoming: dict[tuple[UUID, str], list[UUID]] = defaultdict(list)
    for edge in schema.edges:
        key = (edge.target, edge.target_port)
        incoming[key].append(edge.id)

    for (target_id, port_id), edge_ids in incoming.items():
        if target_id not in node_map:
            continue
        target_node = node_map[target_id]
        port = _get_port(target_node, port_id, "input")
        if port and not port.multiple and len(edge_ids) > 1:
            result.add(
                ConnectionError(
                    code="MULTIPLE_CONNECTIONS_NOT_ALLOWED",
                    message=(
                        f"Port '{port_id}' on node "
                        f"'{target_node.label or target_id}' "
                        f"does not allow multiple connections "
                        f"({len(edge_ids)} found)"
                    ),
                    target_node=target_id,
                    details={"port": port_id, "edge_ids": [str(e) for e in edge_ids]},
                )
            )

    # 6. Cycles
    if _has_cycle(schema):
        result.add(
            ConnectionError(
                code="CYCLE_DETECTED",
                message="The decision model graph contains a cycle",
            )
        )

    # 7. Required ports (warning-level – collected but model can still be saved as draft)
    for node in schema.nodes:
        connected_input_ports = {
            e.target_port for e in schema.edges if e.target == node.id
        }
        for port in node.ports.inputs:
            if port.required and port.id not in connected_input_ports and port.name not in connected_input_ports:
                result.add(
                    ConnectionError(
                        code="REQUIRED_PORT_NOT_CONNECTED",
                        message=(
                            f"Required port '{port.name}' on node "
                            f"'{node.label or node.id}' is not connected"
                        ),
                        target_node=node.id,
                        details={"port": port.name},
                    )
                )

    return result


def can_connect(
    schema: DecisionModelSchema,
    source_node_id: UUID,
    source_port_id: str,
    target_node_id: UUID,
    target_port_id: str,
) -> ValidationResult:
    """
    Check whether a single new connection would be valid.
    Useful for frontend real-time validation.
    """
    from copy import deepcopy
    from uuid import uuid4

    from .schemas import Edge

    temp = deepcopy(schema)
    temp.edges.append(
        Edge(
            id=uuid4(),
            source=source_node_id,
            source_port=source_port_id,
            target=target_node_id,
            target_port=target_port_id,
        )
    )
    return validate_connections(temp)
