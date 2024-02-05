import socket
import os
import requests
import base64
import git
from git import Repo



class ip_adress():
    def get_ip_address(self):
        try:
            # Créez une connexion à un serveur fictif
            # (le choix de l'adresse 8.8.8.8 est arbitraire, c'est l'adresse IP du serveur DNS public de Google)
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip_address = s.getsockname()[0]
            s.close()
            return ip_address
        except socket.error as e:
            print(f"Erreur lors de la récupération de l'adresse IP : {e}")
            return None

    def ecrit_ip(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "master_ip.txt")
        ip_adresse = self.get_ip_address()
        file = open(file_path, "w")
        file.write(ip_adresse)
        file.close()
        # Mettre à jour le fichier sur GitHub
        self.update_github_file(file_path, ip_adresse)

    def update_github_file(self, file_path, new_text):
        # Construire l'URL de l'API GitHub pour obtenir le contenu du fichier
        api_url =  r"C:\Users\Blandine\Tp_python_avance\Jeu_lou_-garou"

        repo = Repo(api_url)

        dest_path = os.path.join(api_url, file_path)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        os.replace(file_path, dest_path)

        # Ajouter tous les fichiers modifiés pour le commit
        repo.git.add("--all")

        # Effectuer le commit
        repo.git.commit(m="MAJ fichier master_ip")

        # Pousser les modifications vers GitHub
        repo.git.push('origin', "main")



