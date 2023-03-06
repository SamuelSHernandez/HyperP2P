from typing import Set

from .node import Node

"""
This module provides classes to represent edges in a hypergraph.
"""

class Edge:
    """
    Represents an edge in a hypergraph.

    :param nodes: A set of nodes connected by this edge.
    :type nodes: Set[Node]
    :param weight: The weight of this edge (default is 1).
    :type weight: int
    """
    def __init__(self, nodes: Set[Node], weight: int = 1):
        self.nodes = nodes
        self.weight = weight

    def __repr__(self):
        node_names = [node.name for node in self.nodes]
        return f"Edge(nodes={node_names}, weight={self.weight})"
