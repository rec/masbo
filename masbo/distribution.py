import dataclasses as dc
import math
import random


@dc.dataclass
class Distribution:
    mean: float
    var: float

    def __call__(self) -> float:
        raise NotImplementedError


class Distributions:
    class Constant(Distribution):
        def __call__(self) -> float:
            return self.mean

    class Uniform(Distribution):
        def __call__(self) -> float:
            return math.uniform(self.mean - self.var / 2, self.mean + self.var / 2)

    class Poisson(Distribution):
        def __call__(self) -> float:
            return -math.log(1 - random.random()) * self.mean


def create(name: str, mean: float, var: float) -> Distribution:
    assert name and not name.startswith('_')
    name = name.capitalize()
    dists = [v for k, v in vars(Distributions) if k.lower().startswith(name)]
    assert len(dists) == 1, str(dists)
    return dists[0]
