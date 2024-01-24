class Main:
    def __init__(self, nom_joueurs: list):
        self.__joueur_mort = []
        self.__sauve = True
        self.__poison = True

    def get_joueur_mort(self):
        return self.__joueur_mort
    def sorciere(self, choix : str): #un bouton sauve avec une fonction qui verifie que sauve est true et un bouton qui affiche nom_joueur mort et Yes
        if choix == "Sauve":
            self.__sauve = False
            print("Le joueur mort est : " + self.__joueur_mort[-1])
            del(self.__joueur_mort[-1])
        if choix == "Poison":
            self.__poison = False
            vote = "nom_du_joueur"
            self.__joueur_mort.append(vote)

