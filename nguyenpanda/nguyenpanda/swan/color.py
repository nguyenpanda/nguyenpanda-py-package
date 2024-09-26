from sys import stdout
from typing import Dict, Literal, IO, Iterable, Optional, Union
from abc import ABC, abstractmethod
import random


class BaseColor(ABC):

    def __init__(self, __seed, is_foreground: bool = True):
        self.reset = '\033[0m'
        self.__seed = __seed
        self.is_foreground = is_foreground

    def set_seed(self):
        pass

    def print(self, *values: object, color: Optional[str] = None, sep: Optional[str] = ' ', end: Optional[str] = '\n',
              file: Optional[IO[str]] = None, flush: Literal[False, True] = False) -> None:
        """
        Prints the values to nguyenpanda stream, or to sys.stdout by default.
        If color is None, prints the values with random color.

        :param color:  Depend on class, e.g., ColorClass: ('r', 'g', 'y', 'b', 'p', 'c')
            -> (red, green, yellow, blue, purple, cyan).
        :param sep: string inserted between values, default a space.
        :param end: string appended after the last value, default a newline.
        :param file:a file-like object (stream); defaults to the current sys.stdout.
        :param flush: whether to forcibly flush the stream.
        :return: None
        """
        color_code = self.random() if None else self[color]

        stdout.write(color_code)
        print(*values, sep=sep, end=end, file=file, flush=flush)
        stdout.write(self.reset)

    def __call__(self, color):
        return self[color]

    @abstractmethod
    def __getitem__(self, color) -> str:
        pass

    @abstractmethod
    def random(self) -> str:
        pass


class FourBitColor(BaseColor):
    """
    This class contains color codes and methods to print colored text to the console.
    """

    _COLOR_KEYS: Dict[str, int] = {
        ' ': 0,  # BLACK
        'r': 1,  # RED
        'g': 2,  # GREEN
        'y': 3,  # YELLOW
        'b': 4,  # BLUE
        'm': 5,  # MAGENTA
        'c': 6,  # CYAN
    }

    def __init__(self, __seed: Optional[int] = None, is_foreground: bool = True, is_bright: bool = True):
        """
        Initialize a new instance of ColorClass.

        :param int __seed: seed for random color. Default is None.
        :type __seed: int or None
        """
        super().__init__(__seed, is_foreground)
        self.keys = list(self._COLOR_KEYS.keys())
        if is_bright:
            self.code = '\033[1;9{}m' if is_foreground else '\033[1;10{}m'
        else:
            self.code = '\033[1;3{}m' if is_foreground else '\033[1;4{}m'

    def __getitem__(self, color: Union[Literal[' ', 'r', 'g', 'y', 'b', 'm', 'c'], str, int, None]) -> str:
        """
        Retrieve the ANSI code color (BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN) for a specified color key.

        :param color: A color key that must be one of (' ', 'r', 'g', 'y', 'b', 'm', 'c', 'p') or a string that starts
        with one of these letters. The input can start with uppercase.

        :return: The ANSI escape code string corresponding to the specified color.

        :raises KeyError: If the provided color key is not one of the valid options.
        """
        try:
            if color:
                if isinstance(color, int):
                    return self.code.format(color)
                return self.code.format(self._COLOR_KEYS[color[0].lower()])
            else:
                return self.random()
        except KeyError as e:
            raise ValueError(f"Invalid color key: '{color}'. Must be one of {self.keys}.") from e

    def random(self):
        """
        Returns nguyenpanda random color

        :return: an ansi code string (RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN)
        """
        return self[random.choice(self.keys)]


