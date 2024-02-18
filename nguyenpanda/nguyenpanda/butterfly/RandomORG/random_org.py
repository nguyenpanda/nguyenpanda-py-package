"""
This module contains the RandomORG class, which is used to interact with the Random.org API.

Classe:
    RandomORG: A class for interacting with the Random.org API.
"""

from typing import Any

import requests

from .random_org_validator import (
    EnumMethod,
    BaseRandomORG,
    Uuid4Validator,
    BlobsValidator,
    StringsValidator,
    DecimalValidator,
    GaussValidator,
    IntValidator,
    IntSeqValidator,
)
from .random_org_validator import (
    UUID4_api_key,
    Base,
    Length,
    Format,
    Str_range_1_32,
    Int_range_1B,
    Int_range_1_10000,
    Int_range_1_1000,
    Int_range_1_100,
    Int_range_1_32,
    Int_range_1_14,
    Int_range_2_14,
    IntSeq_max_min,
    Float_1M_Range,
)

# Constants for the Random.org API
URL: str = "https://api.random.org/json-rpc/2/invoke"
HEADERS: dict = {"Content-Type": "application/json"}
BASE_DATA: dict = {"jsonrpc": "2.0", "id": 42}


class ErrorResponse(Exception):
    """Error in responding data from the Random.org API."""

    def __init__(self, result: dict):
        """
        Initialize the ErrorResponse object.

        :param result: The dictionary containing the error result.
        :type result: dict
        """
        self.result = result
        super().__init__(f"Error in response: {result}")


class HttpRequestError(Exception):
    """Error request from the Random.org API."""

    def __init__(self, status_code: int):
        """
        Initialize the HttpRequestError object.

        :param status_code: The status code of the HTTP request.
        :type status_code: int
        """
        self.status_code = status_code
        super().__init__(f"HTTP request failed with status code: {status_code}")


