"""Module to hold the `AutoImportConfig` class definition."""

from pathlib import Path
from typing import Any, Dict, Optional

import toml

from autoimport.utils import get_pyproject_path


class Config:
    """Defines the base `Config` and provides accessors to get config values."""

    def __init__(self, config_dict: Optional[Dict[str, Any]] = None) -> None:
        """Initialize the config."""
        self._config_dict: Dict[str, Any] = config_dict or {}

    def get_option(self, option: str) -> Optional[str]:
        """Return the value of a config option.

        Args:
            option (str): the config option for which to return the value

        Returns:
            The value of the given config option or `None` if it doesn't exist
        """
        return self._config_dict.get(option)


class AutoImportConfig(Config):
    """Defines the autoimport `Config`."""

    def __init__(self) -> None:
        """Initialize the config."""
        self.config_values: Optional[Dict[str, Any]] = _find_config()
        super().__init__(config_dict=self.config_values)


def _find_config() -> Optional[Dict[str, Any]]:
    """Search for a config file and return a dict of the values if it exists."""
    pyproject_path: Optional[Path] = get_pyproject_path()
    if pyproject_path:
        return toml.load(pyproject_path).get("tool", {}).get("autoimport")

    return None


autoimport_config: AutoImportConfig = AutoImportConfig()
