"""
This module contains validators for the Random.org API.

Class:
    - EnumMethod,
    - BaseRandomORG, RandomValidator,
    - Uuid4Validator, BlobsValidator, StringsValidator,
    - GaussValidator, DecimalValidator, IntValidator, IntSeqValidator

Type hints:
    - UUID4_api_key,
    - Float_1M_Range,
    - Int_range_1B, Int_range_1_10000, Int_range_1_1000, Int_range_1_100,
    - Int_range_1_32, Int_range_1_14, Int_range_2_14,
    - list_tuple, IntSeq_max_min,
    - Length_list_tuple, Length,
    - Str_range_1_32,
    - Format, Base
"""


from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field, AfterValidator, field_validator, model_validator, Json
from typing_extensions import Annotated, Literal, Union

# @formatter:off
UUID4_api_key       = Annotated[str, AfterValidator(lambda v: UUID(v).__str__())]

Float_1M_Range      = Annotated[float, Field(..., ge=-1_000_000, le=1_000_000)]

Int_range_1B        = Annotated[int, Field(..., ge=-10 ** 9, le=10 ** 9)]
Int_range_1_10000   = Annotated[int, Field(..., ge=1, le=10_000)]
Int_range_1_1000    = Annotated[int, Field(..., ge=1, le=1_000)]
Int_range_1_100     = Annotated[int, Field(..., ge=1, le=100)]
Int_range_1_32      = Annotated[int, Field(..., ge=1, le=32)]
Int_range_1_14      = Annotated[int, Field(..., ge=1, le=14)]
Int_range_2_14      = Annotated[int, Field(..., ge=2, le=14)]

list_tuple          = Annotated[list[Int_range_1B] | tuple[Int_range_1B], Field(..., max_items=1_000)]
IntSeq_max_min      = Annotated[Union[Int_range_1B, list_tuple], Field(..., union_mode='left_to_right')]

Length_list_tuple   = Annotated[list[Int_range_1_10000] | tuple[Int_range_1_10000], Field(..., max_items=1_000)]
Length              = Annotated[Union[Int_range_1_10000, Length_list_tuple], Field(..., union_mode='left_to_right')]

Str_range_1_32      = Annotated[str, Field(..., min_length=1, max_length=32)]

Format              = Literal['base64', 'hex']
Base                = Literal[2, 8, 10, 6]


class EnumMethod(Enum):
    """
    Enum class 'EnumMethod' contains the methods for the Random.org API.

    Attributes:
        - Int:      'generateIntegers'
        - IntSeq:   'generateIntegerSequences'
        - Decimal:  'generateDecimalFractions'
        - Gauss:    'generateGaussians'
        - Strings:  'generateStrings'
        - Uuid4:    'generateUUIDs'
        - Blobs:    'generateBlobs'
        - Usage:    'getUsage'
    """
    Int     = 'generateIntegers'
    IntSeq  = 'generateIntegerSequences'
    Decimal = 'generateDecimalFractions'
    Gauss   = 'generateGaussians'
    Strings = 'generateStrings'
    Uuid4   = 'generateUUIDs'
    Blobs   = 'generateBlobs'
    Usage   = 'getUsage'
# @formatter:on


class BaseRandomORG(BaseModel):
    """
    Pydantic dataclass 'BaseRandomORG' validates parameters for the Random.org API key called 'getUsage' API.

    Attribute:
        - apiKey (UUID4_api_key): must be a valid UUID4 API key, e.g, '6b1e65b9-4186-45c2-8981-b77a9842c4f0'.
    """
    apiKey: UUID4_api_key

    def get_params(self) -> dict | Json:
        return self.model_dump(exclude={'method'})


class RandomValidator(BaseRandomORG):
    """
    This class is used as a base class for other validators, not for creating instances.

    Attribute:
        - apiKey (UUID4_api_key): must be a valid UUID4 API key, e.g, '6b1e65b9-4186-45c2-8981-b77a9842c4f0'.
        - n (Int_range_1_10000): must be an integer between 1 and 10000.
    """
    n: Int_range_1_10000


class Uuid4Validator(RandomValidator):
    """
    Pydantic dataclass 'Uuid4Validator' validates parameters for the Random.org API key called 'generateUUIDs' API.

    Attribute:
        - apiKey (UUID4_api_key): must be a valid UUID4 API key, e.g, '6b1e65b9-4186-45c2-8981-b77a9842c4f0'.
        - n (Int_range_1_1000): must be an integer between 1 and 1000.
    """
    n: Int_range_1_1000


class BlobsValidator(RandomValidator):
    """
    Pydantic dataclass 'Uuid4Validator' validates parameters for the Random.org API key called 'generateUUIDs' API.

    Attributes:
        - apiKey (UUID4_api_key): must be a valid UUID4 API key, e.g, '6b1e65b9-4186-45c2-8981-b77a9842c4f0'.
        - n (Int_range_1_100): must be an integer between 1 and 100.
        - size (int): must be an integer divided by 8 and in range from 1 to 2^20.
        - format (Format): optional parameter, must be either 'base64' or 'hex'.
    """
    n: Int_range_1_100
    size: int = Field(..., ge=1, le=2 * 20)
    format: Format = 'base64'

    @field_validator('size')
    @classmethod
    def size_must_be_divided_by_8(cls, v):
        if v % 8 != 0:
            raise TypeError(f'size must be divided by 8, got {v}')
        return v


