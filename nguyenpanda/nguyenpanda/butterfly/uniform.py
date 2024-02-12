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

    def __LinearCongruentialGenerator(self) -> Generator:
        while True:
            self.__state = (self.__w * self.__state + self.__b) % self.__m
            yield self.__state


if __name__ == "__main__":
    from nguyenpanda.swan import Color

    Color.printColor('--- Swan - Uniform ---', color=Color['b'])

    w = 214013
    b = 2531011
    m = 2 ** 31

    __seed = time.time()


    def cal(i):
        return (w * i + b) % m


    for _ in range(100):
        __seed = cal(__seed)
        print(__seed / m)

    Color.printColor('--- Swan - Uniform ---', color=Color['g'])
