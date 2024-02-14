from typing import Generator

from nguyenpanda.nguyenpanda.butterfly import Uniform
from nguyenpanda.nguyenpanda.swan import Color


def test_paras_setter():
    input_para = (1, 2, 3)

    random: Uniform = Uniform()
    random.parameters = input_para
    result: bool = all(i == o for i, o in zip(input_para, random.parameters))

    if result == False:




def test_LinearCongruentialGenerator_is_Uniform(simulate: int, sample: int, _range: list | tuple) -> float:
    def each_iterator() -> float:
        random: Uniform = Uniform()
        w, b, m = random.parameters

        generator: Generator = random.generator
        result: list = []
        pro: int = 0

        result.extend(i / m for i in [next(generator) for _ in range(sample)])

        for n in result:
            if _range[0] <= n <= _range[1]:
                pro += 1

        return pro / sample

    results = [each_iterator() for _ in range(simulate)]

    return sum(results) / simulate


if __name__ == '__main__':
    Color.printColor('--- Swan - Test para setter ---', color=Color['b'])
    print()

    Color.printColor('--- Swan - Test is Uniform Distribution ---', color=Color['b'])
    print('Result: ', end='')
    Color.printColor(test_LinearCongruentialGenerator_is_Uniform(1000, 1000, (0, 0.5)), color='g')

