from main import Main

class sorciere:
    def __init__(self, choix : list):
        self.__joueur_mort_nuit = Main().get_joueur_mort_nuit() #nom du joueur
        self.__choix = choix[0]
        self.__biblio = ["Ressuscite","Tue","Rien"]
        
    def choix(self):
        if self.__choix == self.__biblio[0]:
            print("Sorciere a décidé de : " + self.__choix)



