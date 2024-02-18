"""
Module for interacting with the Random.org API.

Although the Random.org API provides a Python client library called 'rdoclient'
    (https://github.com/RandomOrg/JSON-RPC-Python.git),
    I have decided to create my own client library for the API.

This project serves as an opportunity for me to practice
    object-oriented programming (OOP),
    utilize Pydantic for data validation, and interact with APIs.

Please note that while this library may not be complete,
    I am committed to updating it regularly.
If you encounter any bugs or issues,
    please don't hesitate to contact me via email.

Additionally, this library can also serve as a learning resource
    for beginners who are just starting to learn about APIs and Pydantic.
    While it may not be perfect, we can exchange ideas and provide feedback via email,
    I can provide guidance and support to help you understand the code.
"""

from .random_org import RandomORG

# @formatter:off
from .random_org_validator import (
    # Type hints
    Int_range_1B, Int_range_1_10000, Int_range_1_1000, Int_range_1_100,
    Int_range_1_32, Int_range_1_14, Int_range_2_14, list_tuple, IntSeq_max_min,
    Float_1M_Range, Length_list_tuple, Length,
    Str_range_1_32, Format, Base, UUID4_api_key,

    # Enum
    EnumMethod,

    # Pydantic validators
    BaseRandomORG, RandomValidator, Uuid4Validator,
    BlobsValidator, StringsValidator, GaussValidator,
    DecimalValidator, IntValidator, IntSeqValidator,
)

__all__ = [
    # Main
    'RandomORG',
    'EnumMethod',
    # Type hints
    'Int_range_1B', 'Int_range_1_10000', 'Int_range_1_1000', 'Int_range_1_100',
    'Int_range_1_32', 'Int_range_1_14', 'Int_range_2_14',
    'list_tuple', 'IntSeq_max_min', 'Float_1M_Range',
    'Length_list_tuple', 'Length', 'Str_range_1_32', 'Format', 'Base', 'UUID4_api_key',
    # Pydantic validators
    'BaseRandomORG',
    'RandomValidator', 'Uuid4Validator', 'BlobsValidator', 'StringsValidator',
    'GaussValidator', 'DecimalValidator', 'IntValidator', 'IntSeqValidator',
]
# @formatter:on
