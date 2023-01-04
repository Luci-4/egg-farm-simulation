class EggFarmState:
    def __init__(self, initial_eggs: int, initial_chickens: int) -> None:
        self.__initial_eggs = initial_eggs
        self.__initial_chickens = initial_chickens
        self.__eggs = initial_eggs
        self.__chickens = initial_chickens

    @property
    def eggs(self):
        return self.__eggs
    
    @property
    def chickens(self):
        return self.__chickens

    def reset_to_initial_values(self):
        self.__eggs = self.__initial_eggs
        self.__chickens = self.__initial_chickens

    def add_eggs(self, new_eggs: int) -> None:
        self.__eggs += new_eggs

    def add_chickens(self, new_chickens: int) -> None:
        self.__chickens += new_chickens

