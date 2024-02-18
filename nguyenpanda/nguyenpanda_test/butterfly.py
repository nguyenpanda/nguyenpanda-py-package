# noinspection PyUnresolvedReferences
from nguyenpanda.butterfly.RandomORG import RandomORG

# noinspection PyUnresolvedReferences
from nguyenpanda.butterfly.RandomORG import *
import unittest

API = input("Enter your api key from Random.org: ")


# noinspection PyUnresolvedReferences
class TestRandomORG(unittest.TestCase):
    def test_int_validator(self):
        validator = IntValidator(apiKey=API, n=100, min=10, max=20, base=10)
        self.assertEqual(validator.min, 10)
        self.assertEqual(validator.max, 20)
        self.assertEqual(validator.base, 10)

    def test_int_seq_validator(self):
        validator = IntSeqValidator(
            apiKey=API, n=100, length=[5, 10], min=[1, 2], max=[6, 12], base=10
        )
        self.assertEqual(validator.n, 100)
        self.assertEqual(validator.length, [5, 10])
        self.assertEqual(validator.min, [1, 2])
        self.assertEqual(validator.max, [6, 12])
        self.assertEqual(validator.base, 10)

    def test_uuid4_validator(self):
        validator = Uuid4Validator(apiKey=API, n=1000)
        self.assertEqual(validator.n, 1000)

    def test_blobs_validator(self):
        validator = BlobsValidator(apiKey=API, n=100, size=16)
        self.assertEqual(validator.n, 100)
        self.assertEqual(validator.size, 16)
        self.assertEqual(validator.format, "base64")

    def test_strings_validator(self):
        validator = StringsValidator(
            apiKey=API, n=100, length=32, characters="abcdefghijklmnopqrstuvwxyz"
        )
        self.assertEqual(validator.n, 100)
        self.assertEqual(validator.length, 32)
        self.assertEqual(validator.characters, "abcdefghijklmnopqrstuvwxyz")

    def test_gauss_validator(self):
        validator = GaussValidator(
            apiKey=API, n=100, mean=0.0, standardDeviation=1.0, significantDigits=4
        )
        self.assertEqual(validator.n, 100)
        self.assertEqual(validator.mean, 0.0)
        self.assertEqual(validator.standardDeviation, 1.0)
        self.assertEqual(validator.significantDigits, 4)

    def test_decimal_validator(self):
        validator = DecimalValidator(apiKey=API, n=100, decimalPlaces=6)
        self.assertEqual(validator.n, 100)
        self.assertEqual(validator.decimalPlaces, 6)


def test_random_org():
    generator = RandomORG(api_key=API)

    print(f"Random.randint: {generator.randint(1, 3, 6)}")
    print(f"Random.randint_seq: {generator.randint_seq(3, 4, 3, 4)}")
    print(f"Random.Usage: {generator.Usage()}")
    print(f"Random.Uuid4: {generator.Uuid4(2)}")
    print(f"Random.Blobs: {generator.Blobs(3, 16)}")
    print(f'Random.Strings: {generator.Strings(3, 32, "nguyenpanda")}')
    print(f"Random.Decimal: {generator.Decimal(3, 14)}")
    print(f"Random.Gauss: {generator.Gauss(3, 0, 1, 14)}")


if __name__ == "__main__":
    test_random_org()
    unittest.main()
