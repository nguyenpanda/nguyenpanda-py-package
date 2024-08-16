import os
from pathlib import Path
import sys


def create_alias(source_path: str | Path, alias_name: str, alias_path: str | Path = Path.cwd(), verbose: bool = True) -> Path:
    """
    Creates an alias (symbolic link) to a specified directory. This is useful when working with large datasets that
    are stored on a different part of the computer and are not directly accessible from your working environment
    (e.g., Jupyter notebook, Google Colab).

    The function creates a symbolic link with the provided alias name in the specified directory. If the alias
    directory already exists, it returns the path without making any changes. The function supports Windows, macOS,
    and environments like Google Colab.

    :param source_path: The path to the directory where the actual dataset is stored. This can be a string or a Path object.
    :param alias_name: The name to be used for the alias (symbolic link).
    :param alias_path: The directory where the alias should be created. Defaults to the current working directory.
                       This can be a string or a Path object.
    :param verbose: Whether to print status messages. Defaults to True.
    :return: The absolute path to the created alias directory.
    :raises RuntimeError: If the command to create the alias fails.
    :raises NotImplementedError: If the operating system is not supported.
    :raises PermissionError: If the operation requires elevated permissions (common on Windows in Jupyter notebooks).
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
            raise RuntimeError(f"Failed to create alias. Command exited with status {exit_status}")
    except PermissionError as e:
        if os.name == 'nt' and 'Jupyter' in sys.modules:
            raise PermissionError(
                "Creating symbolic links requires elevated permissions on Windows when running in a Jupyter notebook. "
                "Please run your notebook as Administrator.") from e
        else:
            raise

    return alias_path

