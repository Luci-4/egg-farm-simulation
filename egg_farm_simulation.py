from egg_farm import EggFarm
from json import load as json_load, decoder
from egg_goal_not_reached_error import EggGoalNotReachedError
from time import time

class EggFarmSimulation:

    def __init__(self, farm: EggFarm, config_file_path: str) -> None:
        self.farm = farm 
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
        last_printed_values = (None, None) 
        while time() - start_time < self.duration_in_seconds:
            self.farm.tick(n_iteration)
            if (self.farm.output_eggs, self.farm.chickens) != last_printed_values:
                print(self.farm.output_eggs, self.farm.chickens, n_iteration)
            last_printed_values = (self.farm.output_eggs, self.farm.chickens)
            n_iteration += 1
        # print(n_iteration)
        return self.farm.output_eggs
