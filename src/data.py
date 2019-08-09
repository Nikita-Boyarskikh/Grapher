from dataclasses import dataclass, field
from typing import Union, Optional

from PyQt5.QtGui import QColor


@dataclass
class Node:
    id: int
    name: str
    x: float
    y: float
    weight: float
    color: QColor
    textColor: QColor


@dataclass
class Edge:
    id: int
    start_node: Node
    end_node: Node
    length: float
    speed: float
    offset: Optional[float] = None


@dataclass
class Result:
    target: Union[Node, Edge]
    score: float


@dataclass
class Graph:
    nodes: list = field(default_factory=list)
    edges: list = field(default_factory=list)
    results: list = field(default_factory=list)
