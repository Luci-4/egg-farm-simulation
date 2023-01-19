class OptimizationResult:
    def __init__(self, output_fraction: float, egg_number: int) -> None:
        self.output_fraction = output_fraction
        self.egg_number = egg_number

    def __repr__(self) -> str:
        return f"({self.output_fraction}, {self.egg_number})"