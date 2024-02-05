import random
from src.Player import Player
from src.BOT import bot
class Jeux:

    def __init__(self, nb_player: int, nb_bots: int, server : object):
        self.__joueur_mort = []
        self.__sauve = True
        self.__poison = True
        self.__name_role = {} # dico p0->loup p1->voyante...
        self.__vote = {}
        self.__loups_villageois = [] #list nombre de loup puis nombre de villageois
        self.__bots = {}
        self.__name_bots = {}
        self.__nb_bots = nb_bots
        self.__player = self.create_game_player(nb_player, nb_bots)
        self.__server = server



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

    def condition_sorciere(self, players) -> str:

        client_socket = self.__server.get_client_player()
        client_socket = client_socket[players.get_name()]

        if self.__poison and self.__sauve:
            self.__server.personal_messages(players.get_name() + " <--> Le joueur mort est : " + self.__joueur_mort[-1].get_name() + "\n", players.get_name())
            print("Le joueur mort est : " + self.__joueur_mort[-1].get_name())
            self.__server.personal_messages(players.get_name() + " <--> Vous pouvez choisir 'poison' ou 'sauve'\n Entrez votre choix: ", players.get_name())
            print("Vous pouvez choisir 'poison' ou 'sauve'. Entrez votre choix: ")
            choix = self.__server.get_messages(client_socket)
            while choix == None:
                choix = self.__server.get_messages(client_socket)

        elif self.__poison:
            self.__server.personal_messages(players.get_name() + " <--> Vous pouvez choisir 'poison' ou ne rien faire \n Entrez votre choix: ", players.get_name())
            print("Vous pouvez choisir 'poison' ou ne rien faire. Entrez votre choix: ")
            choix = self.__server.get_messages(client_socket)
            while choix == None:
                choix = self.__server.get_messages(client_socket)

        elif self.__sauve:
            self.__server.personal_messages(players.get_name() + " <--> Le joueur mort est : " + self.__joueur_mort[-1].get_name() + "\n",players.get_name())
            print("Le joueur mort est : " + self.__joueur_mort[-1].get_name())
            self.__server.personal_messages(players.get_name() + " <--> Vous pouvez choisir 'sauve' ou ne rien \n. Entrez votre choix: ",players.get_name())
            print("Vous pouvez choisir 'sauve' ou ne rien . Entrez votre choix: ")
            choix = self.__server.get_messages(client_socket)
            while choix == None:
                choix = self.__server.get_messages(client_socket)
        else:
            choix = None
        return choix

    def is_alive(self):
        liste_player_alive = []
        for player in self.__player:
            if player.get_is_alive() == 1:
                liste_player_alive.append(player.get_name())
        return liste_player_alive

    def vote_verif(self, client_socket, player):
        while 1:
            name = None
            while name == None:
                name = self.__server.get_messages(client_socket)
            for players in self.__player:
                if players.get_name() == name and players.get_is_alive() == 1:
                    print("Vous avez voté contre : " + name)
                    return players

            self.__server.personal_messages("Ce joueur est inexistant ou déjà mort, recommencer", player)
            print("Ce joueur est inexistant ou déjà mort, recommencer")
            self.__server.set_messages()


    def sorciere(self,players) -> None:  # un bouton sauve avec une fonction qui verifie que sauve est true et un bouton qui affiche nom_joueur mort et Yes
        if self.__name_bots[players.get_name()] == "bot":
            liste = []
            if self.__poison:
                liste.append("poison")
            if self.__sauve:
                liste.append("sauve")
            liste.append("rien")
            choix = random.choice(liste)
        else:
            choix = self.condition_sorciere(players)

        if choix == "sauve" and self.__sauve == True:
            self.__sauve = False
            name = int(self.__joueur_mort[-1].get_name()[1])
            self.__player[name].set_is_alive(1)
            if self.__name_bots[players.get_name()] == "bot":
                self.__bots[players.get_name()].set_choix_gentil(self.__joueur_mort[-1].get_name())
            del (self.__joueur_mort[-1])
        if choix == "poison" and self.__poison == True:
            self.__poison = False
            if self.__name_bots[players.get_name()] != "bot":
                client_socket = self.__server.get_client_player()
                client_socket = client_socket[players.get_name()]
                self.__server.personal_messages(players.vote(self.get_players()), players.get_name())
                dead_player = self.vote_verif(client_socket, players.get_name())
            else:
                liste = []
                for others in self.get_players():
                    if others.get_role() != 'sorciere' and others.get_is_alive() == 1:
                        liste.append(others)
                dead_player = random.choice(liste)
            self.kill(dead_player)

    def create_game_player(self, nb_player: int, nb_bots: int) -> object:
        ordre_role = ["loups", "voyante", "chasseur", "sorciere", "voleur", "villageois"]
        DICO_NBJOUEURS = {7: (2, 1, 1, 1, 0, 2), 8: (2, 1, 1, 1, 0, 3), 9: (2, 1, 1, 1, 1, 3),
                                 10: (2, 1, 1, 1, 1, 4),11: (2, 1, 1, 1, 1, 5), 12: (2, 1, 2, 1, 1, 5),
                                 13: (3, 1, 1, 1, 1, 6),14: (3, 1, 1, 1, 1, 7), 15: (3, 1, 1, 1, 1, 8),
                                 16: (3, 1, 2, 1, 1, 8)}
        result = []
        liste_player = []
        liste_role = []
        nb_total = nb_player + nb_bots
        for key, value in DICO_NBJOUEURS.items():
            if key == nb_total:
                self.__loups_villageois.append(DICO_NBJOUEURS[key][0])
                self.__loups_villageois.append(nb_total-DICO_NBJOUEURS[key][0])
                for i in range(nb_player):
                    #creation des noms des joueurs
                    liste_player.append("p"+str(i))
                    self.__name_bots["p" + str(i)] = "joueur"
                if nb_bots != 0:
                    for bots in range(len(liste_player), len(liste_player) + nb_bots + 1):
                        liste_player.append("p"+ str(bots))
                        self.__bots["p"+str(bots)] = bot("p"+str(bots))
                        self.__name_bots["p"+str(bots)] = "bot"
                for elt in range(len(value)):
                    #cree une liste avec tous les roles et nombre d'apparition
                    liste_role.extend([ordre_role[elt]] * value[elt])

                for elt in range(len(liste_role)):
                    #attribution des roles aleatoirement
                    random_role = random.choice(liste_role)
                    liste_role.remove(random_role)
                    obj = Player(liste_player[elt], random_role)
                    self.__name_role[obj] = random_role
                    if self.__name_bots[liste_player[elt]] == "bot":
                        self.__bots[liste_player[elt]].set_role(random_role)
                    result.append(obj)
        print(self.__loups_villageois)
        return result

    def game(self):

        for players in self.get_players():
            self.__server.personal_messages("\n" + "Meneur <--> " + players.get_name() + " tu as le rôle de : " + players.get_role() + "\n", players.get_name())
            print(players.get_name() + " a le role de : " + players.get_role())

        self.__server.broadcast_message('Meneur <--> le village s endort \n')
        print('le village s endort')

