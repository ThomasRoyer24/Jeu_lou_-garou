class bot:
    def __init__(self, player_name: str):
        self.player_name = player_name
        self.role = None
        self.choix_mechants = None
        self.choix_gentil = None

    def get_name(self):
        return self.player_name

    def get_role(self):
        return self.role

    def set_role(self, new_role):
        self.role = new_role

    def get_choix_nice(self):
        return self.choix_gentil

    def get_choix_mechants(self):
        return self.choix_mechants
    def choix_mechants(self, name):
        self.choix = name

    def choix_gentil(self, name):
        self.choix_gentil = name
