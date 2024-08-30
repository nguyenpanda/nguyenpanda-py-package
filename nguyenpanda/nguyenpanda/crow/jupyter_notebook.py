import os
from pathlib import Path
from typing import Union

from ..swan import green, yellow, blue


class NoteBookUtils:
    """
    A utility class for common tasks in Jupyter notebooks, such as creating symbolic links (aliases)
    and detecting the Google Colab environment.
    """

    @classmethod
    def create_alias(cls, source_path: str | Path, alias_name: str, alias_path: str | Path = Path.cwd(),
                     exist_ok: bool = False, verbose: bool = True) -> Path:
        """
        Creates a symbolic link (alias) to the specified source directory.

        Args:
            source_path (Union[str, Path]): The path to the directory to be linked.
            alias_name (str): The name of the alias to be created.
            alias_path (Union[str, Path], optional): The directory where the alias should be created. Defaults to the current working directory.
            exist_ok (bool): Allow to overwrite if True
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

        if alias_path.exists():
            if verbose:
                print(yellow('Directory'), blue(alias_path), yellow(' already exists!'))
            if exist_ok:
                if verbose:
                    print(yellow('Removing exist alias'), blue(alias_path) + yellow('!'))
                alias_path.unlink()

        try:
            alias_path.symlink_to(target=source_path)
            if verbose:
                print(green(f'Creating an alias {blue(source_path)} -> {blue(alias_path)}'))
        except FileExistsError:
            pass

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
