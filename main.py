class Main:
    def __init__(self):
        self.__joueur_mort_nuit = []

    def get_joueur_mort_nuit(self):
        return self.__joueur_mort_nuit

    def set_joueur_mort_nuit(self, new_joueur : list) -> None:
        self.__joueur_mort_nuit = new_joueur