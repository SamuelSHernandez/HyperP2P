class Node:
    def __init__(self, name: str, weight: int = 1, socket=None):
        self.name = name
        self.weight = weight
        self.edges = set()
        self.socket = socket

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return f"Node: (name={self.name}, weight={self.weight}, edges={self.edges})"
