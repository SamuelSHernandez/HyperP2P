import unittest

from Hypergraph.exceptions import HyperedgeAlreadyExistsError, NodeAlreadyExistsError
from Hypergraph.graph import Graph


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()

    def test_add_node(self):
        self.graph.add_node("A")
        self.assertIn("A", self.graph.get_nodes())

    def test_add_existing_node(self):
        self.graph.add_node("A")
        with self.assertRaises(NodeAlreadyExistsError):
            self.graph.add_node("A")

    def test_add_edge(self):
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_edge({"A", "B"}, 2)
        self.assertIn({"A", "B"}, [edge.nodes for edge in self.graph.edges])

    def test_add_existing_edge(self):
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_edge({"A", "B"}, 2)
        with self.assertRaises(HyperedgeAlreadyExistsError):
            self.graph.add_edge({"A", "B"}, 3)

    def test_remove_node(self):
        self.graph.add_node("A")
        self.graph.remove_node("A")
        self.assertNotIn("A", self.graph.get_nodes())

    def test_remove_edge(self):
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_edge({"A", "B"}, 2)
        self.graph.remove_edge({"A", "B"})
        self.assertNotIn({"A", "B"}, [edge.nodes for edge in self.graph.edges])

    def test_update_edge_weight(self):
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_edge({"A", "B"}, 2)
        self.graph.update_edge_weight({"A", "B"}, 3)
        self.assertEqual(3, self.graph.get_edge({"A", "B"}).weight)

    def test_get_nodes(self):
        self.graph.add_node("A")
        self.graph.add_node("B")
        nodes = self.graph.get_nodes()
        self.assertIn("A", nodes)
        self.assertIn("B", nodes)

    def test_get_edges(self):
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_edge({"A", "B"}, 2)
        edges = self.graph.get_edges()
        self.assertIn(({"A", "B"}, 2), edges)


if __name__ == "__main__":
    unittest.main()
