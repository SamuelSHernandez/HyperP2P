from typing import Set

from .node import Node


class Edge:
    def __init__(self, nodes: Set[Node], weight: int = 1):
        self.nodes = nodes
        self.weight = weight

    def __repr__(self):
        node_names = [node.name for node in self.nodes]
        return f"Edge(nodes={node_names}, weight={self.weight})"
