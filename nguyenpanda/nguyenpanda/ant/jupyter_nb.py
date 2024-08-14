import os
from pathlib import Path


def create_alias(source_path: str | Path, alias_name: str, alias_path: str | Path = Path.cwd()) -> Path:
    """

    :param source_path: Where the true directory located
    :param alias_name: The alias name
    :param alias_path: Specify the path of the alias
    :return: The path to alias
    """
    alias_path = (Path(alias_path) / alias_name).absolute()
    source_path = Path(source_path).absolute()

    if alias_path.is_dir():
        print('\033[1;93mDirectory \"\033[1;92m{}\033[1;93m\" already exist!\033[0m'.format(alias_path))
        return alias_path

    if os.name == 'nt':  # Windows NT
        command = 'mklink /D {} {}'.format(alias_path, source_path)
    elif os.name == 'posix':  # macOS-specific code
        command = 'ln -s {} {}'.format(source_path, alias_path)
    else:
        raise NotImplementedError('Unsupported OS')
    print('\033[1;92m{}\033[0m'.format(command))

    exit_status = os.system(command)
    if exit_status != 0:
        raise RuntimeError(f"Failed to create alias. Command exited with status {exit_status}")

    return alias_path
