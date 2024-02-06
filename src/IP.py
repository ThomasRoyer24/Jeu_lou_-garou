import socket
import os
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
        #self.add_to_gitignore()
        self.update_github_file(file_path)

    def update_github_file(self, file_path):
        # Récupérer le répertoire du script
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Remonter d'un niveau pour obtenir le répertoire parent
        parent_dir = os.path.dirname(script_dir)

        # Remonter d'un niveau supplémentaire
        grandparent_dir = os.path.dirname(parent_dir)

        # Construire le chemin complet vers le répertoire souhaité
        api_url = os.path.join(grandparent_dir, "Jeu_lou_-garou")

        repo = Repo(api_url)

        dest_path = os.path.join(api_url, file_path)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        os.replace(file_path, dest_path)

        if repo.is_dirty():
            repo.git.add("--all")

            # Effectuer le commit
            repo.git.commit(m="MAJ fichier master_ip")

            # Pousser les modifications vers GitHub
            repo.git.push('origin', "main")



