from setuptools import setup, find_packages
import info

# noinspection PyInterpreter
setup(
    name='nguyenpanda',
    version=info.__version__,
    description=info.__description__,
    long_description=info.long_description,
    url=info.__url__,
    packages=find_packages(),
    author=info.__author__,
    author_email=info.__email__,
    install_requires=info.install_requires
)
