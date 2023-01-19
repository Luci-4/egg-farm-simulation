from optimizer import Optimizer
from egg_farm_simulation import EggFarmSimulation

class BruteforceOptimizer(Optimizer):
    def __init__(self, egg_farm_simulation: EggFarmSimulation, config_file_path: str) -> None:
        super().__init__(egg_farm_simulation, config_file_path)