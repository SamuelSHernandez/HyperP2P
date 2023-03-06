import contextlib
from typing import List, Set, Tuple, Union

from .edge import Edge
from .exceptions import HyperedgeAlreadyExistsError, NodeAlreadyExistsError
from .node import Node

"""
This module provides a Graph class to represent a hypergraph.
"""


class Graph:
    """
    Represents a hypergraph.

    :param nodes: A list of node names to initialize the hypergraph (default is an empty list).
    :type nodes: List[str]
    :param edges: A list of tuples representing the edges in the hypergraph. Each tuple contains a set of node names
                  and the weight of the edge (default is an empty list).
    :type edges: List[Tuple[Set[str], int]]
    :param name: The name of the hypergraph (default is None).
    :type name: str
    """
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
        """
        Returns a string representation of the graph.

        :return: A string representation of the graph.
        :rtype: str
        """
        return f"Graph(name={self.name}, nodes={self.nodes}, edges={self.edges})"

    def add_node(self, name: str, weight: int = 1, socket=None):
        """
        Adds a new node to the hypergraph.

        :param name: The name of the node to add.
        :type name: str
        :param weight: The weight of the node (default is 1).
        :type weight: int
        :param socket: The socket of the node (default is None).
        :type socket: Any
        """
        if not isinstance(name, str):
            raise TypeError("node name must be a string")
        if self.get_node(name) is not None:
            raise NodeAlreadyExistsError("node with this name already exists")
        node = Node(name, weight)
        node.socket = socket  # assign socket attribute
        self.nodes.add(node)

    def add_edge(self, nodes: Set[str], weight: int = 1) -> None:
        """
        Adds a new edge to the hypergraph.

        :param nodes: A set of node names connected by the edge.
        :type nodes: Set[str]
        :param weight: The weight of the edge (default is 1).
        :type weight: int
        """
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
        """
        Returns the node with the specified name.

        :param name: The name of the node to return.
        :type name: str
        :return: The node with the specified name or None if it doesn't exist.
        :rtype: Union[Node, None]
        """
        return next((node for node in self.nodes if node.name == name), None)

    def get_edge(self, nodes: Set[Node]) -> Union[Edge, None]:
        """
        Returns the edge that connects the specified nodes.

        :param nodes: A set of nodes to look for in the hypergraph.
        :type nodes: Set[Node]
        :return: The edge that connects the specified nodes or None if it doesn't exist.
        :rtype: Union[Edge, None]
        """
        return next((edge for edge in self.edges if edge.nodes == nodes), None)

    def remove_node(self, node: str) -> None:
        """
        Removes the specified node and all edges connected to it from the hypergraph.

        :param node: The name of the node to remove.
        :type node: str
        """
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
        """
        Removes the edge that connects the specified nodes from the hypergraph.

        :param nodes: A set of node names connected by the edge to remove.
        :type nodes: Set[str]
        """
        edge = self.get_edge({self.get_node(name) for name in nodes})
        if edge is None:
            return
        self.edges.remove(edge)
        for node in edge.nodes:
            node.edges.remove(edge)

    def update_edge_weight(self, nodes: Set[str], weight: int) -> None:
        """
        Updates the weight of the edge that connects the specified nodes.

        :param nodes: A set of node names connected by the edge to update.
        :type nodes: Set[str]
        :param weight: The new weight of the edge.
        :type weight: int
        """
        edge = self.get_edge({self.get_node(name) for name in nodes})
        if edge is not None:
            edge.weight = weight

    def get_nodes(self) -> List[str]:
        """
        Returns a list of all node names in the hypergraph.

        :return: A list of all node names in the hypergraph.
        :rtype: List[str]
        """
        return [node.name for node in self.nodes]

    def get_edges(self) -> List[Tuple[Set[str], int]]:
        """
        Returns a list of tuples representing all edges in the hypergraph.

        :return: A list of tuples representing all edges in the hypergraph.
        :rtype: List[Tuple[Set[str], int]]
        """
        return [
            ([node.name for node in edge.nodes], edge.weight) for edge in self.edges
        ]
