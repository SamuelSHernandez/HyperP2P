import logging
import socket
import threading
import time

# Configure logging
logging.basicConfig(filename="p2p.log", level=logging.INFO)
logger = logging.getLogger(__name__)


class Discovery:
    def __init__(self, node, socket):
        self.node = node
        self.socket = socket
        self.threads = []

    def start(self):
        logger.info(f"Discovery service started on {self.node.ip}:{self.node.port}")
        while True:
            client_socket, address = self.socket.accept()
            logger.info(f"Connected to {address[0]}:{address[1]}")
            t = threading.Thread(target=self.handle_connection, args=(client_socket,))
            self.threads.append(t)
            t.start()

    def handle_connection(self, client_socket):
        data = client_socket.recv(1024).decode().strip()
        if data.startswith("CONNECT"):
            ip, port = data.split()[1:]
            self.node.connect(ip, int(port))
        client_socket.close()


class Peer:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.name = f"{ip}:{port}"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.peers = []
        self.message_timestamp = {}
        self.messages_sent = 0
        self.messages_received = 0
        self.lock = threading.Lock()

    def start(self):
        try:
            self.socket.bind((self.ip, self.port))
            self.socket.listen()
        except OSError as e:
            logger.error(f"Error starting node on {self.ip}:{self.port}: {e}")
            return

        logger.info(f"Node on {self.ip}:{self.port}")

        while True:
            client_socket, address = self.socket.accept()
            logger.info(f"Connected to {address[0]}:{address[1]}")

            t = threading.Thread(target=self.handle_connection, args=(client_socket,))
            t.start()

    def handle_connection(self, client_socket: socket.socket):
        data = client_socket.recv(1024).decode().strip()
        if data.startswith("CONNECT"):
            ip, port = data.split()[1:]
            self.connect(ip, int(port))
        elif data.startswith("MESSAGE"):
            self._handle_message(data)
        client_socket.close()

    def _handle_message(self, data: str):
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
                    start_time = time.time()
                    peer_socket.sendall(message_with_timestamp.encode())
                    end_time = time.time()
                    delay = end_time - start_time
                    throughput = self.get_throughput(message)
                    logger.info(
                        f"timestamp={received_timestamp} - sent message to {peer}. metrics={self.get_metrics()}"
                    )
                    self.messages_sent += 1
                    if message not in self.message_timestamp:
                        self.message_timestamp[message] = []
                    self.message_timestamp[message].append((peer, end_time))
                except OSError as e:
                    logger.error(f"Error connecting to peer {peer}: {e}")
                except AttributeError:
                    logger.error(f"Error closing peer socket: {peer_socket} is None")
                finally:
                    if peer_socket is not None:
                        peer_socket.close()
        self.messages_received += 1
