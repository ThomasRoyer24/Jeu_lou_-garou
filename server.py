import socket
import threading
from src.Jeux import Jeux

class Server:

    def __init__(self, host, port, nb_player):
        self.nb_players = nb_player
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        self.game = None
        self.clients = []
        self.messages = {}  # Shared list for messages
        self.clients_player = {}

    def handle_client(self, client_socket):
        try:
            while True:
                # Réception de la réponse du client
                user_input = client_socket.recv(1024).decode('utf-8')
                print(user_input)
                self.messages[client_socket] = user_input
        except Exception as e:
            print(f"Error handling client: {e}")

    def set_messages(self):
        for key in self.messages.keys():
            self.messages[key] = None
    def get_messages(self, client_socket):
        return self.messages[client_socket]
    def accept_clients(self):
        while len(self.clients) < self.nb_players:
            client_socket, addr = self.server.accept()
            print(f"Accepted connection from {addr}")
            self.clients.append(client_socket)
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

        for elt in range(len(self.clients)):
            self.clients_player["p" + str(elt)] = self.clients[elt]
            self.messages[self.clients[elt]] = None
        print(self.clients_player)

    def start_game(self, server):
        if len(self.clients) == self.nb_players:
            self.game = Jeux(self.nb_players, server)
            self.game.create_game_player(self.nb_players)
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

    def personal_messages(self, message, player):
        for key, value in self.clients_player.items():
            if key == player:
                try:
                    value.send(message.encode('utf-8'))
                except Exception as e:
                    print(f"Error sending message to client: {e}")

    def clear_messages(self):
        self.messages = []

    def get_client_player(self):
        return self.clients_player

def main():
    nb_players = int(input("Number of players: "))  # Specify the number of players
    server = Server("0.0.0.0", 8080, nb_players)
    print(f"Server is listening on {server.host}:{server.port}")

    accept_thread = threading.Thread(target=server.accept_clients)
    accept_thread.start()
    accept_thread.join()

    # Une fois que le nombre requis de joueurs est atteint, commencez le jeu
    server.start_game(server)
    server.game_thread.join()

if __name__ == "__main__":
    main()
