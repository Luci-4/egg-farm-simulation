from egg_farm_simulation import EggFarmSimulation
from probability_context import ProbabilityContext
from distribution import Normal, Gamma, Exponential, Distribution
from bruteforce_optimizer import BruteforceOptimizer
from expected_value_optimizer import ExpectedValueOptimizer
from itertools import product
from time import perf_counter
from pprint import pprint
def dump_columns_into_csv(columns: list[list[any]], filename: str) -> None:
    rows = [",".join([str(i) for i in row]) for row in zip(*columns)]
    
    with open(filename, "w+") as file:
        file.write("\n".join(rows))


def compare_algorithms():
    columns = [["lay distribution"], ["hatch distribution"], ["initial chickens"], ["bruteforce optimal fraction"], ["bruteforce egg number"], ["bruteforce real run time"],  ["expected value optimal_fraction"], ["expected value egg number"], ["expected value real run time"]]

    initial_chickens_numbers = [5, 10, 30, 40, 50]
    distributions = [Normal, Gamma, Exponential]
    optimization_parameters_product: list[int, Distribution, Distribution] = list(product(initial_chickens_numbers, distributions, distributions))
    for (initial_chickens, chatched_chickens_distribution, layed_eggs_distribution) in optimization_parameters_product:
        bruteforce_probability_context = ProbabilityContext(
            draw_hatched_chickens = chatched_chickens_distribution.draw_sub_sample_size, 
            draw_layed_eggs=layed_eggs_distribution.draw_sub_sample_size
        )
        expected_value_probability_context = ProbabilityContext(
            draw_hatched_chickens = chatched_chickens_distribution.expected, 
            draw_layed_eggs=layed_eggs_distribution.expected
        )
        bruteforce_simulation = EggFarmSimulation(
            config_file_path="simulation_config.json",
            initial_chickens = initial_chickens,
            probability_context=bruteforce_probability_context
        )
        expected_value_simulation = EggFarmSimulation(
            config_file_path="simulation_config.json",
            initial_chickens = initial_chickens,
            probability_context=expected_value_probability_context
        )

        bruteforce_optimizer = BruteforceOptimizer(
            egg_farm_simulation=bruteforce_simulation,
            config_file_path="optimization_config.json"
        )
        expected_value_optimizer = ExpectedValueOptimizer(
            egg_farm_simulation=expected_value_simulation,
            config_file_path="optimization_config.json"
        )
        
        t1 = perf_counter()
        expected_value_result = expected_value_optimizer.optimize()

        print(expected_value_result)
        t2 = perf_counter()
        expected_value_run_time = t2 - t1
        print(f"expected value finished in {round(expected_value_run_time, 3)}s")

        t1 = perf_counter()
        bruteforce_result = bruteforce_optimizer.optimize()
        print(bruteforce_result)
        t2 = perf_counter()
        bruteforce_run_time = t2 - t1
        print(f"bruteforce finished in {round(bruteforce_run_time, 3)}s")
        columns[0].append(layed_eggs_distribution.NAME)
        columns[1].append(chatched_chickens_distribution.NAME)
        columns[2].append(initial_chickens)
        columns[3].append(bruteforce_result.output_fraction)
        columns[4].append(bruteforce_result.egg_number)
        columns[5].append(bruteforce_run_time)
        columns[6].append(expected_value_result.output_fraction)
        columns[7].append(expected_value_result.egg_number)
        columns[8].append(expected_value_run_time)
    dump_columns_into_csv(columns, "output.csv")


if __name__ == "__main__":
    # probability_context = ProbabilityContext(
    #     draw_hatched_chickens = Gamma.draw_sub_sample_size, 
    #     draw_layed_eggs=Gamma.draw_sub_sample_size
    # )

    # simulation = EggFarmSimulation(
    #     config_file_path="simulation_config.json",
    #     initial_chickens = 10,
    #     probability_context=probability_context
    # )
    compare_algorithms()
    # print(simulation.get_output_eggs_after_duration_time_elapsed())