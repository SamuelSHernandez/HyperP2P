"""
This module provides classes to represent nodes and edges in a hypergraph.
"""

class Node:
    """
    Represents a node in a hypergraph.

    :param name: The name of the node.
    :type name: str
    :param weight: The weight of the node (default is 1).
    :type weight: int
    """
    def __init__(self, name: str, weight: int = 1, socket=None):
        """
        Represents an edge in a hypergraph.

        :param nodes: A set of nodes connected by this edge.
        :type nodes: Set[Node]
        :param weight: The weight of this edge (default is 1).
        :type weight: int
        """
        self.name = name
        self.weight = weight
        self.edges = set()
        self.socket = socket

    def __lt__(self, other):
        return self.weight < other.weight

    def __repr__(self):
        return f"Node(name={self.name}, weight={self.weight}, edges={self.edges})"
