"""
This module provides custom exceptions for the hypergraph module.
"""

class NodeAlreadyExistsError(Exception):
    """
    Exception raised when a node with the same name already exists in the hypergraph.

    :param node_name: The name of the node that already exists.
    :type node_name: str
    """
    def __init__(self, node_name):
        self.node_name = node_name

    def __str__(self):
        return f"Node with name '{self.node_name}' already exists in the hypergraph."


class HyperedgeAlreadyExistsError(Exception):
    """
    Exception raised when a hyperedge with the same nodes already exists in the hypergraph.

    :param nodes: The set of nodes that form the hyperedge that already exists.
    :type nodes: Set[Node]
    """
    def __init__(self, nodes):
        self.nodes = nodes

    def __str__(self):
        node_names = ", ".join(sorted(node.name for node in self.nodes))
        return f"Hyperedge with nodes '{node_names}' already exists in the hypergraph."
