import logging
import random
import threading
import time
import socket

from hypergraph.exceptions import HyperedgeAlreadyExistsError
from hypergraph.graph import Graph
from p2p.network import Discovery, Peer
from utils.config import IP_ADDRESS_PREFIX, IP_ADDRESS_START_PORT, NUM_NODES
from hypergraph.algorithms import shortest_path

# Configure logging
logging.basicConfig(filename="main.log", level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    try:
        # Create network
        num_nodes = NUM_NODES
        message = "This is a longer message!"

        network, peers = create_network(num_nodes)
        start_peers(peers, network)

        # Send message and measure traversal time
        start_node = peers[0]  # Choose the first node as the start node
        target_nodes = peers[1:]  # All other nodes are the target nodes
        traversal_time = send_message(start_node, target_nodes, message)

        print(f"Traversal time: {traversal_time:.6f}s")

    finally:
        for node in peers:
            node.socket.close()

        # Shutdown the logging system
        logging.shutdown()


def create_network(num_nodes):
    """
    Create a P2P network with the specified number of nodes.

    :param num_nodes: The number of nodes in the network.
    :return: The network and the list of peer objects.
    """
    network = Graph(name="My P2P Network")
    peers = [Peer(IP_ADDRESS_PREFIX, IP_ADDRESS_START_PORT + i) for i in range(num_nodes)]

    for i in range(num_nodes):
        network.add_node(peers[i].name)

    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.randint(0, 1) == 1:  # randomly add edges with 50% probability
                try:
                    network.add_edge({peers[i].name, peers[j].name}, weight=1)
                except HyperedgeAlreadyExistsError as e:
                    logger.warning(f"Error adding edge between nodes {i} and {j}: {e}")

    return network, peers


def create_routing_table(network):
    routing_table = {}
    for node1 in network.nodes:
        routing_table[node1.name] = {}
        for node2 in network.nodes:
            if node1 != node2:
                path = shortest_path(network, node1.name, node2.name)
                cost = sum(
                    network.get_edge(
                        {
                            network.get_node(path[i]),
                            network.get_node(path[i + 1]),
                        }
                    ).weight
                    for i in range(len(path) - 1)
                )
                routing_table[node1.name][node2.name] = {
                    "path": path,
                    "cost": cost,
                }
    return routing_table

def start_peers(peers):
    # Start peers and discovery service
    threads = [threading.Thread(target=node.start) for node in peers]
    for t in threads:
        t.start()

    # Start discovery service
    discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    discovery_socket.bind((peers[0].ip, peers[0].port))
    discovery_socket.listen()
    discovery = Discovery(discovery_socket, peers[0])
    discovery_thread = threading.Thread(target=discovery.start)
    discovery_thread.start()

    for i in range(len(peers)):
        for j in range(i + 1, len(peers)):
            try:
                peers[i].connect(peers[j].ip, peers[j].port)
                peers[j].connect(peers[i].ip, peers[i].port)
            except OSError as e:
                logger.warning(f"Error connecting nodes {i} and {j}: {e}")

def send_message(start_node, target_nodes, message):
    """
    Send a message to the target nodes and measure the time it takes to traverse the network.

    :param start_node: The starting node.
    :param target_nodes: A list of target nodes.
    :param message: The message to send.
    :return: The time it took to traverse the network.
    """
    start_time = time.time()
    message_with_timestamp = f"{message}, timestamp={start_time}"

    # Increment messages_sent counter
    with start_node.lock:
        start_node.messages_sent += 1

    for peer in start_node.peers:
        try:
            # Create a socket to connect to the peer
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((peer.ip, peer.port))
                s.sendall(message_with_timestamp.encode("utf-8"))

        except ConnectionRefusedError:
            start_node.logger.warning(f"Connection refused by {peer.ip}:{peer.port}")

        except OSError as e:
            start_node.logger.warning(
                f"Error sending message to {peer.ip}:{peer.port}: {e}"
            )

    # Wait for messages to arrive at the target nodes
    time.sleep(1)

    # Measure the time it took for the message to traverse the network
    traversal_times = []
    for target_node in target_nodes:
        with target_node.lock:
            if message in target_node.message_timestamp:
                for (peer, timestamp) in target_node.message_timestamp[message]:
                    traversal_time = time.time() - timestamp
                    traversal_times.append(traversal_time)

    end_time = time.time()
    total_time = end_time - start_time

    return total_time, traversal_times

if __name__ == "__main__":
    # Create network
    num_nodes = NUM_NODES
    message = "This is a longer message!"
    network, peers = create_network(num_nodes)

    # Create routing table
    routing_table = create_routing_table(network)

    # Log routing table
    logger.info("Routing Table:")
    for source_node, dest_data in routing_table.items():
        logger.info(f"{source_node}:")
        for dest_node, data in dest_data.items():
            logger.info(
                f"    {dest_node}: {' -> '.join(data['path'])} (cost={data['cost']})"
            )

    # Start peers and discovery service
    start_peers(peers)

    # Send message and measure traversal time
    start_node = peers[0]  # Choose the first node as the start node
    target_nodes = peers[1:]  # All other nodes are the target nodes

    traversal_time = send_message(start_node, target_nodes, message)
    logger.info(f"Total traversal time: {traversal_time:.6f}s")

    # Shutdown the logging system
    logging.shutdown()