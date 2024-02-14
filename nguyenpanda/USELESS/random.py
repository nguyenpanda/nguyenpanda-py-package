from abc import ABC, abstractmethod

class Random(ABC):

    def __init__(self, seed: int, *args, **kwargs):
        assert isinstance(seed, int), f'seed must be an integer (got {seed})'

        self.__seed = seed

