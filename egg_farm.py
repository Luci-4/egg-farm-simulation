from probability_context import ProbabilityContext
from egg_farm_state import EggFarmState

class EggFarm:
    def __init__(self, initial_eggs: int, initial_chickens: int, output_fraction: float) -> None:
        self.__state = EggFarmState(initial_eggs, initial_chickens)
        self.output_fraction = output_fraction

    @property
    def output_eggs(self):
        return self.__state.eggs
    
    @property
    def chickens(self):
        return self.__state.chickens

    def reset(self):
        self.__state.reset_to_initial_values()

    def __get_new_output_and_chatching_eggs(self, iteration: int) -> tuple[int, int]:
        new_eggs = self.chickens*int(ProbabilityContext.did_lay_egg(iteration))
        new_output_eggs = int(self.output_fraction*new_eggs)
        new_chatching_eggs = int(new_eggs - new_output_eggs)
        return new_output_eggs, new_chatching_eggs

    def tick(self, iteration: int):
        new_output_eggs, new_chatching_eggs = self.__get_new_output_and_chatching_eggs(iteration)
        new_chickens= sum([int(ProbabilityContext.did_chatch_from_egg()) for _ in range(new_chatching_eggs)])
        self.__state.add_eggs(new_output_eggs)
        self.__state.add_chickens(new_chickens)