# ------------------------------------------------------Voyante------------------------------------------------------------------

        for players in self.get_players() :
            if players.get_role() == 'voyante' and players.get_is_alive() == 1:
                self.__server.broadcast_message('Meneur <--> La voyante se réveillent, se reconnaissent et désignent une nouvelle victime !!!\n')
                print('la Voyante se réveille, et désigne un joueur dont elle veut sonder la véritable personnalité !')
                if self.__name_bots[players.get_name()] == "bot":
                    liste = []
                    for others in self.get_players():
                        if others.get_role() != 'voyante' and others.get_is_alive() == 1:
                            liste.append(others)
                    joueur_choisi = random.choice(liste)
                    print(players.get_name() + " <--> a choisi " + joueur_choisi.get_name() + " qui est : " + joueur_choisi.get_role())
                    if joueur_choisi.get_role() == "loups":
                        self.__bots[players.get_name()].set_choix_mechants(joueur_choisi.get_name())
                    else:
                        self.__bots[players.get_name()].set_choix_gentil(joueur_choisi.get_name())

                else:
                    client_socket = self.__server.get_client_player()
                    client_socket = client_socket[players.get_name()]
                    self.__server.personal_messages(players.vote(self.get_players()), players.get_name())
                    player_x = self.vote_verif(client_socket, players.get_name())
                    self.__server.personal_messages(players.get_name() + ' <--> le role de '+ player_x.get_name() +' est ' + player_x.get_role(), players.get_name())
                    print('le role de '+ player_x.get_name() +' est ' + player_x.get_role())
                    print('la voyante se rendort')
                    self.__server.broadcast_message('Meneur <--> La voyante se rendort \n')
            else:
                self.__server.personal_messages('\n<---------------------------------------VOUS DORMEZ zzzzzzzz----------------------------->' + "\n", players.get_name())
