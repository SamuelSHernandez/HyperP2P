import unittest

from hypergraph.edge import Edge
from hypergraph.node import Node


class TestEdge(unittest.TestCase):
    def test_edge_repr():
        nodes = {Node("A"), Node("B")}
        edge = Edge(nodes, weight=3)
        expected_repr = "Edge(nodes=['A', 'B'], weight=3)"
        assert repr(edge) == expected_repr


if __name__ == "__main__":
    unittest.main()
