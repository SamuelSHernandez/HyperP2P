import logging
import socket
import threading
import time

# Configure logging
logging.basicConfig(filename="p2p.log", level=logging.INFO)
logger = logging.getLogger(__name__)


class Peer:
    def __init__(self, ip, port, peers):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.peers = peers
        self.message_timestamp = {}
        self.messages_sent = 0
        self.messages_received = 0
        self.lock = threading.Lock()
        self.start_time = time.time()

    def start(self):
        try:
            self.socket.bind((self.ip, self.port))
            self.socket.listen()
        except OSError as e:
            logger.error(f"Error starting node on {self.ip}:{self.port}: {e}")
            return

        logger.info(f"Node started on {self.ip}:{self.port}")

        while True:
            client_socket, address = self.socket.accept()
            logger.info(f"Connected to {address[0]}:{address[1]}")

            t = threading.Thread(target=self.handle_connection, args=(client_socket,))
            t.start()

    def handle_connection(self, client_socket):
        data = client_socket.recv(1024).decode().strip()

        if data.startswith("CONNECT"):
            ip, port = data.split()[1:]
            self.connect(ip, int(port))
        elif data.startswith("MESSAGE"):
            self.message(data)
        client_socket.close()

    def message(self, data):
        message = data.split(" ", 1)[1].lstrip("MESSAGE ")
        received_timestamp = float(message.split(",")[-1].split("=")[-1])
        message = message.split(",")[0]
        logger.info(f"timestamp={received_timestamp} - received message")

        with self.lock:
            for peer in self.peers:
                peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    peer_socket.connect(peer)
                    message_with_timestamp = (
                        f"MESSAGE {message}, timestamp={received_timestamp}"
                    )

                    peer_socket.sendall(message_with_timestamp.encode())

                    logger.info(
                        f"timestamp={received_timestamp} - sent message to {peer}. metrics={self.get_metrics()}"
                    )
                    self.message_sent(message, peer)
                except OSError as e:
                    logger.error(f"Error connecting to peer {peer}: {e}")
                except AttributeError:
                    logger.error(f"Error closing peer socket: {peer_socket} is None")
                finally:
                    if peer_socket is not None:
                        peer_socket.close()
        self.messages_received += 1


    def connect(self, ip, port):
        
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self._handle_connection(peer_socket, ip, port)
        except OSError as e:
            logger.error(f"Error connecting to peer {ip}:{port}: {e}")
        finally:
            peer_socket.close()

    def _handle_connection(self, peer_socket, ip, port):
        try:
            peer_socket.connect((ip, port))
        except OSError as e:
            logger.error(f"Error connecting to peer {ip}:{port}: {e}")
            peer_socket.close()
            return

        self.peers.append((ip, port))

        logger.info(f"Connected to peer {ip}:{port}")

        message = f"MESSAGE from {self.ip}:{self.port}, timestamp={time.time()}"
        start_time = time.time()
        peer_socket.sendall(message.encode())
        end_time = time.time()
        delay = end_time - start_time
        logger.info(
            f"timestamp={time.time()} - sent message to {ip}:{port}, delay={delay}"
        )
        self.messages_sent += 1
        if message not in self.message_timestamp:
            self.message_timestamp[message] = []
        self.message_timestamp[message].append(((ip, port), end_time))

    def send_message(self, message):
        timestamp = time.time()

        with self.lock:
            for peer in self.peers:
                peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    peer_socket.connect(peer)

                    message_with_timestamp = f"MESSAGE {message}, timestamp={timestamp}"
                    start_time = time.time()
                    peer_socket.sendall(message_with_timestamp.encode())
                    end_time = time.time()
                    delay = end_time - start_time
                    logger.info(
                        f"Sent message, timestamp={timestamp}, delay={delay} to {peer}"
                    )
                    self.message_sent(message, peer)
                except OSError as e:
                    logger.error(f"Error connecting to peer {peer}: {e}")
                except Exception as e:
                    logger.error(f"Error sending message to peer {peer}: {e}")
                else:
                    logger.info(
                        f"Message '{message}', timestamp={timestamp} sent to {peer}"
                    )
                finally:
                    peer_socket.close()


    def message_sent(self, message, peer):
        self.messages_sent += 1
        if message not in self.message_timestamp:
            self.message_timestamp[message] = []
        self.message_timestamp[message].append((peer))


    def get_metrics(self):
        start_time = time.time()
        recent_messages = {}
        for message, timestamps in self.message_timestamp.items():
            for timestamp in timestamps:
                if timestamp[1] >= start_time:
                    if message not in recent_messages:
                        recent_messages[message] = {"sent": 0, "received": 0}
                    if timestamp[0] == (self.ip, self.port):
                        recent_messages[message]["sent"] += 1
                    else:
                        recent_messages[message]["received"] += 1
        return {
            "ip": self.ip,
            "port": self.port,
            "num_peers": len(self.peers),
            "messages_sent": self.messages_sent,
            "messages_received": self.messages_received,
        }

    def calculate_path_cost(self, path):
        cost = 0
        for i in range(len(path) - 1):
            node1 = path[i]
            node2 = path[i + 1]
            metrics = node1.get_metrics()
            for peer in metrics["peers"]:
                if peer == (node2.ip, node2.port):
                    cost += 1 / metrics["throughput"]
                    break
        return cost

