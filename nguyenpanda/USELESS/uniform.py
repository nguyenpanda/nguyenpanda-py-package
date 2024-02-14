import os
import time
from typing import Tuple, Generator


class Uniform:

    def __init__(self, seed: int | float | None = None,
                 weight: int = 65432,
                 bias: int = 0,
                 modulus: int = 2 ** 32 - 1):

        self.__seed: int | float = (
                int(str(time.time()).split('.')[1]) + 13 * os.getpid() & 0xFFFFFFFF
        ) if seed is None else seed

        self.__state: int | float = self.__seed

        self.__w: int = weight
        self.__b: int = bias
        self.__m: int = modulus

        self.__generator: Generator = self.__LinearCongruentialGenerator()

    @property
    def seed(self) -> int | float:
        return self.__seed

    @property
    def parameters(self) -> Tuple[int, int, int]:
        return self.__w, self.__b, self.__m

    @parameters.setter
    def parameters(self, values: list | tuple):
        weight, bias, m = values
        if all(isinstance(param, int) for param in values):
            self.__w = weight
            self.__b = bias
            self.__m = m

    @property
    def generator(self):
        return self.__generator

    def __LinearCongruentialGenerator(self) -> Generator:
        while True:
            self.__state = (self.__w * self.__state + self.__b) % self.__m
            yield self.__state
