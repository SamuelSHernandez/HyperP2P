import heapq
from typing import List

from .graph import Graph


def shortest_path(graph: Graph, start: str, end: str) -> List[str]:
    distances = {node.name: float("inf") for node in graph.nodes}
    distances[start] = 0
    queue = [(0, graph.get_node(start))]
    predecessors = {node.name: None for node in graph.nodes}
    while queue:
        current_distance, current_node = heapq.heappop(queue)
        if current_distance > distances[current_node.name]:
            continue
        if current_node.name == end:
            path = []
            while current_node is not None:
                path.append(current_node.name)
                current_node = graph.get_node(predecessors[current_node.name])
            path.reverse()
            return path
        for edge in current_node.edges:
            for other_node in edge.nodes:
                if other_node != current_node:
                    tentative_distance = (
                        distances[current_node.name] + edge.weight / other_node.weight
                    )
                    if tentative_distance < distances[other_node.name]:
                        distances[other_node.name] = tentative_distance
                        predecessors[other_node.name] = current_node.name
                        heapq.heappush(queue, (tentative_distance, other_node))
    return []
