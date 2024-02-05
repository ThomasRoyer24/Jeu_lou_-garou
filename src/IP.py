import socket

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
        ip_adresse = self.get_ip_address()
        file = open("C:/Users/Blandine/Tp_python_avance/Jeu_lou_-garou/master_ip.txt", "w")
        file.write(ip_adresse)

