from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field, AfterValidator, field_validator, model_validator, Json
from typing_extensions import Annotated, Literal, Union

# @formatter:off
Int_range_1_10000   = Annotated[int, Field(..., ge=1, le=10_000)]
Int_range_1_1000    = Annotated[int, Field(..., ge=1, le=1_000)]
Int_range_1_100     = Annotated[int, Field(..., ge=1, le=100)]
Int_range_1_32      = Annotated[int, Field(..., ge=1, le=32)]
Int_range_1_14      = Annotated[int, Field(..., ge=1, le=14)]
Int_range_2_14      = Annotated[int, Field(..., ge=2, le=14)]
Int_range_1B        = Annotated[int, Field(..., ge=-10 ** 9, le=10 ** 9)]

list_tuple          = Annotated[list[Int_range_1B] | tuple[Int_range_1B], Field(..., max_items=1_000)]
IntSeq_max_min      = Annotated[Union[Int_range_1B, list_tuple], Field(..., union_mode='left_to_right')]

Float_1M_Range      = Annotated[float, Field(..., ge=-1_000_000, le=1_000_000)]

Length_list_tuple   = Annotated[list[Int_range_1_10000] | tuple[Int_range_1_10000], Field(..., max_items=1_000)]
Length              = Annotated[Union[Int_range_1_10000, Length_list_tuple], Field(..., union_mode='left_to_right')]
Str_range_1_32      = Annotated[str, Field(..., min_length=1, max_length=32)]

Format              = Literal['base64', 'hex']
Base                = Literal[2, 8, 10, 6]
UUID4_api_key       = Annotated[str, AfterValidator(lambda v: UUID(v).__str__())]
# @formatter:on

class EnumMethod(Enum):
    # @formatter:off
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
    apiKey: UUID4_api_key

    def get_params(self) -> dict | Json:
        return self.model_dump(exclude={'method'})


class RandomValidator(BaseRandomORG):
    n: Int_range_1_10000


class Uuid4Validator(RandomValidator):
    n: Int_range_1_1000


class BlobsValidator(RandomValidator):
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
    length: Int_range_1_32
    characters: Str_range_1_32


class GaussValidator(RandomValidator):
    mean: Float_1M_Range
    standardDeviation: Float_1M_Range
    significantDigits: Int_range_2_14


class DecimalValidator(RandomValidator):
    decimalPlaces: Int_range_1_14


class IntValidator(RandomValidator):
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

