import os
from pathlib import Path

def create_alias(source_path, alias_name, alias_path: Path | str = Path.cwd()):
    alias_path = (Path(alias_path) / alias_name).absolute()
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