"""
Pydantic schemas for Decision Model (v1.1).
Used for validation of the JSON structure stored in DecisionModel.schema.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, model_validator


# ===== Enums =====

class NodeType(str, Enum):
    MATRIX = "matrix"
    WEIGHTS = "weights"
    MCDA = "mcda"
    RANKING = "ranking"
    CORRELATION = "correlation"
    VISUALIZATION = "visualization"
    SENSITIVITY = "sensitivity"
    INPUT = "input"


class Extension(str, Enum):
    CRISP = "crisp"
    FUZZY = "fuzzy"


class DataType(str, Enum):
    MATRIX = "matrix"
    CRITERIA_TYPES = "criteria_types"
    WEIGHTS = "weights"
    PREFERENCE = "preference"
    RANKING = "ranking"
    RANKING_SET = "ranking_set"
    CORRELATION = "correlation_matrix"
    SENSITIVITY = "sensitivity"
    MCDA_CONFIG = "mcda_config"
    REFERENCE_POINTS = "reference_points"
    ANY = "any"


class AnnotationType(str, Enum):
    TEXT = "text"
    GROUP = "group"
    LEGEND = "legend"


# ===== Shared sub-models =====

class Position(BaseModel):
    x: float
    y: float


class Size(BaseModel):
    width: float = 200
    height: float = 120


class Port(BaseModel):
    id: str
    name: str
    label: str | None = None
    data_type: DataType
    required: bool = False
    multiple: bool = False


class Ports(BaseModel):
    inputs: list[Port] = Field(default_factory=list)
    outputs: list[Port] = Field(default_factory=list)


class UISettings(BaseModel):
    color: str | None = None
    collapsed: bool = False
    locked: bool = False
    z_index: int = 1


class ValidationState(BaseModel):
    is_valid: bool = True
    errors: list[str] = Field(default_factory=list)


class EdgeStyle(BaseModel):
    stroke: str = "#666666"
    stroke_width: float = 2
    animated: bool = False


# ===== Node =====

class Node(BaseModel):
    id: UUID
    numeric_id: int | None = None
    type: NodeType
    method: str | None = None
    extension: Extension = Extension.CRISP
    label: str = ""
    position: Position
    size: Size = Field(default_factory=Size)
    ports: Ports = Field(default_factory=Ports)
    data: dict[str, Any] = Field(default_factory=dict)
    params: dict[str, Any] = Field(default_factory=dict)
    ui: UISettings = Field(default_factory=UISettings)
    validation: ValidationState = Field(default_factory=ValidationState)

    @field_validator("method")
    @classmethod
    def method_uppercase(cls, v: str | None) -> str | None:
        return v.upper() if v else v


# ===== Edge =====

class Edge(BaseModel):
    id: UUID
    numeric_id: int | None = None
    source: UUID
    source_port: str
    target: UUID
    target_port: str
    label: str | None = None
    style: EdgeStyle = Field(default_factory=EdgeStyle)


# ===== Annotations =====

class AnnotationStyle(BaseModel):
    font_size: int | None = None
    color: str | None = None
    background: str | None = None
    border: str | None = None
    padding: int | None = None


class Annotation(BaseModel):
    id: UUID
    type: AnnotationType
    content: Any = None
    label: str | None = None
    position: Position | None = None
    size: Size | None = None
    node_ids: list[UUID] = Field(default_factory=list)
    style: AnnotationStyle = Field(default_factory=AnnotationStyle)


# ===== Metadata & Canvas =====

class Metadata(BaseModel):
    id: UUID | None = None
    name: str = Field(..., min_length=1, max_length=255)
    description: str = ""
    author_id: UUID | str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    tags: list[str] = Field(default_factory=list)
    is_public: bool = False
    notes: str = ""


class Canvas(BaseModel):
    zoom: float = 1.0
    offset_x: float = 0.0
    offset_y: float = 0.0
    grid_size: int = 20


# ===== Root schema =====

class DecisionModelSchema(BaseModel):
    schema_version: Literal["1.0", "1.1"] = "1.1"
    metadata: Metadata
    canvas: Canvas = Field(default_factory=Canvas)
    nodes: list[Node] = Field(default_factory=list)
    edges: list[Edge] = Field(default_factory=list)
    annotations: list[Annotation] = Field(default_factory=list)

    @model_validator(mode="after")
    def check_unique_node_ids(self) -> DecisionModelSchema:
        ids = [n.id for n in self.nodes]
        if len(ids) != len(set(ids)):
            raise ValueError("Node IDs must be unique")
        return self

    @model_validator(mode="after")
    def check_unique_edge_ids(self) -> DecisionModelSchema:
        ids = [e.id for e in self.edges]
        if len(ids) != len(set(ids)):
            raise ValueError("Edge IDs must be unique")
        return self
