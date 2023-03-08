import unittest

from hypergraph.node import Node

class TestNode(unittest.TestCase):

    def test_node_creation(self):
            node = Node("A")
            self.assertEqual(node.name, "A")
            self.assertEqual(node.weight, 1)
            self.assertEqual(node.edges, set())
            self.assertIsNone(node.socket)

            node = Node("B", weight=2, socket="localhost")
            self.assertEqual(node.name, "B")
            self.assertEqual(node.weight, 2)
            self.assertEqual(node.edges, set())
            self.assertEqual(node.socket, "localhost")

    def test_node_comparison(self):
        node1 = Node("A")
        node2 = Node("B")
        self.assertTrue(node1 < node2)

    def test_node_representation(self):
        node = Node("A", weight=2, socket="localhost")
        self.assertEqual(repr(node), "Node: (name=A, weight=2, edges=set())")

if __name__ == "__main__":
    unittest.main()
