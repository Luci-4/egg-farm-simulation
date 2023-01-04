from typing import Callable
from random import random
from numpy import arange
from multiprocessing import Process
from ProbabilityContext import ProbabilityContext
from EggFarm import EggFarm
from json import load as json_load, decoder

class EggFarmSimulation:

    def __init__(self, farm: EggFarm, config_file_path: str) -> None:
        try:
            with open(config_file_path, encoding="utf-8") as file:
                config_data = json_load(file)
        except FileNotFoundError:
            exit("config file not found")
        except decoder.JSONDecodeError:
            exit("config parsing error")
        else:
            self.__init_fields_from_config_data(config_data)
        self.farm = farm 

    def __init_fields_from_config_data(self, config_data: dict[str, any]) -> None:
        self.output_egg_number_goal = config_data["output_egg_number_goal"]
        self.iteration_n_limit = config_data["iteration_n_limit"]
        self.multiprocessing_optimization = config_data["multiprocessed_optimization"]
        self.optimization_interval_count = config_data["optimization_interval_count"]
        self.iterations_per_process = config_data["iterations_per_process"]
        self.simulation_sample = config_data["simulation_sample"]

    def __calculate_average_simulation_iteration_number(self, output_fraction: float) -> float:
        sum = 0
        self.farm.output_fraction = output_fraction

        for i in range(self.simulation_sample):
            self.farm.reset()
            result = self.simulate_farm_work_cycle()
            if result is None:
                return
            iterations = result
            sum += iterations
        return sum/self.simulation_sample

    def populate_output_fractions_iterations_results(self, output_fractions_iterations, output_fractions):
        for output_fraction in output_fractions:
            average_iteration_count = self.__calculate_average_simulation_iteration_number(output_fraction)
            output_fractions_iterations.append((output_fraction, average_iteration_count))
            print("\tfinished", output_fraction, average_iteration_count)

    def __split_output_fractions_to_parts(self, potential_output_fractions) -> list[list[float]]:
        split_points = range(0, len(list(potential_output_fractions)), self.iterations_per_process)
        return [list(potential_output_fractions)[i:i+self.iterations_per_process] for i in split_points]

    @staticmethod
    def __wait_for_all_processes(processes: list[Process]) -> None:
        while any([process.is_alive() for process in processes]):
            pass

    def __init_processes(self, output_fractions_parts, output_fractions_iterations_results) -> list[Process]:
        processes = []
        for percentages_part in output_fractions_parts:
            # thread = Thread(target=self.thread_callback, args=(percentages_part, simulation_tries), daemon=True)
            process = Process(target=self.populate_output_fractions_iterations_results, args=(output_fractions_iterations_results, percentages_part))
            print("starting for ", percentages_part)
            process.start()
            processes.append(process)
        return processes

    def __optimize_with_multiprocessing(self, output_fractions_iterations_results, potential_output_fractions):
        output_fractions_parts = self.__split_output_fractions_to_parts(potential_output_fractions)
        processes = self.__init_processes(output_fractions_parts, output_fractions_iterations_results)
        self.__wait_for_all_processes(processes)        


    def optimize(self):
        start = 0
        stop = 1
        interval = (stop - start)/self.optimization_interval_count
        potential_output_fractions = arange(start, stop, interval)
        # percentage_results = [(percentage, self.__average_simulate(percentage,simulation_tries)) for percentage in percentages]
        output_fractions_iterations_results = []

        if self.multiprocessing_optimization:
            self.__optimize_with_multiprocessing(output_fractions_iterations_results, potential_output_fractions)
        else:
            self.populate_output_fractions_iterations_results(output_fractions_iterations_results, potential_output_fractions)

        valid_percentage_results = [i for i in output_fractions_iterations_results if not(i[1] is None)]
        
        optimal_output_fraction, minimal_iteration_count = min(valid_percentage_results, key=lambda x: x[1])                       
        print("".join([(f"|{p}|\t\t"if p == optimal_output_fraction else f" {p} \t\t") for (p, n) in valid_percentage_results]))
        print("".join([(f"|{n}|\t\t"if p == optimal_output_fraction else f" {n} \t\t") for (p, n) in valid_percentage_results]))
        return optimal_output_fraction, minimal_iteration_count

        
    def simulate_farm_work_cycle(self):
        for n_iteration in range(1, self.iteration_n_limit+1):
            self.farm.tick(n_iteration)

            if self.farm.output_eggs >= self.output_egg_number_goal:
                return n_iteration

