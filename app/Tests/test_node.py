import unittest

from Hypergraph.node import Node


class TestNode(unittest.TestCase):
    def test_node():
        # Create a node
        node1 = Node("A", weight=2)
        assert node1.name == "A"
        assert node1.weight == 2

        # Test adding and removing edges
        node2 = Node("B")
        node1.add_edge(node2)
        assert node1.edges == {node2}
        assert node2.edges == {node1}
        node1.remove_edge(node2)
        assert node1.edges == set()
        assert node2.edges == set()

        # Test node comparison
        node3 = Node("A")
        assert node1 == node3
        assert node1 != node2

        # Test setting socket attribute
        node1.socket = "localhost:8000"
        assert node1.socket == "localhost:8000"

        # Test node string representation
        assert str(node1) == "Node(name=A, weight=2)"


if __name__ == "__main__":
    unittest.main()
