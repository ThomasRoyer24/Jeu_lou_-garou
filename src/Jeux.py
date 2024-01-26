import random
from src.Player import Player


class Jeux:

    def __init__(self, nb_player: int):
        self.__joueur_mort = []
        self.__sauve = True
        self.__poison = True
        self.__name_role = {} # dico p0->loup p1->voyante...
        self.__vote = {}
        self.__loups_villageois = [] #list nombre de loup puis nombre de villageois
        self.__player = self.create_game_player(nb_player)

    def get_joueur_mort(self):
        return self.__joueur_mort

    def add_joueur_mort(self,player) -> None:
        self.__joueur_mort.append(player)

    def get_players(self) -> Player:
        return self.__player

    def set_vote(self,player):
        if player in self.get_vote():
            self.get_vote()[player] += 1
        else:
            self.get_vote()[player] = 1

    def get_vote(self):
        return self.__vote

    def empty_vote(self) -> None:
        self.__vote= {}

    def empty_joueur_mort(self):
        self.__joueur_mort = []

    def kill(self, player):
        player.set_is_alive(0)
        self.add_joueur_mort(player)

    def condition_sorciere(self) -> str:
        if self.__poison and self.__sauve:
            print("Le joueur mort est : " + self.__joueur_mort[-1].get_name())
            choix = input("Vous pouvez choisir 'poison' ou 'sauve'. Entrez votre choix: ")

        elif self.__poison:
            choix = input("Vous pouvez choisir 'poison' ou ne rien faire. Entrez votre choix: ")

        elif self.__sauve:
            choix = input("Vous pouvez choisir 'sauve' ou ne rien . Entrez votre choix: ")
            print("Le joueur mort est : " + self.__joueur_mort[-1].get_name())
        else:
            choix = None
        return choix

    def is_alive(self):
        liste_player_alive = []
        for player in self.__player:
            if player.get_is_alive() == 1:
                liste_player_alive.append(player.get_name())
        print(liste_player_alive)
        return liste_player_alive

    def sorciere(
            self,player) -> None:  # un bouton sauve avec une fonction qui verifie que sauve est true et un bouton qui affiche nom_joueur mort et Yes

        choix = self.condition_sorciere()
        if choix == "sauve" and self.__sauve == True:
            self.__sauve = False
            name = int(self.__joueur_mort[-1].get_name()[1])
            self.__player[name].set_is_alive(1)
            del (self.__joueur_mort[-1])
        if choix == "poison" and self.__poison == True:
            self.__poison = False
            dead_player = player.vote(self.get_players())
            self.kill(dead_player)

            # self.__joueur_mort.append(vote)

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
                self.__loups_villageois.append(DICO_NBJOUEURS[key][0])
                self.__loups_villageois.append(nb_player-DICO_NBJOUEURS[key][0])

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

        for players in self.get_players() :
            if players.get_role() == 'voyante' and players.get_is_alive() == 1:
                print('la Voyante se réveille, et désigne un joueur dont elle veut sonder la véritable personnalité !')
                player_x = players.vote(self.get_players())
                print('le role de '+ player_x.get_name() +' est ' + player_x.get_role())
                print('la voyante se rendo')

#----------------------------------------------Loup------------------------------------------------------------------

        print('les Loups-Garous se réveillent, se reconnaissent et désignent une nouvelle victime !!!')
        for players in self.get_players() :
            if players.get_role() == 'loups' and players.get_is_alive() == 1:
                self.set_vote(players.vote(self.get_players()))
        self.kill(max(self.get_vote(), key=self.get_vote().get))
        self.empty_vote()
        print('les loups se rendorme')

#----------------------------------------------Voleur------------------------------------------------------------------

        for players in self.get_players() :
            if players.get_role() == 'voleur' and players.get_is_alive() == 1:
                print('le voleur se reveille et designe un joueur')
                player_x = players.vote()
                role_player_designe = player_x.get_role() #recupère le role du joueur designe
                players.set_role(role_player_designe) #modifier le role du joueur designe
                player_x.set_role("voleur")#modifier le role du voleur

#----------------------------------------------Sorciere------------------------------------------------------------------

        for players in self.get_players() :
            if players.get_role() == 'sorciere' and players.get_is_alive() == 1:
                self.sorciere(players)

#----------------------------------------------Jour------------------------------------------------------------------
        if self.finish() == 1:
            return 1

        print("C’est le matin, le village se réveille,")
        if not self.__joueur_mort:
            print("Il n'y a pas eu de mort.")
        else:
            stats_morts = {}
            for joueur in self.__joueur_mort:
                print("le joueur " + joueur.get_name() + " est mort, il etait "+joueur.get_role())
                if joueur.get_role() == 'chasseur':
                    victime_chasseur = joueur.vote(self.get_players())
                    self.kill(victime_chasseur)
            self.empty_joueur_mort()

        print("Les joueurs doivent éliminer un joueur suspecté d’être un Loup-Garou")
        for players in self.get_players():
            if players.get_is_alive() == 1:
                self.set_vote(players.vote(self.get_players()))
        joueur_mort_vote = max(self.get_vote(), key=self.get_vote().get)
        self.kill(joueur_mort_vote)
        self.empty_joueur_mort()
        print("le joueur " + joueur_mort_vote.get_name() + " est mort, il etait " + joueur_mort_vote.get_role())
        self.empty_vote()

        if self.finish() == 1:
            return 1


    def finish(self):
        loups_mort = 0
        villageois_mort = 0
        for players in self.get_players() :
            if players.get_role() != 'loups' and players.get_is_alive() == 0:
                villageois_mort +=1
            if players.get_role() == 'loups' and players.get_is_alive() == 0:
                loups_mort +=1

        if loups_mort == self.__loups_villageois[0]:
            print("Les villageois on gagné")
            return 1
        if villageois_mort == self.__loups_villageois[1]:
            print("Les loups on gagné")
            return 1
        return 0
