import threading
import time
import unittest

from p2p.network import Peer


class TestNetwork(unittest.TestCase):
    def test_node():
        # Create 3 nodes and connect them to each other
        node1 = Peer("127.0.0.1", 5001)
        node2 = Peer("127.0.0.1", 5002)
        node3 = Peer("127.0.0.1", 5003)
        node1.connect("127.0.0.1", 5002)
        node2.connect("127.0.0.1", 5003)
        node3.connect("127.0.0.1", 5001)

        # Define a function to send messages between nodes
        def send_messages(node, peer, num_messages):
            for i in range(num_messages):
                message = f"Hello from {node.ip}:{node.port}, timestamp={time.time()}"
                node.socket.sendall(f"MESSAGE {message}".encode())
                time.sleep(0.1)

        # Start the nodes in separate threads
        node_threads = [
            threading.Thread(target=node.start) for node in [node1, node2, node3]
        ]
        for thread in node_threads:
            thread.start()

        # Send messages between nodes and assert that they are received correctly
        send_messages(node1, node2, 5)
        send_messages(node2, node3, 5)
        send_messages(node3, node1, 5)

        # Wait for messages to be received
        time.sleep(1)

        # Assert that the message timestamps are updated correctly
        for message, timestamps in node1.message_timestamp.items():
            assert len(timestamps) == 2
            assert all(
                peer in [(node2.ip, node2.port), (node3.ip, node3.port)]
                for peer, timestamp in timestamps
            )
        for message, timestamps in node2.message_timestamp.items():
            assert len(timestamps) == 2
            assert all(
                peer in [(node1.ip, node1.port), (node3.ip, node3.port)]
                for peer, timestamp in timestamps
            )
        for message, timestamps in node3.message_timestamp.items():
            assert len(timestamps) == 2
            assert all(
                peer in [(node1.ip, node1.port), (node2.ip, node2.port)]
                for peer, timestamp in timestamps
            )


if __name__ == "__main__":
    unittest.main()
