from src.server import activation
from src.IP import ip_adress


if __name__ == "__main__":
    # Utilisation de la fonction pour obtenir l'adresse IP
    appele_classe = ip_adress()
    ip_address = appele_classe.ecrit_ip()

    activation()