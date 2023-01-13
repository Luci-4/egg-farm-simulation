from egg_farm_simulation import EggFarmSimulation
from optimizer import Optimizer
from egg_farm import EggFarm

if __name__ == "__main__":
    farm = EggFarm(initial_eggs=0, initial_chickens=1, output_fraction=0.8)
    simulation = EggFarmSimulation(
        farm=farm,
        config_file_path="simulation_config.json"
    )
    print(simulation.get_output_eggs_after_duration_time_elapsed())

    # optimizer = Optimizer(
    #     egg_farm_simulation=simulation, 
    #     config_file_path="optimization_config.json"
    # )
    # print(optimizer.optimize())

# TODO: random initial state (eggs chickens)
# expected value (2nd algorithm)
# replace random single hatch with multiple
# real time limit with egg number output