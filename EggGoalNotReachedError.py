class EggGoalNotReachedError(Exception):
    def __init__(self, iteration_limit: int) -> None:
            message = f"Iteration limit {iteration_limit} reached without reaching the egg goal"
            super().__init__(message)
        