#----------------------------------------------Loup------------------------------------------------------------------

        for players in self.get_players() :
            if players.get_role() == 'loups' and players.get_is_alive() == 1:
                if self.__name_bots[players.get_name()] == "bot":
                    for others in self.get_players():
                        liste = []
                        if others.get_role() != 'loups' and others.get_is_alive() == 1:
                            liste.append(others)
                    print(liste)
                    joueur_choisi = random.choice(liste)
                    self.set_vote(joueur_choisi)
                else:
                    self.__server.broadcast_message('Meneur <--> Les Loups-Garous se réveillent, se reconnaissent et désignent une nouvelle victime !!!')
                    print('les Loups-Garous se réveillent, se reconnaissent et désignent une nouvelle victime !!!')
                    for partenaire in self.get_players():
                        if partenaire.get_role() == "loups" and players.get_name() != partenaire.get_name():
                            self.__server.personal_messages("\n" + players.get_name() + " <--> l autre joueur qui est loups avec vous est : " + partenaire.get_name() + "\n", players.get_name())
                    client_socket = self.__server.get_client_player()
                    client_socket = client_socket[players.get_name()]
                    self.__server.personal_messages(players.vote(self.get_players()), players.get_name())
                    player_x = self.vote_verif(client_socket, players.get_name())
                    self.__server.personal_messages(players.get_name() + " <--> vous avez voté : " + player_x.get_name(), players.get_name())
                    self.set_vote(player_x)
            else:
                self.__server.personal_messages('\n<---------------------------------------VOUS DORMEZ zzzzzzzz----------------------------->' + "\n", players.get_name())
        self.kill(max(self.get_vote(), key=self.get_vote().get))
        self.empty_vote()
        self.__server.broadcast_message("Meneur <--> Les loups se rendorment \n")
        print('les loups se rendorment')

#---------------------------------------------------------------Voleur------------------------------------------------------------------

        for players in self.get_players() :
            if players.get_role() == 'voleur' and players.get_is_alive() == 1:
                if self.__name_bots[players.get_name()] == "bot":
                    for others in self.get_players():
                        liste = []
                        if others.get_role() != 'voleur' and others.get_is_alive() == 1:
                            liste.append(others)
                    joueur_choisi = random.choice(liste)
                    role_player_designe = joueur_choisi.get_role()
                    print(players.get_name()+ " est devenue " + role_player_designe)
                    players.set_role(role_player_designe)
                    joueur_choisi.set_role("voleur")
                    self.__bots[players.get_name()].set_role(role_player_designe)
                    if self.__name_bots[joueur_choisi.get_name()] == "bot":
                        self.__bots[joueur_choisi.get_name()].set_role(role_player_designe)
                    break
                else:
                    self.__server.broadcast_message("Meneur <--> Le voleur se reveille et designe un joueur\n")
                    print('le voleur se reveille et designe un joueur\n')
                    client_socket = self.__server.get_client_player()
                    client_socket = client_socket[players.get_name()]
                    self.__server.personal_messages(players.vote(self.get_players()), players.get_name())
                    player_x = self.vote_verif(client_socket, players.get_name())
                    role_player_designe = player_x.get_role() #recupère le role du joueur designe
                    self.__server.personal_messages(players.get_name()+ " est devenue " +role_player_designe, players.get_name())
                    print(players.get_name()+ " est devenue " +role_player_designe)
                    players.set_role(role_player_designe) #modifier le role du joueur designe
                    player_x.set_role("voleur")#modifier le role du voleur
                    break
            else:
                self.__server.personal_messages('\n<---------------------------------------VOUS DORMEZ zzzzzzzz----------------------------->' + "\n",players.get_name())

#----------------------------------------------Sorciere------------------------------------------------------------------


        for players in self.get_players() :
            if players.get_role() == 'sorciere' and players.get_is_alive() == 1:
                self.__server.broadcast_message("Meneur <--> La sorciere se reveille\n")
                self.sorciere(players)
            else:
                self.__server.personal_messages('<---------------------------------------VOUS DORMEZ zzzzzzzz----------------------------->' + "\n",players.get_name())

