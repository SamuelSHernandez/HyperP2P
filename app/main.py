from Hypergraph.algorithms import shortest_path
from Hypergraph.graph import Graph
from P2P.network import Node, Discovery
import threading
from Utils.config import IP_ADDRESS_PREFIX, IP_ADDRESS_START_PORT

# create a graph with two nodes and one edge
g = Graph(nodes=["A", "B"], edges=[({"A", "B"}, 1)])

# print the nodes and edges
print(g.get_nodes())
print(g.get_edges())

# add a new node
g.add_node("C")

# add a new edge
g.add_edge({"B", "C"}, 2)

# print the updated nodes and edges
print(g.get_nodes())
print(g.get_edges())

# remove a node
g.remove_node("B")

# print the final nodes and edges
print(g.get_nodes())
print(g.get_edges())

# create a graph with three nodes and two edges
g = Graph(nodes=["A", "B", "C"], edges=[({"A", "B"}, 1), ({"B", "C"}, 2)])

# find the shortest path between A and C
path = shortest_path(g, "A", "C")

# print the path
print(path)
