"""Module to hold various utils."""

from pathlib import Path
from typing import Optional

PYPROJECT_FILENAME = "pyproject.toml"


def path_contains_pyproject(path: Path) -> bool:
    """Determine whether a `pyproject.toml` exists in the given path.

    Args:
        path (Path): the path in which to search for the `pyproject.toml`

    Returns:
        A boolean to indicate whether a `pyproject.toml` exists in the given path
    """
    return (path / PYPROJECT_FILENAME).is_file()


def get_pyproject_path() -> Optional[Path]:
    """Search for a `pyproject.toml` starting from the `cwd` and traversing up the tree.

    Returns:
        The `Path` to the `pyproject.toml` if it exists or `None` if it doesn't
    """
    cwd: Path = Path.cwd()

    for path in [cwd, *cwd.parents]:
        if path_contains_pyproject(path):
            return path / PYPROJECT_FILENAME

    return None
