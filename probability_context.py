from random import random
from distribution import Normal
from typing import Callable


class ProbabilityContext:
    TICKS_PER_SECOND = 20
    AVERAGE_LAY_WINDOOW_IN_MINUTES = 7.5

    def __init__(
        self, 
        draw_hatched_chickens: Callable = Normal.draw_sub_sample_size, 
        draw_layed_eggs: Callable = Normal.draw_sub_sample_size
    ) -> None:
        self.draw_hatched_chickens = draw_hatched_chickens
        self.draw_layed_eggs = draw_layed_eggs

    @staticmethod
    def did_chatch_from_egg() -> bool:
        return random() < 1/8

    @classmethod
    def did_lay_egg(cls, n_iteration: int) -> bool:
        return n_iteration != 0 and n_iteration % (cls.TICKS_PER_SECOND*60*cls.AVERAGE_LAY_WINDOOW_IN_MINUTES) == 0
