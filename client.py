import base64
import socket
import threading
import os
class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()
        print("Vous êtes connecté au serveur")

        try:
            while True:
                message = input()
                self.client.send(message.encode('utf-8'))
        except KeyboardInterrupt:
            print("Déconnexion du client.")


    def receive_messages(self):
        while True:
            try:
                data = self.client.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                print(message)
            except Exception as e:
                print(f"Error receiving message from servers: {e}")
                break



import requests

def get_github_file_content():
    # Construire l'URL de l'API GitHub pour obtenir le contenu du fichier
    api_url = "https://raw.githubusercontent.com/ThomasRoyer24/Jeu_lou_garou/main/src/master_ip.txt"

    # Faire une requête GET à l'API GitHub
    response = requests.get(api_url)

    # Vérifier si la requête a réussi (code 200)
    if response.status_code == 200:
        # Récupérer le contenu du fichier
        content = response.text
        print(content)

        return content
    else:
        # Afficher un message d'erreur si la requête a échoué
        print(f"Erreur lors de la récupération du fichier : {response.status_code}")
        return None



def main():
    print(get_github_file_content())
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "src", "master_ip.txt")
    server_ip = open(file_path, "r").read().strip()
    Client(server_ip, 8080)

if __name__ == "__main__":
    main()