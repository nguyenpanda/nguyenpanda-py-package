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
    Base, Length, Format,
    Str_range_1_32,
    Int_range_1B, Int_range_1_10000, Int_range_1_1000, Int_range_1_100,
    Int_range_1_32, Int_range_1_14, Int_range_2_14,
    IntSeq_max_min, Float_1M_Range,
)

# Constants for the Random.org API
URL: str = "https://api.random.org/json-rpc/2/invoke"
HEADERS: dict = {"Content-Type": "application/json"}
BASE_DATA: dict = {"jsonrpc": "2.0", "id": 42}


class RandomORG:
    """
    Class for interacting with the Random.org API.

    Although the Random.org API provides a Python client library called 'rdoclient' (https://github.com/RandomOrg/JSON-RPC-Python.git),
    I have decided to create my own client library for the API.

    This project serves as an opportunity for me to practice object-oriented programming (OOP), utilize Pydantic for data validation, and interact with APIs.

    Please note that while this library may not be complete, I am committed to updating it regularly.
    If you encounter any bugs or issues, please don't hesitate to contact me via email.

    Additionally, this library can also serve as a learning resource for beginners who are just starting to learn about APIs and Pydantic.
    While it may not be perfect, we can exchange ideas and provide feedback via email, I can provide guidance and support to help you understand the code.
    """

    def __init__(self, api_key: UUID4_api_key) -> None:
        """Initialize the RandomORG object.

        Args:
            api_key (str): The API key for accessing Random.org services. Must contain 36 characters (char, num, -).
        """
        self.api_key = BaseRandomORG(apiKey=api_key).apiKey

    @classmethod
    def _get_data(cls, _response: requests.Response) -> Any:
        """Extract data from the API response.

        Args:
            _response (requests.Response): The response object from the API request.

        Returns:
            Any: The extracted data from the response.

        Raises:
            Exception: If there is an error in the API response.
        """
        result = _response.json()

        if "error" in result:
            raise Exception("Error in response: ", result["error"]["message"])

        if "result" in result and "random" in result["result"]:
            return result["result"]["random"]["data"]
        else:
            raise Exception("Error in response: ", result)

    @classmethod
    def _request(cls, json_data: dict) -> requests.Response:
        """Make a request to the Random.org API.

        Args:
            json_data (dict): The JSON data to be sent in the request.

        Returns:
            requests.Response: The response object from the API post-request.

        Raises:
            Exception: If the HTTP request fails.
        """
        _response = requests.post(URL, json=json_data, headers=HEADERS)
        if _response.status_code != 200:
            raise Exception(
                f"HTTP request failed with status code: {_response.status_code}"
            )
        return _response

    def _call_api_method(self, method: EnumMethod, params: dict) -> Any:
        """Call a specific method of the Random.org API.

        Args:
            method (EnumMethod): The method to call.
            params: A dictionary containing the parameters for the method.

        Returns:
            Any: The result of the API call.

        Raises:
            Exception: If there is an error in the API response.
        """
        data = BASE_DATA
        data["method"] = method.value
        data["params"] = params

        response = self._request(data)
        return self._get_data(response)

    def Usage(self) -> dict:
        """Get usage statistics for the Random.org API.

        Returns:
            dict: A dictionary containing usage statistics.

        Raises:
            Exception: If there is an error in the API response.
        """
        data = BASE_DATA
        data["method"] = EnumMethod.Usage.value
        data["params"] = BaseRandomORG(apiKey=self.api_key).get_params()
        result = RandomORG._request(data).json()

        if "error" in result:
            raise Exception("Error in response: ", result["error"]["message"])

        if "result" not in result:
            raise Exception("Error in response: ", result)

        return result["result"]

    def Uuid4(self, _n: Int_range_1_10000) -> list[str] | str:
        """Generate UUIDs.

        Args:
            _n (int): The number of UUIDs to generate, range [1, 1_000].

        Returns:
            list[str] | str: A list of UUIDs or a single UUID.

        Raises:
            Exception: If there is an error in the API response.
        """
        params = Uuid4Validator(apiKey=self.api_key, n=_n).get_params()
        result = self._call_api_method(EnumMethod.Uuid4, params)
        return result if len(result) > 1 else result[0]

    def Blobs(
        self, _n: Int_range_1_100, _size: int, _format: Format = "base64"
    ) -> list[str] | str:
        """Generate blobs of random binary data.

        Args:
            _n (int): The number of blobs to generate, range [1, 100].
            _size (int): The size of each blob in bytes, range [1, 2^20] and divisible by 8.
            _format (str, optional): The format of the blobs ('base64' or 'hex'). Defaults to 'base64'.

        Returns:
            list[str] | str: A list of blobs or a single blob.

        Raises:
            Exception: If there is an error in the API response.
        """
        params = BlobsValidator(
            apiKey=self.api_key, n=_n, size=_size, format=_format
        ).get_params()
        result = self._call_api_method(EnumMethod.Blobs, params)
        return result if len(result) > 1 else result[0]

    def Strings(
        self,
        _n: Int_range_1_10000,
        _length: Int_range_1_32,
        _characters: Str_range_1_32,
    ) -> list[str] | str:
        """Generate random strings.

        Args:
            _n (int): The number of strings to generate, range [1, 10_000].
            _length (int): The length of each string, range [1, 32].
            _characters (str): The characters to use for generating the strings, length in range [1, 32].

        Returns:
            list[str] | str: A list of strings or a single string.

        Raises:
            Exception: If there is an error in the API response.
        """
        params = StringsValidator(
            apiKey=self.api_key, n=_n, length=_length, characters=_characters
        ).get_params()
        result = self._call_api_method(EnumMethod.Strings, params)
        return result if len(result) > 1 else result[0]

    def Decimal(self,
                _n: Int_range_1_10000,
                _decimal_places: Int_range_1_14) -> list[float] | float:
        """Generate random decimal fractions.

        Args:
            _n (int): The number of decimal fractions to generate, range [1, 10_000].
            _decimal_places (int): The number of decimal places, range [1, 14].

        Returns:
            list[float] | float: A list of decimal fractions or a single decimal fraction.

        Raises:
            Exception: If there is an error in the API response.
        """
        params = DecimalValidator(
            apiKey=self.api_key, n=_n, decimalPlaces=_decimal_places
        ).get_params()
        result = self._call_api_method(EnumMethod.Decimal, params)
        return result if len(result) > 1 else result[0]

    def Gauss(
        self,
        _n: Int_range_1_10000,
        _mean: Float_1M_Range,
        _standard_deviation: Float_1M_Range,
        _significant_digits: Int_range_2_14,
    ) -> list[float] | float:
        """Generate random numbers following a Gaussian distribution.

        Args:
            _n (int): The number of random numbers to generate, range [1, 10_000].
            _mean (float): The mean (μ) of the Gaussian distribution, range [-1M, 1M].
            _standard_deviation (float): The standard deviation (σ) of the Gaussian distribution, range [-1M, 1M].
            _significant_digits (int): The number of significant digits, range [2, 14].

        Returns:
            list[float] | float: A list of random numbers or a single random number.

        Raises:
            Exception: If there is an error in the API response.
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
        """Generate random integers within a specified range.

        Args:
            _n (int): The number of random integers to generate, range [1, 10_000].
            _min (int): The minimum value (inclusive) of the range, range [-1B, 1B].
            _max (int): The maximum value (inclusive) of the range, range [-1B, 1B].
            _base (int, optional): The base of the random numbers (2, 8, 10, or 6). Defaults to 10.

        Returns:
            list[int] | int: A list of random integers or a single random integer.

        Raises:
            Exception: If there is an error in the API response.
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
        """Generate sequences of random integers.

        Args:
            _n (int): The number of sequences to generate, range [1, 1_000].
            _length (Union[int, List[int]]): The lengths of the sequences requested (1 to 10000).
            _min (Union[int, List[int]]): The lower boundaries of the sequences requested (-1e9 to 1e9).
            _max (Union[int, List[int]]): The upper boundaries of the sequences requested (-1e9 to 1e9).
            _base (int, optional): The base of the random numbers (2, 8, 10, or 6). Defaults to 10.

        Returns:
            list[int] | int: A list of sequences of random integers or a single sequence.

        Raises:
            Exception: If there is an error in the API response.
        """
        params = IntSeqValidator(
            apiKey=self.api_key, n=_n, length=_length, min=_min, max=_max, base=_base
        ).get_params()
        result = self._call_api_method(EnumMethod.IntSeq, params)
        return result if len(result) > 1 else result[0]

