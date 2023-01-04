from json import load as json_load, decoder
from numpy import arange
from multiprocessing import Process, Manager

from EggFarmSimulation import EggFarmSimulation
from OptimizationResult import OptimizationResult

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
            self.iterations_per_process = config_data["iterations_per_process"]

    @staticmethod
    def __wait_for_all_processes(processes: list[Process]) -> None:
        while any([process.is_alive() for process in processes]):
            pass

    def populate_output_fractions_iterations_results(self, output_fractions_iterations_results: list[OptimizationResult], output_fractions: list[float]) -> None:
        for output_fraction in output_fractions:
            average_iteration_count = self.egg_farm_simulation.calculate_average_simulation_iteration_number(output_fraction)
            result = OptimizationResult(output_fraction, average_iteration_count)
            output_fractions_iterations_results.append(result)
            print("\tfinished", output_fraction, average_iteration_count)

    def __init_processes(self, output_fractions_parts: list[list[float]], output_fractions_iterations_results: list[OptimizationResult]) -> list[Process]:
        processes = []
        for output_fraction_part in output_fractions_parts:
            process = Process(target=self.populate_output_fractions_iterations_results, args=(output_fractions_iterations_results, output_fraction_part))
            print("starting for ", output_fraction_part)
            process.start()
            processes.append(process)
        return processes

    def __split_output_fractions_to_parts(self, potential_output_fractions: list[tuple]) -> list[list[float]]:
        split_points = range(0, len(list(potential_output_fractions)), self.iterations_per_process)
        return [list(potential_output_fractions)[i:i+self.iterations_per_process] for i in split_points]


    def __optimize_with_multiprocessing(self, output_fractions_iterations_results: list[OptimizationResult], potential_output_fractions: list[float]) -> None:
        output_fractions_parts = self.__split_output_fractions_to_parts(potential_output_fractions)
        processes = self.__init_processes(output_fractions_parts, output_fractions_iterations_results)
        self.__wait_for_all_processes(processes)        


    def optimize(self) -> OptimizationResult:
        start = 0
        stop = 1
        interval = (stop - start)/self.optimization_interval_count
        potential_output_fractions = arange(start, stop, interval)
        output_fractions_iterations_results: list[OptimizationResult] = []

        if self.multiprocessing_optimization:
            shared_list = Manager().list()
            self.__optimize_with_multiprocessing(shared_list, potential_output_fractions)
            output_fractions_iterations_results = shared_list
        else:
            self.populate_output_fractions_iterations_results(output_fractions_iterations_results, potential_output_fractions)

        valid_output_fractions_results = [i for i in output_fractions_iterations_results if not(i.iteration_count is None)]
        
        optimal_result = min(valid_output_fractions_results, key=lambda x: x.iteration_count)                       
        print("".join([(f"|{r.output_fraction}|\t\t"if r.output_fraction == optimal_result.output_fraction else f" {r.output_fraction} \t\t") for r in valid_output_fractions_results]))
        print("".join([(f"|{r.iteration_count}|\t\t"if r.output_fraction == optimal_result.output_fraction else f" {r.iteration_count} \t\t") for r in valid_output_fractions_results]))
        return optimal_result