class RandomORG:
    """
    Class for interacting with the Random.org API.

    Although the Random.org API provides a Python client library called 'rdoclient'
    'rdoclient': (https://github.com/RandomOrg/JSON-RPC-Python.git),
    I have decided to create my own client library for the API.

    This project serves as an opportunity for me to practice object-oriented programming (OOP),
    utilize Pydantic for data validation, and interact with APIs.

    Please note that while this library may not be complete,
    I am committed to updating it regularly.
    If you encounter any bugs or issues, please don't hesitate to contact me via email.

    Additionally, this library can also serve as a learning resource for beginners
    who are just starting to learn about APIs and Pydantic.
    """

    def __init__(self, api_key: UUID4_api_key) -> None:
        """
        Initialize the RandomORG object.

        :param api_key: The API key for accessing Random.org services,
            must be 36 characters (letters, numbers, and hyphens).
        :type api_key: str
        """
        self.api_key = BaseRandomORG(apiKey=api_key).apiKey

    @classmethod
    def _get_data(cls, _response: requests.Response) -> Any:
        """
        Extract data from the API response.

        :param requests.Response _response: The response object from the API request.

        :return: The extracted data from the response.
        :rtype: Any

        :raises Exception: If there is an error in the API response.
        """
        result = _response.json()

        if "error" in result:
            raise ErrorResponse(result["error"]["message"])

        if "result" in result and "random" in result["result"]:
            return result["result"]["random"]["data"]

        raise ErrorResponse(result)

    @classmethod
    def _request(cls, json_data: dict) -> requests.Response:
        """
        Make a request to the Random.org API.

        :param dict json_data: The JSON data to be sent in the request.

        :return: The response object from the API post-request.
        :rtype: requests.Response

        :raises Exception: If the HTTP request fails.
        """
        _response = requests.post(URL, json=json_data, headers=HEADERS, timeout=10)
        if _response.status_code != 200:
            raise HttpRequestError(_response.status_code)
        return _response

    def _call_api_method(self, method: EnumMethod, params: dict) -> Any:
        """
        Call a specific method of the Random.org API.

        :param EnumMethod method: The method to call.
        :param dict params: A dictionary containing the parameters for the method.

        :return: The result of the API call.
        :rtype: Any

        :raises Exception: If there is an error in the API response.
        """
        data = BASE_DATA
        data["method"] = method.value
        data["params"] = params

        response = self._request(data)
        return self._get_data(response)

    def usage(self) -> dict:
        """
        Get usage statistics for the Random.org API.

        :return: A dictionary containing usage statistics.
        :rtype: dict

        :raises Exception: If there is an error in the API response.
        """
        data = BASE_DATA
        data["method"] = EnumMethod.Usage.value
        data["params"] = BaseRandomORG(apiKey=self.api_key).get_params()
        result = RandomORG._request(data).json()

        if "error" in result:
            raise ErrorResponse(result["error"]["message"])

        if "result" not in result:
            raise ErrorResponse(result)

        return result["result"]

    def uuid4(self, _n: Int_range_1_10000) -> list[str] | str:
        """
        Generate UUIDs.

        :param int _n: The number of UUIDs to generate, range [1, 1_000].

        :return: A list of UUIDs or a single UUID.
        :rtype: list[str] | str

        :raises Exception: If there is an error in the API response.
        """
        params = Uuid4Validator(apiKey=self.api_key, n=_n).get_params()
        result = self._call_api_method(EnumMethod.Uuid4, params)
        return result if len(result) > 1 else result[0]

    def blobs(
        self, _n: Int_range_1_100, _size: int, _format: Format = "base64"
    ) -> list[str] | str:
        """
        Generate blobs of random binary data.

        :param int _n: The number of blobs to generate, range [1, 100].
        :param int _size: The size of each blob in bytes,
            range [1, 2^20] and divisible by 8.
        :param str _format: The format of the blobs ('base64' or 'hex'). Defaults to 'base64'.

        :return: A list of blobs or a single blob.
        :rtype: list[str] | str

        :raises Exception: If there is an error in the API response.
        """
        params = BlobsValidator(
            apiKey=self.api_key, n=_n, size=_size, format=_format
        ).get_params()
        result = self._call_api_method(EnumMethod.Blobs, params)
        return result if len(result) > 1 else result[0]

    def strings(
        self,
        _n: Int_range_1_10000,
        _length: Int_range_1_32,
        _characters: Str_range_1_32,
    ) -> list[str] | str:
        """
        Generate random strings.

        :param int _n:
            The number of strings to generate, range [1, 10_000].
        :param int _length:
            The length of each string, range [1, 32].
        :param str _characters:
            The characters to use for generating the strings, length in range [1, 32].

        :return: A list of strings or a single string.
        :rtype: list[str] | str

        :raises Exception: If there is an error in the API response.
        """
        params = StringsValidator(
            apiKey=self.api_key, n=_n, length=_length, characters=_characters
        ).get_params()
        result = self._call_api_method(EnumMethod.Strings, params)
        return result if len(result) > 1 else result[0]

    def decimal(
        self, _n: Int_range_1_10000, _decimal_places: Int_range_1_14
    ) -> list[float] | float:
        """
        Generate random decimal fractions.

        :param int _n: The number of decimal fractions to generate, range [1, 10_000].
        :param int _decimal_places: The number of decimal places, range [1, 14].

        :return: A list of decimal fractions or a single decimal fraction.
        :rtype: list[float] | float

        :raises Exception: If there is an error in the API response.
        """
        params = DecimalValidator(
            apiKey=self.api_key, n=_n, decimalPlaces=_decimal_places
        ).get_params()
        result = self._call_api_method(EnumMethod.Decimal, params)
        return result if len(result) > 1 else result[0]

    def gauss(
        self,
        _n: Int_range_1_10000,
        _mean: Float_1M_Range,
        _standard_deviation: Float_1M_Range,
        _significant_digits: Int_range_2_14,
    ) -> list[float] | float:
        """
        Generate random numbers following a Gaussian distribution.

        :param int _n: The number of random numbers to generate, range [1, 10_000].
        :param float _mean: The mean (μ) of the Gaussian distribution, range [-1M, 1M].
        :param float _standard_deviation: The standard deviation (σ)
            of the Gaussian distribution, range [-1M, 1M].
        :param int _significant_digits: The number of significant digits, range [2, 14].

        :return: A list of random numbers or a single random number.
        :rtype: list[float] | float

        :raises Exception: If there is an error in the API response.
        """
        params = GaussValidator(
            apiKey=self.api_key,
            n=_n,
            mean=_mean,
            standardDeviation=_standard_deviation,
            significantDigits=_significant_digits,
        ).get_params()
        result = self._call_api_method(EnumMethod.Gauss, params)
        return result if len(result) > 1 else result[0]

    def randint(
        self,
        _n: Int_range_1_10000,
        _min: Int_range_1B,
        _max: Int_range_1B,
        _base: Base = 10,
    ) -> list[int] | int:
        """
        Generate random integers within a specified range.

        :param int _n: The number of random integers to generate, range [1, 10_000].
        :param int _min: The minimum value (inclusive) of the range, range [-1B, 1B].
        :param int _max: The maximum value (inclusive) of the range, range [-1B, 1B].
        :param int _base: The base of the random numbers (2, 8, 10, or 6). Defaults to 10.

        :return: A list of random integers or a single random integer.
        :rtype: list[int] | int

        :raises Exception: If there is an error in the API response.
        """
        params = IntValidator(
            apiKey=self.api_key, n=_n, min=_min, max=_max, base=_base
        ).get_params()
        result = self._call_api_method(EnumMethod.Int, params)
        return result if len(result) > 1 else result[0]

    def randint_seq(
        self,
        _n: Int_range_1_1000,
        _length: Length,
        _min: IntSeq_max_min,
        _max: IntSeq_max_min,
        _base: Base = 10,
    ) -> list[int] | int:
        """
        Generate sequences of random integers.

        :param int _n: The number of sequences to generate, range [1, 1_000].
        :param Union[int, List[int]] _length: The lengths of the sequences requested [1 to 10000].
            It can be a list or tuple of integer in that range.
        :param Union[int, List[int]] _min: The minimum of the sequences requested [-1e9 to 1e9].
            It can be a list or tuple of integer in that range.
        :param Union[int, List[int]] _max: The maximum of the sequences requested [-1e9 to 1e9].
            It can be a list or tuple of integer in that range.
        :param int _base: The base of the random numbers (2, 8, 10, or 6). Defaults to 10.

        :return: A list of sequences of random integers or a single sequence.
        :rtype: list[int] | int

        :raises Exception: If there is an error in the API response.
        """
        params = IntSeqValidator(
            apiKey=self.api_key, n=_n, length=_length, min=_min, max=_max, base=_base
        ).get_params()
        result = self._call_api_method(EnumMethod.IntSeq, params)
        return result if len(result) > 1 else result[0]
