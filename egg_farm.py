from probability_context import ProbabilityContext
from egg_farm_state import EggFarmState

class EggFarm:
    def __init__(self, initial_chickens: int, probability_context: ProbabilityContext, output_fraction: float = 0.5) -> None:
        self.__state = EggFarmState(initial_chickens=initial_chickens)
        self.output_fraction = output_fraction
        self.probability_context = probability_context

    @property
    def output_eggs(self):
        return self.__state.eggs
    
    @property
    def chickens(self):
        return self.__state.chickens

    def reset(self):
        self.__state.reset_to_initial_values()

    def __get_new_output_and_chatching_eggs(self, iteration: int) -> tuple[int, int]:
        new_eggs = self.probability_context.draw_layed_eggs(self.chickens)
        new_output_eggs = int(self.output_fraction*new_eggs)
        new_chatching_eggs = int(new_eggs - new_output_eggs)
        return new_output_eggs, new_chatching_eggs

    def tick(self, iteration: int):
        new_output_eggs, new_chatching_eggs = self.__get_new_output_and_chatching_eggs(iteration)
        # new_chickens= sum([int(ProbabilityContext.did_chatch_from_egg()) for _ in range(new_chatching_eggs)])
        new_chickens = self.probability_context.draw_hatched_chickens(new_chatching_eggs)

        self.__state.add_eggs(new_output_eggs)
        self.__state.add_chickens(new_chickens)