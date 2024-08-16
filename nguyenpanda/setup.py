"""
This file is used to build the package and upload it to PyPI.
"""

import os
from pathlib import Path

from setuptools import setup, find_packages


def read(file_name: str) -> str:
    """Read README.md file."""
    with open(Path.cwd() / file_name, 'r') as f:
        return f.read()


def list_all(file_name: str) -> list[str]:
    """List all lines"""
    with open(Path.cwd() / file_name, 'r') as f:
        return f.read().splitlines()


if __name__ == '__main__':
    meta: dict = {}
    with open(os.path.join('nguyenpanda', '__version__.py')) as file:
        exec(file.read(), meta)

    print('\033[1;92mExporting README.md from inside to outside\033[0m')
    with open(Path.cwd().parent / 'README.md', 'w') as out_read_me:
        with open(Path.cwd() / 'README.md', 'r') as in_read_me:
            out_read_me.write(in_read_me.read())

    print('\033[1;92mRunning setup function\033[0m')
    setup(
        name=meta['__name__'],
        version=meta['__version__'],
        author=meta['__author__'],
        author_email=meta['__email__'],
        maintainer=meta['__maintainer__'],
        maintainer_email=meta['__maintainer_email__'],
        description=meta['__description__'],
        license=meta['__license__'],
        keywords='nguyenpanda tuong nguyen hcmut panda',
        url=meta['__url__'],
        packages=find_packages(),
        long_description=read('README.md'),
        long_description_content_type='text/markdown',
        install_requires=list_all('requirements.txt'),
        project_urls={
            'Source Code': meta['__src__'],
        },
        python_requires=meta['__python_requires__'],
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'License :: OSI Approved :: MIT License',
            'Intended Audience :: Developers',
            'Intended Audience :: Education',
            'Intended Audience :: Science/Research',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3.12',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    )
