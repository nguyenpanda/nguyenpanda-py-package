"""
This module contains the ColorClass class,
which contains color codes and methods to print colored text to the console.

Classes:
    - ColorClass

Instances:
    - ColorClass.Color: an instance of ColorClass, using singleton pattern.

Functions:
    - is_ansi() -> bool
"""

from sys import stdout
from typing import Dict, Literal, IO

from numpy.random import choice, seed


def is_ansi(color: str) -> bool:
    """
    Check if the color is ansi code.

    :param str color: any string
    :return: true if the color is ansi code, false otherwise.
    """
    return "\033" in color


class ColorClass:
    """
    This class contains color codes and methods to print colored text to the console.

    Properties:
        - ColorClass.reset

    Methods:
        - ColorClass.printColor()
        - ColorClass.set_seed()
        - ColorClass.__getitem__()

    """

    __RESET: str = "\033[0m"
    __COLORS: Dict[str, str] = {
        "r": "\033[1;91m",  # RED
        "g": "\033[1;92m",  # GREEN
        "y": "\033[1;93m",  # YELLOW
        "b": "\033[1;94m",  # BLUE
        "p": "\033[1;95m",  # PURPLE
        "c": "\033[1;96m",  # CYAN
    }

    def __init__(self, __seed: int | None = None):
        """
        Initialize a new instance of ColorClass.

        :param int __seed: seed for random color. Default is None.
        :type __seed: int or None
        """
        self.__seed: int | None = __seed

        if __seed is not None:
            seed(self.__seed)

    def __getitem__(self, key: str) -> str:
        """
        Retrieve color by key.

        :param key: Color key ('r', 'g', 'y', 'b', 'p', 'c').
        :return: ANSI code string for (RED, GREEN, YELLOW, BLUE, PURPLE, CYAN)
        """
        return self.__get_color(key)

    def print(self, *values: object,
              color: str | None = None,
              sep: str | None = " ",
              end: str | None = "\n",
              file: IO[str] | None = None,
              flush: Literal[False, True] = False
              ) -> None:
        """
        Prints the values to nguyenpanda stream, or to sys.stdout by default.
        If color is None, prints the values with random color.

        :param color:  ('r', 'g', 'y', 'b', 'p', 'c')
            -> (red, green, yellow, blue, purple, cyan).
        :param sep: string inserted between values, default a space.
        :param end: string appended after the last value, default a newline.
        :param file:a file-like object (stream); defaults to the current sys.stdout.
        :param flush: whether to forcibly flush the stream.
        :return: None
        """
        if color is None:
            color = self.__random_color()

        color_code = self.__get_color(color)

        stdout.write(color_code)
        print(*values, sep=sep, end=end, file=file, flush=flush)
        stdout.write(self.__RESET)

    def set_seed(self, new_seed: int | None = None) -> None:
        """
        Set seed for random color.

        :param int new_seed: seed for random color. Default is None.
        :return: None
        """
        self.__seed = new_seed
        seed(new_seed)

    @property
    def reset(self) -> str:
        """
        Returns ansi reset color.

        :return: ansi code '\033[0m'
        """
        return self.__RESET

    def __random_color(self) -> str:
        """
        Returns nguyenpanda random color

        :return: an ansi code string (RED, GREEN, YELLOW, BLUE, PURPLE, CYAN)
        """
        return self.__get_color(choice(["r", "g", "y", "b", "p", "c"]))

    def __get_color(self, color: str) -> str:
        """
        Retrieve color.

        :param color: color name (allow lower, upper, title-case or abbreviations)
        :return: ANSI code string for (RED, GREEN, YELLOW, BLUE, PURPLE, CYAN)
        """
        if is_ansi(color):
            return color

        color_key: str = color.lower()[0]
        assert (color_key in self.__COLORS), \
            f"'{color_key}' is not in (GREEN, RED, GREEN, YELLOW, BLUE, PURPLE, CYAN)"

        return self.__COLORS[color_key]


Color: ColorClass = ColorClass()
