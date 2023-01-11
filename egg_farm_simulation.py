from egg_farm import EggFarm
from json import load as json_load, decoder
from egg_goal_not_reached_error import EggGoalNotReachedError

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
        self.output_egg_number_goal = config_data["output_egg_number_goal"]
        self.iteration_n_limit = config_data["iteration_n_limit"]
        self.simulation_sample = config_data["simulation_sample"]

    def try_to_get_average_iterations_to_reach_egg_goal(self, output_fraction: float) -> float:
        sum = 0
        self.farm.output_fraction = output_fraction

        for _ in range(self.simulation_sample):
            self.farm.reset()
            iterations = self.__try_to_get_iterations_to_reach_egg_goal()
            sum += iterations
        return sum/self.simulation_sample

    def __try_to_get_iterations_to_reach_egg_goal(self) -> int:
        for n_iteration in range(1, self.iteration_n_limit+1):
            self.farm.tick(n_iteration)

            if self.farm.output_eggs >= self.output_egg_number_goal:
                return n_iteration

        raise EggGoalNotReachedError(self.iteration_n_limit)
