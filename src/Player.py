
class Player:

    def __init__(self, name: str, role: str):
        self.__name = name
        self.__is_alive = 1
        self.__role = role

    def get_is_alive(self) -> int:
        return self.__is_alive

    def set_is_alive(self, value: int) -> None:
        self.__is_alive = value

    def get_role(self) -> str:
        return self.__role

    def set_role(self, value: str) -> None:
        self.__role = value

    def vote(self):
        return input()