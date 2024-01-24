from src.Player import Player
import random
class Main:
    def __init__(self, nb_player: int):
        self.__joueur_mort = []
        self.__sauve = True
        self.__poison = True
        self.__DICO_NBJOUEURS = {7: (2, 1, 1, 1, 0, 2), 8: (2, 1, 1, 1, 0, 3), 9: (2, 1, 1, 1, 1, 3),
                                 10: (2, 1, 1, 1, 1, 4),11: (2, 1, 1, 1, 1, 5), 12: (2, 1, 2, 1, 1, 5),
                                 13: (3, 1, 1, 1, 1, 6),14: (3, 1, 1, 1, 1, 7), 15: (3, 1, 1, 1, 1, 8),
                                 16: (3, 1, 2, 1, 1, 8)}
        self.__ordre_role = ["loups","voyante","chasseur","sorciere","voleur","villageois"]
        self.__name_role = {}
        self.__player = self.create_game_player(nb_player)

    def get_joueur_mort(self):
        return self.__joueur_mort

    def get_data(self):
        return self.__player
    def sorciere(self, choix : str) -> None: #un bouton sauve avec une fonction qui verifie que sauve est true et un bouton qui affiche nom_joueur mort et Yes
        self.__joueur_mort.append("p1")
        for key, value in self.__name_role.items():
            if value == "sorciere":
                sorciere = key
        liste_player_alive = []
        for player in self.__player:
            if player.get_is_alive() == 1 and player.get_name() != sorciere:
                liste_player_alive.append(player.get_name())
        if choix == "Sauve":
            self.__sauve = False
            print("Le joueur mort est : " + self.__joueur_mort[-1])
            name = int(self.__joueur_mort[-1][1])
            self.__player[name].set_is_alive(1)
            del(self.__joueur_mort[-1])
        if choix == "Poison":
            self.__poison = False
            print("qui veux tu tuer entre: " + str(liste_player_alive) )

            #self.__joueur_mort.append(vote)

    def create_game_player(self, nb_player: int) -> object:
        result = []
        liste_player = []
        liste_role = []
        for key, value in self.__DICO_NBJOUEURS.items():
            if key == nb_player:
                for i in range(nb_player+1):
                    liste_player.append("p"+str(i))
                for elt in range(len(value)):
                    liste_role.extend([self.__ordre_role[elt]] * value[elt])
                for elt in range(len(liste_role)):
                    random_role = random.choice(liste_role)
                    liste_role.remove(random_role)
                    self.__name_role[liste_player[elt]] = random_role
                    result.append(Player(liste_player[elt], random_role))
        return result

call = Main(8)
data = call.get_data()
test = data[0].get_role()

print(data[0].get_name())
print(test)
sor = call.sorciere("Sauve")