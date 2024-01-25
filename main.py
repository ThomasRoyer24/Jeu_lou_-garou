from random import random
from src.Player import Player

class Main:

    def __init__(self, nb_player: int):
        self.__joueur_mort = []
        self.__sauve = True
        self.__poison = True
        self.__name_role = {} # dico p0->loup p1->voyante...
        self.__player = self.create_game_player(nb_player)
        self.__vote = {}

    def get_joueur_mort(self):
        return self.__joueur_mort

    def add_joueur_mort(self,player) -> None:
        self.__joueur_mort.append(player)

    def get_players(self) -> Player:
        return self.__player

    def get_vote(self):
        return self.__vote

    def set_vote(self,name: str) -> None:
        self.__vote[name] +=1

    def kill(self, player):
        player.set_is_alive(0)
        self.add_joueur_mort(player)

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
        ordre_role = ["loups", "voyante", "chasseur", "sorciere", "voleur", "villageois"]
        DICO_NBJOUEURS = {7: (2, 1, 1, 1, 0, 2), 8: (2, 1, 1, 1, 0, 3), 9: (2, 1, 1, 1, 1, 3),
                                 10: (2, 1, 1, 1, 1, 4),11: (2, 1, 1, 1, 1, 5), 12: (2, 1, 2, 1, 1, 5),
                                 13: (3, 1, 1, 1, 1, 6),14: (3, 1, 1, 1, 1, 7), 15: (3, 1, 1, 1, 1, 8),
                                 16: (3, 1, 2, 1, 1, 8)}
        result = []
        liste_player = []
        liste_role = []
        for key, value in DICO_NBJOUEURS.items():
            if key == nb_player:
                for i in range(nb_player+1):
                    #creation des noms des joueurs
                    liste_player.append("p"+str(i))

                for elt in range(len(value)):
                    #cree une liste avec tous les roles et nombre d'apparition
                    liste_role.extend([ordre_role[elt]] * value[elt])

                for elt in range(len(liste_role)):
                    #attribution des roles aleatoirement
                    random_role = random.choice(liste_role)
                    liste_role.remove(random_role)
                    obj = Player(liste_player[elt], random_role)
                    self.__name_role[obj] = random_role
                    result.append(obj)

        return result

    def game(self):

        print('le village s endort')

# ----------------------------------------------Voyante------------------------------------------------------------------

        for players in self.get_players(self) :
            if players.get_role() == 'voyante' and players.get_is_alive() == 1:
                print('la Voyante se réveille, et désigne un joueur dont elle veut sonder la véritable personnalité !')
                player_x = players.vote(self.get_players(self))
                print('le role de '+ player_x.get_name() +' est ' + player_x.get_role())
                print('la voyante se rendo')

#----------------------------------------------Loup------------------------------------------------------------------

        print('lles Loups-Garous se réveillent, se reconnaissent et désignent une nouvelle victime !!!')
        for players in self.get_players(self) :
            if players.get_role() == 'loup' and players.get_is_alive() == 1:
                self.set_vote(self,players.vote())
                self.kill(max(self.get_vote(self), key=self.get_vote(self).get))
        print('les loups se rendorme')

#----------------------------------------------Voleur------------------------------------------------------------------

        for players in self.get_players(self) :
            if players.get_role() == 'voleur' and players.get_is_alive() == 1:
                print('le voleur se reveille et designe un joueur')
                player_x = players.vote()
                role_player_designe = player_x.get_role() #recupère le role du joueur designe
                players.set_role(role_player_designe) #modifier le role du joueur designe
                player_x.set_role("voleur")#modifier le role du voleur





