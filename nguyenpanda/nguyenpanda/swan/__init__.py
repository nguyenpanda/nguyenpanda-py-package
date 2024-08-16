"""
🦢 swan
    Indulge in the beauty of aesthetics and user interfaces with the elegant swan package.
    Dive into the world of colors, front-end development, GUI, and more.
    Transform your applications into visual masterpieces with swan.

    - ColorClass: class that contains color codes and methods to print colored text to the console.
    - Color: an instance of ColorClass.
"""

from .color import BaseColor, FourBitColor, EightBitColor, Two4BitColor

color: BaseColor = FourBitColor()
c8: BaseColor = EightBitColor()
c8b: BaseColor = EightBitColor(is_foreground=False)
c24: BaseColor = Two4BitColor()
c24b: BaseColor = Two4BitColor(is_foreground=False)

__all__ = (
    'BaseColor',
    'FourBitColor',
    'EightBitColor',
    'Two4BitColor',
    'color',
    'c8', 'c8b',
    'c24', 'c24b'
)
