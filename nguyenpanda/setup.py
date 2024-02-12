from setuptools import setup, find_packages

# noinspection PyInterpreter
setup(
    name='nguyenpanda',
    version='0.1.0',
    description='nguyenpanda libray contains some utility package',
    long_description='''
    - butterfly: random packages
    - owl: mathematical packages
    - swan: beautiful packages
    ''',
    url='https://github.com/nguyenpanda',
    packages=find_packages(),
    author='Tuong Nguyen Ha',
    author_email='nguyen.hatuong0107@hcmut.edu',
    install_requires=[
        'numpy',
        'requests'
    ],
)
