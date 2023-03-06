import threading
import time
import unittest
from P2P.network import Node

class TestDiscovery(unittest.TestCase):
    def test_node_start_stop():
        node = Node('127.0.0.1', 5000)
        node_thread = threading.Thread(target=node.start)
        node_thread.start()

        # Give the thread some time to start
        time.sleep(1)

        # Check if the node is running
        assert node_thread.is_alive()

        # Stop the node
        node.socket.close()

        # Give the thread some time to stop
        time.sleep(1)

        # Check if the node has stopped
        assert not node_thread.is_alive()


    def test_node_connect():
        node1 = Node('127.0.0.1', 5001)
        node2 = Node('127.0.0.1', 5002)

        # Start both nodes
        node1_thread = threading.Thread(target=node1.start)
        node2_thread = threading.Thread(target=node2.start)
        node1_thread.start()
        node2_thread.start()

        # Give the threads some time to start
        time.sleep(1)

        # Connect node1 to node2
        node1.connect('127.0.0.1', 5002)

        # Give the connection some time to establish
        time.sleep(1)

        # Check if node1 has node2 as a peer
        assert ('127.0.0.1', 5002) in node1.peers

        # Stop both nodes
        node1.socket.close()
        node2.socket.close()

        # Give the threads some time to stop
        time.sleep(1)

        # Check if the nodes have stopped
        assert not node1_thread.is_alive()
        assert not node2_thread.is_alive()

if __name__ == "__main__":
    unittest.main()
