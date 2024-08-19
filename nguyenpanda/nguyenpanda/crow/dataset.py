import os
import subprocess
from pathlib import Path
from typing import Optional

from typing_extensions import Self

from .exception import InvalidKaggleAPI, KaggleAuthenticationFailed
from .google_colab import gcu
from .jupyter_notebook import nbu
from ..swan import green, yellow

if nbu.is_colab():
    from google.colab import files


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
        os.system('unzip {}.zip -d "{}"'.format(api.split('/')[-1], self.dataset_source_dir.as_posix()))

        return self

    def alias(self, source: Optional[str | Path] = None, destination: str | Path = Path.cwd(), verbose: bool = True) -> Path:
        if source is None:
            source = self.dataset_source_dir
        if isinstance(destination, str):
            destination = Path(destination)
            if not destination.is_dir():
                destination.mkdir(parents=True)

        return nbu.create_alias(source_path=source, alias_name=self.name or Path(source).name,
                                alias_path=destination, verbose=verbose)
