from dataclasses import dataclass, field
from typing import Union, Optional


@dataclass
class Node:
    id: int
    name: str
    x: int
    y: int
    weight: int


@dataclass
class Edge:
    id: int
    start_node: Node
    end_node: Node
    weight: int
    offset: Optional[int] = None


@dataclass
class Result:
    target: Union[Node, Edge]
    score: int


@dataclass
class Graph:
    nodes: list = field(default_factory=list)
    edges: list = field(default_factory=list)
    results: list = field(default_factory=list)
