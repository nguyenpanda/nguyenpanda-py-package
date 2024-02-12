import sys
from nguyenpanda.swan import Color


def __test_slicing() -> None:
    print(Color['RED'] + 'Tuong Nguyen Khoai To' + Color.reset)
    print(Color['r'] + 'Tuong Nguyen Khoai Rat To' + Color.reset)
    print(Color['rEd'] + 'Tuong Nguyen Khoai Rat Rat To' + Color.reset)
    print(Color['ReD'] + 'Tuong Nguyen Khoai Rat Rat Rat To' + Color.reset)
    print(Color['reD'] + 'Tuong Nguyen Khoai Rat Rat Rat To' + Color.reset)


def __test_printColor() -> None:
    dict_color: tuple = ('rEd', 'gREEn', 'Yellow', 'bLUE', 'pUrpLe', 'c')

    for i in range(21, 81):
        Color.printColor(i, end=' ')
        if i % 20 == 0:
            sys.stdout.write('\n')

    for __color in dict_color:
        Color.printColor(__color, color=__color, end=' ')
    sys.stdout.write('\n')

    for __color in dict_color:
        for i in range(20):
            Color.printColor(i, color=__color, end=' ')
        sys.stdout.writelines('\n')


if __name__ == '__main__':
    __test_slicing()

    __test_printColor()
