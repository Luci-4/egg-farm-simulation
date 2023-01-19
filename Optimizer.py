from json import load as json_load, decoder
from numpy import arange
from multiprocessing import Process, Manager

from egg_farm_simulation import EggFarmSimulation
from optimization_result import OptimizationResult
from math import log, ceil

class Optimizer:
    def __init__(self, egg_farm_simulation: EggFarmSimulation, config_file_path: str) -> None:
        self.egg_farm_simulation = egg_farm_simulation
        try:
            with open(config_file_path, encoding="utf-8") as file:
                config_data = json_load(file)
        except FileNotFoundError:
            exit("config file not found")
        except decoder.JSONDecodeError:
            exit("config parsing error")
        else:
            self.multiprocessing_optimization = config_data["multiprocessed_optimization"]
            self.optimization_interval_count = config_data["optimization_interval_count"]
            self.simulation_sample = config_data["simulation_sample"]
            self.iterations_per_process = config_data["iterations_per_process"]

    @staticmethod
    def __wait_for_all_processes(processes: list[Process]) -> None:
        while any([process.is_alive() for process in processes]):
            pass

    def get_average_egg_number_after_duration_time_elapsed(self, output_fraction: float) -> int:
        sum = 0
        self.egg_farm_simulation.set_output_fraction(output_fraction)

        for _ in range(self.simulation_sample):
            self.egg_farm_simulation.reset_initial_state()
            output_eggs = self.egg_farm_simulation.get_output_eggs_after_duration_time_elapsed()
            sum += output_eggs
        return sum/self.simulation_sample

    def populate_results(self, results: list[OptimizationResult], output_fractions: list[float]) -> None:
        for output_fraction in output_fractions:
            average_egg_number = self.get_average_egg_number_after_duration_time_elapsed(output_fraction)
            result = OptimizationResult(output_fraction, average_egg_number)
            results.append(result)
            # print("\tfinished", output_fraction, average_egg_number)

    def __init_processes(self, output_fractions_parts: list[list[float]], results: list[OptimizationResult]) -> list[Process]:
        processes = []
        for output_fraction_part in output_fractions_parts:
            process = Process(target=self.populate_results, args=(results, output_fraction_part))
            # print("starting for ", output_fraction_part)
            process.start()
            processes.append(process)
        return processes

    def __split_output_fractions_to_parts(self, potential_output_fractions: list[tuple]) -> list[list[float]]:
        split_points = range(0, len(list(potential_output_fractions)), self.iterations_per_process)
        return [list(potential_output_fractions)[i:i+self.iterations_per_process] for i in split_points]

    def __optimize_with_multiprocessing(self, results: list[OptimizationResult], potential_output_fractions: list[float]) -> None:
        output_fractions_parts = self.__split_output_fractions_to_parts(potential_output_fractions)
        processes = self.__init_processes(output_fractions_parts, results)
        self.__wait_for_all_processes(processes)        

    def round_ouput_fraction(self, fraction: float):
        return round(fraction, ceil(log(self.optimization_interval_count, 10)))
    def optimize(self) -> OptimizationResult:
        print("optimizing...")
        start = 0
        stop = 1
        interval = (stop - start)/self.optimization_interval_count
        potential_output_fractions = arange(start, stop, interval)
        results: list[OptimizationResult] = []

        if self.multiprocessing_optimization:
            shared_list = Manager().list()
            self.__optimize_with_multiprocessing(shared_list, potential_output_fractions)
            results = shared_list
        else:
            self.populate_results(results, potential_output_fractions)
        
        optimal_result = max(results, key=lambda x: x.egg_number)                       
        fractions_formated_str = "".join([(f"|{self.round_ouput_fraction(r.output_fraction)}|\t\t"if r.output_fraction == optimal_result.output_fraction else f" {self.round_ouput_fraction(r.output_fraction)} \t\t") for r in results])
        tab_space_length = 4
        tab_count = fractions_formated_str.count("\t")
        number_of_dashes = len(fractions_formated_str) + tab_count*(tab_space_length-1)
        
        print(number_of_dashes*"-")
        print(fractions_formated_str)
        print(number_of_dashes*"-")

        egg_numbers_formated_str = "".join([(f"|{int(r.egg_number)}|\t\t"if r.output_fraction == optimal_result.output_fraction else f" {int(r.egg_number)} \t\t") for r in results])
        tab_count = fractions_formated_str.count("\t")
        number_of_dashes = len(egg_numbers_formated_str) + tab_count*(tab_space_length-1)
        print(number_of_dashes*"-")
        print(egg_numbers_formated_str)
        print(number_of_dashes*"-")
        return optimal_result