class StringsValidator(RandomValidator):
    """
    Pydantic dataclass 'StringsValidator' validates parameters for the Random.org API key called 'generateStrings' API.

    Attributes:
        - apiKey (UUID4_api_key): must be a valid UUID4 API key, e.g, '6b1e65b9-4186-45c2-8981-b77a9842c4f0'.
        - n (Int_range_1_10000): must be an integer between 1 and 10000.
        - length (Int_range_1_32): must be an integer between 1 and 32.
        - characters (Str_range_1_32): must be a string with a length between 1 and 32.
    """
    length: Int_range_1_32
    characters: Str_range_1_32


class GaussValidator(RandomValidator):
    """
    Pydantic dataclass 'GaussValidator' validates parameters for the Random.org API key called 'generateGaussians' API.

    Attributes:
        - apiKey (UUID4_api_key): must be a valid UUID4 API key, e.g, '6b1e65b9-4186-45c2-8981-b77a9842c4f0'.
        - n (Int_range_1_10000): must be an integer between 1 and 10000.
        - mean (Float_1M_Range): must be a float between -1_000_000 and 1_000_000 (-1M and 1M).
        - standardDeviation (Float_1M_Range): must be a float between -1_000_000 and 1_000_000 (-1M and 1M).
        - significantDigits (Int_range_2_14): must be an integer between 2 and 14.
    """
    mean: Float_1M_Range
    standardDeviation: Float_1M_Range
    significantDigits: Int_range_2_14


class DecimalValidator(RandomValidator):
    """
    Pydantic dataclass 'DecimalValidator' validates parameters for the Random.org API key called 'generateDecimalFractions' API.

    Attributes:
        - apiKey (UUID4_api_key): must be a valid UUID4 API key, e.g, '6b1e65b9-4186-45c2-8981-b77a9842c4f0'.
        - n (Int_range_1_10000): must be an integer between 1 and 10000.
        - decimalPlaces (Int_range_1_14): must be an integer between 1 and 14.
    """
    decimalPlaces: Int_range_1_14


class IntValidator(RandomValidator):
    """
    Pydantic dataclass 'IntValidator' validates parameters for the Random.org API key called 'generateIntegers' API.

    Attributes:
        - apiKey (UUID4_api_key): must be a valid UUID4 API key, e.g, '6b1e65b9-4186-45c2-8981-b77a9842c4f0'.
        - n (Int_range_1_10000): must be an integer between 1 and 10000.
        - min (Int_range_1B): must be an integer between -10^9 and 10^9 (-1B and 1B).
        - max (Int_range_1B): must be an integer between -10^9 and 10^9 (-1B and 1B).
        - base (Base): must be either 2, 8, 10, or 6.
    """
    min: Int_range_1B
    max: Int_range_1B
    base: Base

    @model_validator(mode='after')
    def min_must_less_than_max(self):
        if self.min >= self.max:
            raise TypeError(f'min must less than max, got (min, max)=({self.min}, {self.max})')
        if self.base not in (2, 8, 10, 6):
            raise TypeError(f'base must be (2, 8, 10, 6), got {self.base}')

        return self


class IntSeqValidator(RandomValidator):
    """
    Pydantic dataclass 'IntSeqValidator' validates parameters for the Random.org API key called 'generateIntegerSequences' API.

    Attributes:
        - apiKey (UUID4_api_key): must be a valid UUID4 API key, e.g, '6b1e65b9-4186-45c2-8981-b77a9842c4f0'.
        - n (Int_range_1_1000): number for sequence, must be an integer between 1 and 1000.
        - length (Length): number for integer in each sequence, must be an integer between 1 and 10000 or a list of integers in that range.
        - min (IntSeq_max_min): minimum range for integer in each sequence, must be an integer between -10^9 and 10^9 (-1B and 1B) or a list of integers in that range.
        - max (IntSeq_max_min): maximum range for integer in each sequence, must be an integer between -10^9 and 10^9 (-1B and 1B) or a list of integers in that range.
        - base (Base): must be either 2, 8, 10, or 6.
    """
    n: Int_range_1_1000
    length: Length
    min: IntSeq_max_min
    max: IntSeq_max_min
    base: Base

    @field_validator('length', 'min', 'max')
    @classmethod
    def iter_to_list(cls, v):
        if isinstance(v, int):
            return v
        return list(v)

    @model_validator(mode='after')
    def min_must_less_than_max(self) -> 'IntSeqValidator':
        if isinstance(self.min, list | tuple) and isinstance(self.max, list | tuple):
            if any(each_min >= each_max for each_min, each_max in zip(self.min, self.max)):
                raise TypeError(f'EVERY NUMBER in an Iterable \'min\' must smaller EVERY NUMBER in an Iterable \'max\'')
            if len(self.min) != len(self.max):
                raise TypeError(f'\'min\' and \'max\' must have the same length')

        if isinstance(self.min, int) and isinstance(self.max, list | tuple):
            if any(self.min >= i for i in self.max):
                raise TypeError(f'\'min\'={self.min} must greater than EVERY NUMBER in an Iterable \'max\'')

        if isinstance(self.max, int) and isinstance(self.min, list | tuple):
            if any(self.max <= i for i in self.min):
                raise TypeError(f'\'max\'={self.max} must smaller than EVERY NUMBER in an Iterable \'min\'')

        if isinstance(self.max, int) and isinstance(self.min, int):
            if self.min >= self.max:
                raise TypeError(f'\'min\'={self.min} must be smaller than \'max\'={self.max}')

        return self
