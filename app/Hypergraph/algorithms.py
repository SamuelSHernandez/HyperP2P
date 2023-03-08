import heapq
from typing import List

from .graph import Graph, Node


def shortest_path(graph: Graph, start: str, end: str) -> List[str]:
    """
    Computes the shortest path between two nodes in a graph using Dijkstra's algorithm.

    :param graph: The graph in which to find the shortest path.
    :type graph: Graph
    :param start: The name of the starting node.
    :type start: str
    :param end: The name of the ending node.
    :type end: str
    :return: A list of node names representing the shortest path between the start and end nodes.
    :rtype: List[str]
    """

    # Set up distances and queue
    nodes = graph.nodes
    for node in nodes:
        node.distance = float("inf")
        node.predecessor = None
    start_node = graph.get_node(start)
    start_node.distance = 0
    queue = {start_node: 0}  # Use a dictionary to track the queue

    # Use a set to keep track of visited nodes
    visited = set()

    while queue:
        current_node = min(queue, key=queue.get)
        del queue[current_node]
        visited.add(current_node)

        if current_node.name == end:
            # Early exit if we've found the shortest path
            path = []
            while current_node is not None:
                path.append(current_node.name)
                current_node = current_node.predecessor
            path.reverse()
            return path

        for edge in current_node.edges:
            for other_node in edge.nodes:
                if other_node != current_node:
                    if other_node in visited:
                        continue
                    tentative_distance = (
                        current_node.distance + edge.weight / other_node.weight
                    )
                    if tentative_distance < other_node.distance:
                        other_node.distance = tentative_distance
                        other_node.predecessor = current_node
                        queue[other_node] = other_node.distance

    return []
