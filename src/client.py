import socket
import threading
import requests
import json
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




def get_github_file_content():
    # Construire l'URL de l'API GitHub pour obtenir le contenu du fichier
    api_url = "https://github.com/ThomasRoyer24/Jeu_lou_garou/blob/main/src/master_ip.txt"

    # Faire une requête GET à l'API GitHub

    with requests.get(api_url) as response:
        # Vérifier si la requête a réussi (code 200)
        if response.status_code == 200:
            data = json.loads(response.text)

            # Extraire le contenu brut du fichier
            raw_lines = data["payload"]["blob"]["rawLines"]

            return raw_lines[0]
        else:
            # Afficher un message d'erreur si la requête a échoué
            print(f"Erreur lors de la récupération du fichier : {response.status_code}")
            return None



def main_client():
    Client(get_github_file_content(), 8080)

if __name__ == "__main__":
    main_client()