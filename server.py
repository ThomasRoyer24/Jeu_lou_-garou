import socket
import threading
from main import main
from Jeux import Jeux
class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        self.game = None
        self.clients = []

    def handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                print(f"Received from client {client_socket.getpeername()}: {message}")
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client_socket.close()

    def accept_clients(self):
        while True:
            client_socket, addr = self.server.accept()
            print(f"Accepted connection from {addr}")
            self.clients.append(client_socket)
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

    def start_game(self, nb_players):
        self.game = main()
        jeux = Jeux(int(input("Nombre de joueur: ")))
        while jeux.game() != 1:
            pass
        exit()
        self.game.create_game_player(nb_players)
        self.game_thread = threading.Thread(target=self.game_loop)
        self.game_thread.start()

    def game_loop(self):
        while not self.game.finish():
            self.game.game()

    def broadcast_message(self, message):
        for client in self.clients:
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error sending message to client: {e}")

def main():
    server = Server("localhost", 12800)
    print(f"Server is listening on {server.host}:{server.port}")

    accept_thread = threading.Thread(target=server.accept_clients)
    accept_thread.start()

    nb_players = 8  # Specify the number of players
    server.start_game(nb_players)

    accept_thread.join()
    server.game_thread.join()

if __name__ == "__main__":
    main()