class EightBitColor(BaseColor):
    """
    A class to generate ANSI escape codes for 8-bit colors, supporting both foreground and background colors.

    This class allows you to generate ANSI escape codes for terminal colorization using either specific 8-bit color
    values or random colors within a specified range. It supports both foreground and background color codes.

    Example usage:
        color = EightBitColor(color_range=(16, 231), is_foreground=True)
        print(color[128])      # Generate a color code for the specific 8-bit color value 128.
        print(color.random())  # Generate a random color code within the specified range.

    Attributes:
        range (tuple[int] | list[int]): The range of 8-bit color values allowed (inclusive).
        code (str): The ANSI escape code template for either foreground or background colors.

    Methods:
        __getitem__(color: int | None) -> str:
            Retrieves the ANSI escape code for the given 8-bit color value.

        random() -> str:
            Generates a random 8-bit color code within the specified range.
    """

    def __init__(self, color_range: Union[tuple[int], list[int]] = (0, 255),
                 is_foreground: bool = True, __seed: Optional[int] = None):
        """
        Initializes an 8-bit color object.

        :param color_range: A tuple or list specifying the range of valid 8-bit color values (inclusive).
                            Defaults to (0, 255).
        :param is_foreground: Determines if the color is for the foreground (True) or background (False).
        :param __seed: Optional seed for random color generation.
        :raises ValueError: If the color_range is not a tuple or list, or if it does not contain exactly two elements.
        """
        super().__init__(__seed, is_foreground)
        self.range = color_range
        self.code = '\033[38;5;{}m' if is_foreground else '\033[48;5;{}m'

        if not isinstance(self.range, (tuple, list)) or len(self.range) != 2:
            raise ValueError("color_range must be a tuple or list containing exactly two integers.")

    def __getitem__(self, color: Optional[int]) -> str:
        """
        Retrieves the ANSI escape code for the given 8-bit color value.

        :param color: An integer representing the 8-bit color value. If None, a random color will be generated.
        :return: The ANSI escape code string.
        :raises ValueError: If the color value is outside the specified range.
        """
        if color:
            if color < self.range[0] or color > self.range[1]:
                raise ValueError(f"Invalid color key: '{color}'. Must be in range of {self.range}.")
            return self.code.format(color)
        else:
            return self.random()

    def random(self) -> str:
        """
        Generates a random 8-bit color within the specified range.

        :return: The ANSI escape code string for the random color.
        """
        return self[random.randint(*self.range)]


class Two4BitColor(BaseColor):
    """
        A class to generate ANSI escape codes for 24-bit RGB colors, supporting both foreground and background colors.

    This class can generate ANSI escape codes for terminal colorization using either specific RGB values or random
    colors. It supports RGB input as a list or tuple of integers (0-255) or hexadecimal strings (e.g., 'ff').
    The generated escape codes can be used to colorize text or backgrounds in a terminal.

    Example usage:
        color = Two4BitColor(is_foreground=True)
        print(color[['ff', 220, 'f2']])  # Generate a color code from mixed RGB input.
        print(color[(255, 0, 128)])      # Generate a color code from integer RGB values.
        print(color.random())            # Generate a random color code.

    Attributes:
        code (str): The ANSI escape code template for either foreground or background colors.

    Methods:
        __getitem__(rgb: list[int | str] | tuple[int | str]) -> str:
            Retrieves the ANSI escape code for the given RGB color.

        random() -> str:
            Generates a random 24-bit RGB color code.
    """

    def __init__(self, is_foreground: bool = True, __seed: Optional[int] = None):
        """
        Initializes a 24-bit color object.

        :param is_foreground: Determines if the color is for the foreground (True) or background (False).
        :param __seed: Optional seed for random color generation.
        """
        super().__init__(__seed, is_foreground)
        self.code = '\033[38;2;{};{};{}m' if is_foreground else '\033[48;2;{};{};{}m'

    def __getitem__(self, rgb: Union[int, str, Iterable[str], Iterable[int], Iterable[Union[str, int]]]) -> str:
        """
        Retrieves the ANSI escape code for the given RGB color.

        :param rgb: A list or tuple representing RGB values. It can be:
                    - A list or tuple of three integers in the range 0-255.
                    - A list or tuple of three hexadecimal strings (or a mix of integers and hex strings).
                    - A single string representing the full RGB color in hexadecimal (e.g., 'ff0f13').
        :return: The ANSI escape code string.
        :raises ValueError: If the input is invalid.
        """
        if rgb:
            if isinstance(rgb, int):
                rgb = (rgb, rgb, rgb)
            elif isinstance(rgb, str) and len(rgb) == 6:
                rgb = [int(rgb[i:i + 2], 16) for i in range(0, 6, 2)]
            elif len(rgb) == 3:
                rgb = [int(c, 16) if isinstance(c, str) else c for c in rgb]
            else:
                raise ValueError("RGB must be a list or tuple of exactly three values, or a single 6-character hex string.")

            if not all(0 <= c <= 255 for c in rgb):
                raise ValueError("RGB values must be in the range 0-255.")

            return self.code.format(*rgb)
        else:
            return self.random()

    def random(self) -> str:
        """
        Generates a random 24-bit color.

        :return: The ANSI escape code string for the random color.
        """
        return self[[random.randint(0, 255) for _ in range(3)]]
