"""
butterfly module contains anything related to randomness, probability, and statistics.
Small things can have non-linear impacts on a complex system, so don't let the butterfly fly away.

Classes:
    - RandomORG module for interacting with the Random.org API.
"""

from .RandomORG import RandomORG

__all__ = [
    "RandomORG",
]
