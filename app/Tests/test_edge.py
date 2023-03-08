import unittest

from hypergraph.edge import Edge
from hypergraph.node import Node


class TestEdge(unittest.TestCase):
    def test_edge_repr(self):
        nodes = {Node("A"), Node("B")}
        edge = Edge(nodes, weight=3)
        expected_repr = "Edge: (nodes=['B', 'A'], weight=3)"
        self.assertEqual(repr(edge), expected_repr)


if __name__ == "__main__":
    unittest.main()
