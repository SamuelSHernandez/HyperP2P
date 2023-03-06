import unittest

from hypergraph.algorithms import shortest_path
from hypergraph.graph import Graph


class TestAlgorithms(unittest.TestCase):
    def test_shortest_path(self):
        # create a graph with three nodes and two edges
        g = Graph(nodes=["A", "B", "C"], edges=[({"A", "B"}, 1), ({"B", "C"}, 2)])

        # find the shortest path between A and C
        path = shortest_path(g, "A", "C")

        # verify the path is correct
        self.assertEqual(path, ["A", "B", "C"])


if __name__ == "__main__":
    unittest.main()
