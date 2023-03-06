import contextlib
from typing import List, Set, Tuple, Union

from .edge import Edge
from .exceptions import HyperedgeAlreadyExistsError, NodeAlreadyExistsError
from .node import Node


class Graph:
    def __init__(
        self,
        nodes: List[str] = None,
        edges: List[Tuple[Set[str], int]] = None,
        name: str = None,
    ):
        if nodes is None:
            nodes = []
        if edges is None:
            edges = []
        self.nodes = set()
        self.edges = set()
        self.name = name

        for node in nodes:
            self.add_node(node)

        for nodes, edge in edges:
            self.add_edge(nodes, edge)

    def __repr__(self):
        return f"Graph(name={self.name}, nodes={self.nodes}, edges={self.edges})"

    def add_node(self, name: str, weight: int = 1, socket=None):
        if not isinstance(name, str):
            raise TypeError("node name must be a string")
        if self.get_node(name) is not None:
            raise NodeAlreadyExistsError("node with this name already exists")
        node = Node(name, weight)
        node.socket = socket  # assign socket attribute
        self.nodes.add(node)

    def add_edge(self, nodes: Set[str], weight: int = 1) -> None:
        with contextlib.suppress(ValueError):
            if nodes in [edge.nodes for edge in self.edges]:
                raise HyperedgeAlreadyExistsError(
                    "edge with this set of nodes already exists"
                )
            edge = Edge({self.get_node(node) for node in nodes}, weight)
            self.edges.add(edge)
            for node in edge.nodes:
                node.edges.add(edge)

    def get_node(self, name: str) -> Union[Node, None]:
        return next((node for node in self.nodes if node.name == name), None)

    def get_edge(self, nodes: Set[Node]) -> Union[Edge, None]:
        return next((edge for edge in self.edges if edge.nodes == nodes), None)

    def remove_node(self, node: str) -> None:
        node = self.get_node(node)
        if node is None:
            return
        self.nodes.remove(node)
        for edge in node.edges:
            self.edges.remove(edge)
            for other_node in edge.nodes:
                if other_node != node:
                    other_node.edges.remove(edge)

    def remove_edge(self, nodes: Set[str]) -> None:
        edge = self.get_edge({self.get_node(name) for name in nodes})
        if edge is None:
            return
        self.edges.remove(edge)
        for node in edge.nodes:
            node.edges.remove(edge)

    def update_edge_weight(self, nodes: Set[str], weight: int) -> None:
        edge = self.get_edge({self.get_node(name) for name in nodes})
        if edge is not None:
            edge.weight = weight

    def get_nodes(self) -> List[str]:
        return [node.name for node in self.nodes]

    def get_edges(self) -> List[Tuple[Set[str], int]]:
        return [
            ([node.name for node in edge.nodes], edge.weight) for edge in self.edges
        ]
