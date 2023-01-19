from egg_farm import EggFarm
from json import load as json_load, decoder
from egg_goal_not_reached_error import EggGoalNotReachedError
from probability_context import ProbabilityContext
from time import time

class EggFarmSimulation:

    def __init__(self, initial_chickens: int, probability_context: ProbabilityContext, config_file_path: str) -> None:
        self.farm = EggFarm(
            initial_chickens=initial_chickens,
            probability_context=probability_context
        )
        try:
            with open(config_file_path, encoding="utf-8") as file:
                config_data = json_load(file)
        except FileNotFoundError:
            exit("config file not found")
        except decoder.JSONDecodeError:
            exit("config parsing error")
        else:
            self.__init_fields_from_config_data(config_data)

    def __init_fields_from_config_data(self, config_data: dict[str, any]) -> None:
        self.duration_in_seconds = config_data["duration_in_seconds"]

    def set_output_fraction(self, value: float) -> None:
        self.farm.output_fraction = value

    def reset_initial_state(self) -> None:
        self.farm.reset()

    def get_output_eggs_after_duration_time_elapsed(self) -> int:
        start_time = time()
        n_iteration = 1

        while time() - start_time < self.duration_in_seconds:
            self.farm.tick(n_iteration)
            n_iteration += 1
        return self.farm.output_eggs
