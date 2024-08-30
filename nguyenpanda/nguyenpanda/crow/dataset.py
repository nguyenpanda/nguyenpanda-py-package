import os
import subprocess
import zipfile
from collections import deque
from pathlib import Path
from typing import Optional

from typing_extensions import Self

from .exception import InvalidKaggleAPI, KaggleAuthenticationFailed
from .google_colab import gcu
from .jupyter_notebook import nbu
from ..swan import green, yellow, red

if nbu.is_colab():
    from google.colab import files

try:
    import kaggle
except ModuleNotFoundError as e:
    print(red('Please install kaggle package by this command "pip install kaggle"'))
except OSError as e:
    print(yellow(e))


class Dataset:
    """
    A class to manage Kaggle datasets, including downloading and preparing them for use
    in Machine Learning and Deep Learning projects.
    """

    def __init__(self, name: Optional[str] = None):
        """
        Initializes the Dataset class.

        Args:
            name (Optional[str]): The name of the dataset. Defaults to None.
        """
        self.name = name
        self.in_colab: bool = nbu.is_colab()
        self.dataset_source_dir: Optional[Path] = None
        self.alias_path: Optional[Path] = None

    def __str__(self) -> str:
        """
        Returns a string representation of the Dataset object.

        Returns:
            str: The string representation of the Dataset object.
        """
        return ('{}(name={}, in_colab={}, dataset_source_dir={})'.
                format(self.__class__.__name__, self.name, self.in_colab, self.dataset_source_dir))

    def kaggle(self, api: str, to_path: str | Path = Path.cwd(), verbose: bool = True) -> Self:
        """
        Downloads a dataset from Kaggle using the provided API command.

        Args:
            api (str): The Kaggle API command to download the dataset.
            to_path (Union[str, Path], optional): The directory where the dataset will be downloaded. Defaults to the current working directory.
            verbose (bool, optional): Whether to print status messages. Defaults to True.

        Returns:
            Self: The current Dataset instance.

        Raises:
            InvalidKaggleAPI: If the API command does not follow the expected pattern.
            KaggleAuthenticationFailed: If the Kaggle authentication fails.
            RuntimeError: If the download fails for reasons other than authentication.
        """
        tokens = api.split(' ')
        if len(tokens) != 5 or tokens[:4] != ['kaggle', 'datasets', 'download', '-d']:
            raise InvalidKaggleAPI(api)

        self.dataset_source_dir = Path(to_path).resolve()
        self.dataset_source_dir = to_path / (self.name or tokens[-1].split('/')[-1])

        if not self.dataset_source_dir.is_dir():
            self.dataset_source_dir.mkdir(parents=True)
        else:
            return self

        if self.in_colab and not (Path.cwd() / 'kaggle.json').is_file():
            print(yellow('Please upload your Kaggle API JSON file'))
            gcu.notification()
            files.upload()
            os.system('mkdir ~/.kaggle')
            os.system('cp kaggle.json ~/.kaggle/')
            os.system('chmod 600 ~/.kaggle/kaggle.json')

        if verbose:
            print(green('Downloading Kaggle dataset...'))
        result = subprocess.run(api, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            if '403 - Forbidden' in result.stderr or 'Unauthorized' in result.stderr:
                raise KaggleAuthenticationFailed()
            else:
                raise RuntimeError(f'Failed to download the Kaggle dataset: {result.stderr}')

        if verbose:
            print(green('Unzipping Kaggle Dataset...'))
        with zipfile.ZipFile(api.split('/')[-1] + '.zip', 'r') as zip_ref:
            zip_ref.extractall(self.dataset_source_dir.as_posix())

        return self

    def alias(self, source: Optional[str | Path] = None, destination: str | Path = Path.cwd(),
              exist_ok: bool = False, verbose: bool = True) -> Self:
        """
        Creates a symbolic link (alias) to the dataset directory.

        If the `source` is not provided, the method will use `self.dataset_source_dir`.
        If both `source` and `self.dataset_source_dir` are None, a ValueEror is raised.

        Args:
            source (Optional[Union[str, Path]], optional): The source directory to create an alias for.
                                                           If None, `self.dataset_source_dir` is used.
                                                           Defaults to None.
            destination (Union[str, Path], optional): The destination where the alias should be created.
                                                      Defaults to the current working directory.
            exist_ok (bool): Allow overwriting alias if True.
            verbose (bool, optional): Whether to print status messages. Defaults to True.

        Returns:
            Path: The path to the created alias.

        Raises:
            ValueError: If both `source` and `self.dataset_source_dir` are None.
            PermissionError: If creating the alias fails due to permissions.
            RuntimeError: If creating the alias fails for other reasons.
        """
        if source is None and self.dataset_source_dir is None:
            raise ValueError('There is no dataset directory to point to')

        if self.dataset_source_dir is None:
            self.dataset_source_dir = source
        if source is None:
            source = self.dataset_source_dir

        destination = Path(destination) if isinstance(destination, str) else destination
        if not destination.is_dir():
            destination.mkdir(parents=True)

        self.alias_path = nbu.create_alias(source_path=source,
                                           alias_name=self.name or Path(source).name,
                                           alias_path=destination,
                                           exist_ok=exist_ok, verbose=verbose)

        return self

    @staticmethod
    def bfs_find(target: str = 'datasets', search_path: Path = None,
                 strict: bool = True, verbose: bool = True) -> Optional[Path]:
        """
        Performs a breadth-first search (BFS) to locate a directory by name.

        Args:
            target (str, optional): The directory name to search for. Defaults to 'datasets'.
            search_path (Path, optional): The root directory where the search begins.
                                          If running in Google Colab, defaults to the current working directory.
                                          If not specified, default to the user's home directory.
            strict (bool, optional): If True, the search is case-sensitive and looks for an exact match.
                                     If False, the search is case-insensitive and allows partial matches. Defaults to True.
            verbose (bool, optional): If True, print the search progress. Defaults to True.

        Returns:
            Optional[Path]: The path to the found directory if it exists, or None if not found.
        """
        ignore = {'Library', 'Applications', 'bin', 'Documents', 'Movies', 'Music', 'Pictures',
                  'venv', 'env', 'lib', 'build', 'cmake-build-debug', 'numpy'}
        exclude_extensions = {'.photoslibrary', '.ignore', '__', 'env'}
        exclude_prefix = {'.', '__', 'env'}

        def is_valid_dir(p: Path):
            return (p.is_dir() and
                    p.stem not in ignore and
                    not any(p.name.endswith(ext) for ext in exclude_extensions) and
                    not any(p.name.startswith(ext) for ext in exclude_prefix))

        if search_path is None:
            search_path = Path.cwd() if nbu.is_colab() else Path.home()

        queue = deque([search_path])
        target = target.lower() if not strict else target
        total_check = 0

        while queue:
            current_dir = queue.popleft()
            for path in filter(is_valid_dir, current_dir.glob('[!.*]*')):
                if (strict and path.stem == target) or (not strict and target in path.stem.lower()):
                    return path
                queue.append(path)
                total_check += 1
                if verbose and total_check % 300 == 0:
                    print(f'Total checked: {total_check} | {path}', end='\n')

        if verbose:
            print(red('\nDirectory not found.'))
        return None
