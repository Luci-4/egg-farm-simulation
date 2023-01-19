from optimizer import Optimizer
from egg_farm_simulation import EggFarmSimulation

class ExpectedValueOptimizer(Optimizer):
    def __init__(self, egg_farm_simulation: EggFarmSimulation, config_file_path: str) -> None:
        super().__init__(egg_farm_simulation, config_file_path)

    def get_average_egg_number_after_duration_time_elapsed(self, output_fraction: float) -> int:
        self.egg_farm_simulation.set_output_fraction(output_fraction)
        self.egg_farm_simulation.reset_initial_state()
        output_eggs = self.egg_farm_simulation.get_output_eggs_after_duration_time_elapsed()
        return output_eggs

    def optimize(self):
        return super().optimize()