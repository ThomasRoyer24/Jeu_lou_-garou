import threading
from src.Jeux import Jeux
from server import Server

class Main:
    def __init__(self, nb_players, server):
        self.nb_players = nb_players
        self.server = server
        self.game = None
        self.game_thread = None

    def start_game(self):
        if len(self.server.get_clients()) == self.nb_players:
            self.game = Jeux(self.nb_players, self.server)
            self.game.create_game_player(self.nb_players)
            self.game_thread = threading.Thread(target=self.game_loop)
            self.game_thread.start()

    def game_loop(self):
        while not self.game.finish():
            self.game.game()

def main():
    nb_players = int(input("Nombre de joueur: "))  # Specify the number of players
    server = Server("0.0.0.0", 5555, nb_players)
    print(f"Server is listening on {server.host}:{server.port}")

    init_main = Main(nb_players, server)

    init_main.start_game()
    accept_thread = threading.Thread(target=server.accept_clients)
    accept_thread.start()

    accept_thread.join()
    init_main.game_thread.join()

if __name__ == "__main__":
    main()
