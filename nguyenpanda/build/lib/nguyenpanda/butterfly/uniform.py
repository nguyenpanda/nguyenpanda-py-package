import os
import time
from typing import Tuple, Generator


class Uniform:

    def __init__(self, seed: int | float | None = None):
        self.__seed: int | float = seed if seed is not None else (
                int(str(time.time()).split('.')[1]) + 13 * os.getpid() & 0xFFFFFFFF
        )
        self.__state: int | float = self.__seed

        self.__w: int = 65432
        self.__b: int = 0
        self.__m: int = 2 ** 32 - 1

    @property
    def seed(self) -> int | float:
        return self.__seed

    @property
    def parameters(self) -> Tuple[int, int, int]:
        return self.__w, self.__b, self.__m

    def _LinearCongruentialGenerator(self) -> Generator:
        while True:
            self.__state = (self.__w * self.__state + self.__b) % self.__m
            yield self.__state

