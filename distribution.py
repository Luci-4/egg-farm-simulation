from numpy.random import normal, exponential, gamma
from numpy import mean, std

class Distribution:

    @staticmethod
    def convert_value_to_valid_int_sample_size(value: float, collection_length: int):
        random_n = round(value)
        return max(min(collection_length, random_n), 0)

    @staticmethod
    def create_draw_options(collection_length: int) -> list[float]:
        return [i for i in range(collection_length+1)]

    @classmethod
    def draw_sub_sample_size(cls, collection_length: int) -> list[float]:
        raise NotImplementedError

    @classmethod
    def expected(cls, collection_length: int) -> list[float]:
        raise NotImplementedError

class Normal(Distribution):
    std_divisor = 2
    NAME = "normal"
    @classmethod
    def draw_sub_sample_size(cls, collection_length: int) -> list[float]:
        draw_options = cls.create_draw_options(collection_length)
        mean_ = mean(draw_options)
        standard_deviation = std(draw_options)/cls.std_divisor
        random_value = float(normal(mean_, standard_deviation))
        return cls.convert_value_to_valid_int_sample_size(random_value, collection_length)

    @classmethod
    def expected(cls, collection_length: int) -> list[float]:
        draw_options = cls.create_draw_options(collection_length)
        expected_value = float(mean(draw_options))
        return cls.convert_value_to_valid_int_sample_size(expected_value, collection_length)

class Exponential(Distribution):

    NAME = "exponential"
    mean_divisor = 3.5
    @classmethod
    def draw_sub_sample_size(cls, collection_length: int):
        draw_options = cls.create_draw_options(collection_length)
        mean_ = mean(draw_options)/cls.mean_divisor
        random_value = float(exponential(mean_))
        return cls.convert_value_to_valid_int_sample_size(random_value, collection_length)

    @classmethod
    def expected(cls, collection_length: int) -> list[float]:
        draw_options = cls.create_draw_options(collection_length)
        expected_value = float(mean(draw_options)/cls.mean_divisor)
        return cls.convert_value_to_valid_int_sample_size(expected_value, collection_length)


class Gamma(Distribution):
    NAME = "gamma"
    shape = 2
    mean_divisor = 5.3
    @classmethod
    def draw_sub_sample_size(cls, collection_length: int):
        draw_options = cls.create_draw_options(collection_length)
        random_value = float(gamma(cls.shape, mean(draw_options)/cls.mean_divisor))
        return cls.convert_value_to_valid_int_sample_size(random_value, collection_length)

    @classmethod
    def expected(cls, collection_length: int) -> list[float]:
        draw_options = cls.create_draw_options(collection_length)
        expected_value = float((mean(draw_options)/cls.mean_divisor)*cls.shape)
        return cls.convert_value_to_valid_int_sample_size(expected_value, collection_length)


def test_distribution(dist: Distribution, collection_length: int):
    x = []
    for _ in range(10000):
        r = dist.draw_sub_sample_size(collection_length)
        x.append(r)
    print(type(dist.expected(collection_length)))
    # import matplotlib.pyplot as plt
    # plt.hist(x, bins=collection_length)
    # plt.show()
