import logging
import random
import threading
import time
import sys
from hypergraph.algorithms import shortest_path
from hypergraph.graph import Graph
from p2p.network import Peer
from utils import config


def create_network(num_nodes):
    # Set random seed for reproducibility
    random.seed(492)

    # Create network
    network = Graph(name="My P2P Network")
    for i in range(num_nodes):
        network.add_node(
            f"{config.IP_ADDRESS_PREFIX}:{config.IP_ADDRESS_START_PORT+i}")
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.randint(0, 1) == 1:  # randomly add edges with 50% probability
                network.add_edge(
                    {
                        f"{config.IP_ADDRESS_PREFIX}:{config.IP_ADDRESS_START_PORT+i}",
                        f"{config.IP_ADDRESS_PREFIX}:{config.IP_ADDRESS_START_PORT+j}",
                    },
                    weight=1,
                )

    return network


def create_routing_table(network):
    # Create routing table
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
                    "cost": cost+1,
                }

    return routing_table


def start_nodes(network):
    # Create nodes and start threads
    nodes = [
        Peer(node.name.split(":")[0], int(node.name.split(":")[1]), [])
        for node in network.nodes
    ]
    threads = [threading.Thread(target=node.start) for node in nodes]
    for t in threads:
        t.start()

    return nodes, threads


def connect_peers(nodes, logger):
    # Connect nodes
    num_nodes = len(nodes)
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            try:
                nodes[i].connect(nodes[j].ip, nodes[j].port)
                nodes[j].connect(nodes[i].ip, nodes[i].port)
            except OSError as e:
                logger.warning(f"Error connecting nodes {i} and {j}: {e}")


def send_messages(nodes, message, logger, start_time):
    # Send message and measure traversal time
    start_node = nodes[0]  # Choose the first node as the start node
    target_nodes = nodes[1:]  # All other nodes are the target nodes
    traversal_time = 0

    for node in target_nodes:
        start_node.send_message(f"{message}")
        logger.info(
            f"Sent message from {start_node.ip}:{start_node.port} to {node.ip}:{node.port}"
        )
        while not node.message_timestamp:  # Wait for the message to arrive
            if time.time() - start_time > 10:  # Add timeout of 10 seconds
                logger.error(f"Message not received by {node.ip}:{node.port}")
                break
        if node.message_timestamp:
            logger.info(f"Message received by {node.ip}:{node.port}")
            if 0 in node.message_timestamp:
                # Remove the message from the node's message queue
                node.message_timestamp.pop(0)
            else:
                logger.error(
                    f"Key 0 not found in message_timestamp for {node.ip}:{node.port}"
                )
            end_time = time.time()

            # Calculate traversal time
            traversal_time = end_time - start_time
            logger.info(f"Traversal time: {traversal_time:.6f}s")
            break  # Exit the loop once we get the traversal time

        # Return traversal time if it is not zero
        if traversal_time > 0:
            return traversal_time

    # Return traversal time even if it is zero
    return traversal_time


def run():
    # Configure logging
    logging.basicConfig(filename="main.log", level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Create network
    num_nodes = config.NUM_NODES
    network = create_network(num_nodes)

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

    # Create nodes and start threads
    nodes, threads = start_nodes(network)

    # Connect nodes
    connect_peers(nodes, logger)

    # Send message and measure traversal time
    message = "Hello world!"
    start_time = time.time()
    traversal_time = send_messages(nodes, message, logger, start_time)
    print(f'\nTraversal time: {traversal_time:.4f}s\n')

    # Stop the program if the traversal time is not zero
    if traversal_time :
        logging.shutdown()
        for node in nodes:
            node.socket.close()
        sys.exit()


if __name__ == "__main__":
    run()
