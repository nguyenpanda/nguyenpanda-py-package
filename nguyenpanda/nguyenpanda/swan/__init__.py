"""
🦢 swan
    Indulge in the beauty of aesthetics and user interfaces with the elegant swan package.
    Dive into the world of colors, front-end development, GUI, and more.
    Transform your applications into visual masterpieces with swan.

    Classes:
        - 'BaseColor',
        - 'FourBitColor',
        - 'EightBitColor',
        - 'Two4BitColor',

    Instances:
    'color', 'c4', 'c4b', 'c4d', 'c4db',
    'c8', 'c8b',
    'c24', 'c24b',
    'green',
    'red',
    'yellow'

    Examples
    ```
    from nguyenpanda.swan import color, c8, c24

    print(color['green'] + 'Hello! World' + color.reset)

    print(c8[79] + 'nguyenpanda' + c8.reset)

    print(c24['ff00ff'] + 'nguyenpanda' + c24.reset)
    print(c24['ff', 0, 'ff'] + 'nguyenpanda' + c24.reset)
    print(c24[0, 255, 200] + 'nguyenpanda' + c24.reset)
    ```
"""

from .color import BaseColor, FourBitColor, EightBitColor, Two4BitColor
from typing import Literal


def set_color_bit(bit: Literal[4, 8, 24], is_foreground: bool = True, is_bright: bool = True) -> BaseColor:
    """
    Sets the global `color` instance to a new color class based on the specified bit depth.

    This function allows the user to change the type of color used in the application by selecting
    between 4-bit, 8-bit, or 24-bit color modes. The `color` instance is updated globally, so subsequent
    uses of the `color` variable will reflect this change.

    Args:
        bit (Literal[4, 8, 24]): The bit depth of the color to be used. Valid options are:
            - 4: Use a 4-bit color mode, selecting from a predefined set of colors.
            - 8: Use an 8-bit color mode, allowing for 256 possible colors.
            - 24: Use a 24-bit color mode, allowing for true color with millions of possible colors.

        is_foreground (bool, optional): Determines if the color applies to the foreground.
            Defaults to True. This argument is relevant for 4-bit and 24-bit color modes.

        is_bright (bool, optional): Determines if the 4-bit color should use the bright variant.
            Defaults to True. This argument is only relevant when `bit` is 4.

    Returns:
        BaseColor: The newly created color instance, which is also assigned to the global `color` variable.

    Raises:
        ValueError: If an invalid bit value is provided. Valid options are 4, 8, or 24.
    """
    global color
    if bit == 4:
        color = FourBitColor(is_foreground, is_bright)
    elif bit == 8:
        color = EightBitColor()
    elif bit == 24:
        color = Two4BitColor()
    else:
        raise ValueError(f'DEFAULT_COLOR_BITS must be (4, 8, 24), got {bit}')
    return color


color: BaseColor = FourBitColor()

c4: FourBitColor = FourBitColor()  # 4-bit color (foreground & bright)
c4b: FourBitColor = FourBitColor(is_foreground=False)  # 4-bit color (background & bright)
c4d: FourBitColor = FourBitColor(is_bright=False)  # 4-bit color (foreground & dark)
c4db: FourBitColor = FourBitColor(is_foreground=False, is_bright=False)  # 4-bit color (background & dark)

c8: EightBitColor = EightBitColor()  # 8-bit color (foreground)
c8b: EightBitColor = EightBitColor(is_foreground=False)  # 8-bit color (background)

c24: Two4BitColor = Two4BitColor()  # 24-bit color (foreground)
c24b: Two4BitColor = Two4BitColor(is_foreground=False)  # 24-bit color (foreground)

RESET = reset = '\033[0m'

def green(text) -> str:
    """
    Wrap the text with green color.
    Args:
        text: input text
    Returns: green text
    """
    return '\033[1;92m' + str(text) + '\033[0m'


def red(text) -> str:
    """
    Wrap the text with red color.
    Args:
        text: input text
    Returns: red text
    """
    return '\033[1;91m' + str(text) + '\033[0m'


def yellow(text) -> str:
    """
    Wrap the text with yellow color.
    Args:
        text: input text
    Returns: red text
    """
    return '\033[1;93m' + str(text) + '\033[0m'


def blue(text) -> str:
    """
    Wrap the text with blue color.
    Args:
        text: input text
    Returns: red text
    """
    return '\033[1;94m' + str(text) + '\033[0m'

__all__ = (
    'BaseColor',
    'FourBitColor',
    'EightBitColor',
    'Two4BitColor',
    'color', 'c4', 'c4b', 'c4d', 'c4db',
    'c8', 'c8b',
    'c24', 'c24b',
    'set_color_bit',
    'RESET', 'reset',
    'green', 'red', 'yellow', 'blue'
)
