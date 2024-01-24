from main import Main

class sorciere:
    def __init__(self, choix):
        self.joueur_mort_nuit = Main().get_joueur_mort_nuit() #nom du joueur
        self.choix = choix
        self.dico = {"Vie":1, "Mort":-1, "Neutre":0}
        
    def choix(self):
        pass
        


