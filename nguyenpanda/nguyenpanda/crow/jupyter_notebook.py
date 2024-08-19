import os
import sys
from pathlib import Path
from typing import Union


class NoteBookUtils:
    """
    A utility class for common tasks in Jupyter notebooks, such as creating symbolic links (aliases)
    and detecting the Google Colab environment.
    """

    @classmethod
    def create_alias(cls, source_path: str | Path, alias_name: str, alias_path: str | Path = Path.cwd(),
                     verbose: bool = True) -> Path:
        """
        Creates a symbolic link (alias) to the specified source directory.

        Args:
            source_path (Union[str, Path]): The path to the directory to be linked.
            alias_name (str): The name of the alias to be created.
            alias_path (Union[str, Path], optional): The directory where the alias should be created. Defaults to the current working directory.
            verbose (bool, optional): Whether to print status messages. Defaults to True.

        Returns:
            Path: The absolute path to the created alias directory.

        Raises:
            RuntimeError: If the command to create the alias fails.
            NotImplementedError: If the operating system is not supported.
            PermissionError: If the operation requires elevated permissions (common on Windows in Jupyter notebooks).
        """
        alias_path = (Path(alias_path) / alias_name).absolute()
        source_path = Path(source_path).absolute()

        if alias_path.is_dir():
            if verbose:
                print(f'\033[1;93mDirectory \"\033[1;92m{alias_path}\033[1;93m\" already exists!\033[0m')
            return alias_path

        if os.name == 'nt':  # Windows NT
            command = f'mklink /D "{alias_path}" "{source_path}"'
        elif os.name == 'posix':  # macOS and Linux (including Google Colab)
            command = f'ln -s "{source_path}" "{alias_path}"'
        else:
            raise NotImplementedError('Unsupported OS')

        if verbose:
            print(f'\033[1;92m{command}\033[0m')

        try:
            exit_status = os.system(command)
            if exit_status != 0:
                raise RuntimeError(f'Failed to create alias. Command exited with status {exit_status}')
        except PermissionError as e:
            if os.name == 'nt' and 'Jupyter' in sys.modules:
                raise PermissionError(
                    'Creating symbolic links requires elevated permissions '
                    'on Windows when running in a Jupyter notebook. '
                    'Please run your notebook as Administrator.') from e
            else:
                raise

        return alias_path

    @classmethod
    def is_colab(cls) -> bool:
        """
        Checks if the current environment is Google Colab.

        Returns:
            bool: True if the code is running on Google Colab, otherwise False.
        """
        return os.getenv("COLAB_RELEASE_TAG") is not None


nb_utils: NoteBookUtils = NoteBookUtils()
nbu: NoteBookUtils = nb_utils
