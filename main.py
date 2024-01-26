from src.Jeux import Jeux

def main():
    jeux = Jeux(int(input("Nombre de joueur: ")))
    while jeux.game() != 1:
        pass
    exit()
main()