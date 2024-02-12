import os

from setuptools import setup, find_packages


def read(file_name: str) -> str:
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


# noinspection PyInterpreter
setup(
    name='nguyenpanda',
    version='0.1.2',
    author='Tường Nguyên Hà',
    author_email='hatuongnguyen0107@gmail.com',
    description='Welcome to the world of \'nguyenpanda\', a Python library that brings you the essence of utility packages, each named after animals, perfectly representing its unique domain.',
    license='MIT',
    keywords='nguyenpanda tuong nguyen hcmut panda',
    url='https://github.com/nguyenpanda',
    packages=find_packages(),
    long_description=read('README.md'),
    install_requires=[
        'numpy',
        'requests'
    ],
    project_urls={
        'Source Code': 'https://github.com/nguyenpanda/PyPackages',
    },
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
