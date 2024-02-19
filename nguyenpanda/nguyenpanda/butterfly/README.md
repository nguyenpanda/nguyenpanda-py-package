# Module for interacting with the Random.org API

Although the Random.org API provides a Python client library called 'rdoclient' ([GitHub](https://github.com/RandomOrg/JSON-RPC-Python.git)), I have decided to create my own client library for the API.

This project serves as an opportunity for me to practice object-oriented programming (OOP), utilize Pydantic for data validation, and interact with APIs.

Please note that while this library may not be complete, I am committed to updating it regularly. If you encounter any bugs or issues, please don't hesitate to contact me via email.

Additionally, this library can also serve as a learning resource for beginners who are just starting to learn about APIs and Pydantic. While it may not be perfect, we can exchange ideas and provide feedback via email. I can provide guidance and support to help you understand the code.

# RandomOrg API

This package is a wrapper for the RandomOrg API. It allows you to generate random numbers, strings, and UUIDs. It also allows you to generate random numbers from atmospheric noise.

## 1. Install the package
```bash
pip install nguyenpanda
```

## 2. Import the package
```python
from nguyenpanda.butterfly import RandomORG
```

## 3. Generate RandomORG instance
```python
generator = RandomORG(api_key='ENTER_YOUR_API_KEY')
```


We provide the following **_methods_** for generating random data:

- **usage**: Get usage statistics for the Random.org API.
- **uuid4**: Generate UUIDs.
- **blobs**: Generate blobs of random binary data.
- **strings**: Generate random strings.
- **decimal**: Generate random decimal fractions.
- **gauss**: Generate random numbers following a Gaussian distribution.
- **randint**: Generate random integers within a specified range.
- **randint_seq**: Generate sequences of random integers.

## Example
```python
print(f"Random.randint: {generator.randint(1, 3, 6)}")
print(f"Random.randint_seq: {generator.randint_seq(3, 4, 3, 4)}")
print(f"Random.Usage: {generator.Usage()}")
print(f"Random.Uuid4: {generator.Uuid4(2)}")
print(f"Random.Blobs: {generator.Blobs(3, 16)}")
print(f'Random.Strings: {generator.Strings(3, 32, "nguyenpanda")}')
print(f"Random.Decimal: {generator.Decimal(3, 14)}")
print(f"Random.Gauss: {generator.Gauss(3, 0, 1, 14)}")
```
