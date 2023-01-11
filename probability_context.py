from random import random

class ProbabilityContext:
    TICKS_PER_SECOND = 20
    AVERAGE_LAY_WINDOOW_IN_MINUTES = 7.5

    @staticmethod
    def did_chatch_from_egg() -> bool:
        return random() < 1/8

    @classmethod
    def did_lay_egg(cls, n_iteration: int) -> bool:
        return n_iteration != 0 and n_iteration % (cls.TICKS_PER_SECOND*60*cls.AVERAGE_LAY_WINDOOW_IN_MINUTES) == 0