class bot:
    def __init__(self, player_name: str):
        self.player_name = player_name
        self.role = None

    def get_name(self):
        return self.player_name

    def get_role(self):
        return self.role

    def set_role(self, new_role):
        self.role = new_role
