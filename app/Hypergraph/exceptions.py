class NodeAlreadyExistsError(Exception):
    def __init__(self, node_name):
        self.node_name = node_name

    def __str__(self):
        return f"Node with name '{self.node_name}' already exists in the hypergraph."


class HyperedgeAlreadyExistsError(Exception):
    def __init__(self, nodes):
        self.nodes = nodes

    def __str__(self):
        node_names = ", ".join(sorted(node.name for node in self.nodes))
        return f"Hyperedge with nodes '{node_names}' already exists in the hypergraph."
