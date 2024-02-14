'''
Int, IntSeq, Dec, Gauss, Str, UUID, Blobs, Usage

apiKey
n

min, max (Int, IntSeq
length (IntSeq, str
characters (str

decimalPlaces (DecimalFractions
mean, standardDeviation, significantDigits (Gaussians
size (Blobs

base
format
'''
from enum import Enum
from typing import Iterable, Union, List

from icecream import ic
from requests import post, Response

BASE_URL: str = 'https://api.random.org/json-rpc/4/invoke'
HEADERS: dict = {'Content-Type': 'application/json'}


class API(Enum):
    Int = 'generateIntegers'
    IntSeq = 'generateIntegerSequences'
    DecFra = 'generateDecimalFractions'
    Gauss = 'generateGaussians'
    Str = 'generateStrings'
    Uuid = 'generateUUIDs'
    Blob = 'generateBlobs'
    Usage = 'getUsage'

class Params(Enum):
    Int = ('max, min', ('base', ))
    IntSeq = ('max, min', 'length', ('base', ))
    Str = ('length', ('characters', ))
    Blob = ('size', ('format', ))

class RandomORG:

    def __init__(self, api_key: str):
        assert isinstance(api_key, str), f'api_key must be a string, got {type(api_key).__name__}'
        self.__api_key: str = api_key

    def Int(self, size: int, _min: int, _max: int, base: int = 10) -> Union[list, int]:
        assert 1 <= size <= 10_000, f'size must be in range [1, 1e4], got size={size}'
        assert -1_000_000_000 <= _min <= _max <= 1_000_000_000, \
            f'_min must be smaller than _max and in range [-1e9, 1e9], got (_min, _max)={(_min, _max)}'
        assert base in {2, 8, 10, 16}, f'base must be in {2, 8, 10, 16}, got base={base}'

        params = {
            'apiKey': self.__api_key,
            'n': size,
            'min': _min,
            'max': _max,
            'base': base,
        }

        data = self.__get_respond_data(API.Int, params)

        return data if size != 1 else data[0]

    def IntSeq(self, num_of_seq: int,
               length: Union[int, Iterable[int]],
               _min: Union[int, Iterable[int]],
               _max: Union[int, Iterable[int]],
               base: int = 10) -> List[List[int]]:
        assert 1 <= num_of_seq <= 1_000, f'num_of_seq must be an integer and in range [1, 1000], got num_of_seq={num_of_seq}'

        if isinstance(length, Iterable):
            assert all(isinstance(item, int) for item in length), 'length must be an iterator of integers.'

        if isinstance(_min, Iterable):
            assert all(isinstance(item, int) for item in _min), '_min must be an iterator of integers.'

        if isinstance(_max, Iterable):
            assert all(isinstance(item, int) for item in _max), '_max must be an iterator of integers.'

        assert base in {2, 8, 10, 16}, f'base must be in {2, 8, 10, 16}, got base={base}'

        params = {
            'apiKey': self.__api_key,
            'n': num_of_seq,
            'length': length,
            'min': _min,
            'max': _max,
            'base': base,
        }

        data: List[List[int]] = self.__get_respond_data(API.IntSeq, params)

        return data

    def Usage(self) -> dict:
        params = {'apiKey': self.__api_key}

        response: Response = self.__send_post_request(api=API.Usage, params=params)
        result: dict = response.json()
        ic(result)

        assert 'result' in result, f''

        return result['result']

    @staticmethod
    def __send_post_request(api: API, params: dict) -> Response:
        json_data = {
            'jsonrpc': '2.0',
            'method': api.value,
            'params': params,
            'id': 15998
        }

        ic(json_data)

        response = post(BASE_URL, headers={'Content-Type': 'application/json'}, json=json_data)

        assert response.status_code == 200, f'HTTP request failed with status code:, {response.status_code}'
        return response

    @staticmethod
    def __get_respond_data(api: API, params: dict) -> list:
        response: Response = RandomORG.__send_post_request(api=api, params=params)

        result: dict = response.json()
        ic(result)
        assert 'result' in result and 'random' in result['result'], f''

        return result['result']['random']['data']


if __name__ == '__main__':
    intButter = RandomORG('1aaffe1a-32a9-4172-87e6-7086c5630637')
    # print(intButter.int(10, -10, 6))
    # print(intButter.int(1, -10, 6))

    # ic(intButter.IntSeq(3, 4, [1, 1, 4], [6, 6, 42]))

    ic(intButter.Usage())
