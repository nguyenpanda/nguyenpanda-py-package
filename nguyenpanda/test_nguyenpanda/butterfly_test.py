import unittest

from pydantic import ValidationError

from nguyenpanda.nguyenpanda.butterfly.RandomORG import *

API = "1aaffe1a-32a9-4072-87e6-7086c5630637"  # Fake API


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

    def test_fake_api_key(self):
        fake_api_key = "1aaffe1a-32a9-4072-87e6-7086c5630637"
        generator = RandomORG(api_key=fake_api_key)

        with self.assertRaises(ErrorResponse):
            generator.randint(1, 1, 6)

    # def test_input_validator(self):
    #     with self.assertRaises(ValidationError):
    #         generator.randint_seq(3, 4, 3, 4)
    #     with self.assertRaises(ValidationError):
    #         generator.usage()
    #     with self.assertRaises(ValidationError):
    #         generator.uuid4(2)
    #     with self.assertRaises(ValidationError):
    #         generator.blobs(3, 16)
    #     with self.assertRaises(ValidationError):
    #         generator.strings(3, 32, "nguyenpanda")
    #     with self.assertRaises(ValidationError):
    #         generator.decimal(3, 14)
    #     with self.assertRaises(ValidationError):
    #         generator.gauss(3, 0, 1, 14)


if __name__ == "__main__":
    unittest.main()