#----------------------------------------------Jour------------------------------------------------------------------
        if self.finish() == 1:
            return 1
        self.__server.set_messages()
        self.__server.broadcast_message("Meneur <--> C’est le matin, le village se réveille\n")
        print("C’est le matin, le village se réveille")
        if not self.__joueur_mort:
            self.__server.broadcast_message("Meneur <--> Il n'y a pas eu de mort\n")
            print("Il n'y a pas eu de mort.")
        else:
            for joueur in self.__joueur_mort:
                self.__server.broadcast_message("Meneur <--> Le joueur " + joueur.get_name() + " est mort, il etait " + joueur.get_role() + "\n")
                self.__server.personal_messages("------------------------------------------TU ES MORT--------------------------------------------\n", joueur.get_name())
                print("le joueur " + joueur.get_name() + " est mort, il etait "+joueur.get_role())
                if joueur.get_role() == 'chasseur':
                    if self.__name_bots[joueur.get_name()] == "bot":
                        for others in self.get_players():
                            liste = []
                            if others.get_role() != 'chasseur' and others.get_is_alive() == 1:
                                liste.append(others)
                        joueur_choisi = random.choice(liste)
                        print(joueur_choisi.get_name() + " est tué par le chasseur")
                        self.kill(joueur_choisi)
                    else:
                        client_socket = self.__server.get_client_player()
                        client_socket = client_socket[joueur.get_name()]
                        self.__server.personal_messages(joueur.vote(self.get_players()), joueur.get_name())
                        victime_chasseur = self.vote_verif(client_socket, joueur.get_name())
                        self.kill(victime_chasseur)
            self.empty_joueur_mort()
        if self.finish() == 1:
            return 1
        self.__server.broadcast_message("Meneur <--> Les joueurs doivent éliminer un joueur suspecté d’être un Loup-Garou\n")
        print("Les joueurs doivent éliminer un joueur suspecté d’être un Loup-Garou\n")
        for players in self.get_players():
            if players.get_is_alive() == 1:
                if self.__name_bots[joueur.get_name()] == "bot":
                    for others in self.get_players():
                        liste = []
                        if others.get_role() != 'chasseur' and others.get_is_alive() == 1:
                            liste.append(others)
                    for elt in liste:
                        if self.__bots.get_choix_nice() == elt.get_name() and self.__bots.get_choix_nice() != None:
                            del (liste[elt])
                        if self.__bots.get_choix_mechants() == elt.get_name() and self.__bots.get_choix_nice() != None:
                            liste = []
                            liste.append(elt)
                    print(liste)
                    joueur_choisi = random.choice(liste)
                    print(players.get_name() + " a voté pour " + joueur_choisi.get_name())
                    self.set_vote(joueur_choisi)
                else:
                    client_socket = self.__server.get_client_player()
                    client_socket = client_socket[players.get_name()]
                    self.__server.personal_messages(players.vote(self.get_players()), players.get_name())
                    accuse = self.vote_verif(client_socket, players.get_name())
                    self.__server.personal_messages(players.get_name() + " <--> vous avez voté : " + accuse.get_name(), players.get_name())
                    self.set_vote(accuse)
        joueur_mort_vote = max(self.get_vote(), key=self.get_vote().get)
        self.kill(joueur_mort_vote)
        self.empty_joueur_mort()
        self.__server.broadcast_message("Meneur <--> Le joueur " + joueur_mort_vote.get_name() + " est mort, il etait " + joueur_mort_vote.get_role()+ "\n")
        self.__server.personal_messages("\n" + joueur_mort_vote.get_name() + " <--> vous etes mort suite à la majorité des votes \n",joueur_mort_vote.get_name())
        self.__server.personal_messages("-----------------------------------------TU ES MORT-------------------------------------------\n",joueur.get_name())
        print("le joueur " + joueur_mort_vote.get_name() + " est mort, il etait " + joueur_mort_vote.get_role())
        self.empty_vote()
        self.__server.set_messages()
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
            self.__server.broadcast_message("\n Meneur <--> Les villageois ont gagné Youpiii")
            print("Les villageois ont gagné")
            return 1
        if villageois_mort == self.__loups_villageois[1]:
            self.__server.broadcast_message("\n Meneur <--> Les loups ont gagné Bouhhhh")
            print("Les loups ont gagné")
            return 1
        return 0