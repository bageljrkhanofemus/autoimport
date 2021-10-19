"""Tests for the `Config` classes."""

from typing import Callable
from unittest.mock import MagicMock, patch

import toml

from autoimport.config import AutoImportConfig, Config


class TestConfig:
    """Tests for the `Config` class."""

    def test_get_valid_option(self) -> None:
        """
        Given: a `Config` instance with a `config_dict` populated,
        When a value is retrieved for an existing option,
        Then the value of the option is returned
        """
        config_dict = {"foo": "bar"}
        config = Config(config_dict=config_dict)

        result = config.get_option("foo")

        assert result == "bar"

    def test_get_value_for_missing_option(self) -> None:
        """
        Given: a `Config` instance with a `config_dict` populated,
        When: a value is retrieved for a option not defined in the `config_dict`,
        Then: `None` is returned
        """
        config_dict = {"foo": "bar"}
        config = Config(config_dict=config_dict)

        result = config.get_option("baz")

        assert result is None

    def test_get_value_for_no_config_dict(self) -> None:
        """
        Given: a `Config` instance without a given `config_dict`,
        When: a value is retrieved for an option,
        Then: `None` is returned
        """
        config = Config()

        result = config.get_option("foo")

        assert result is None


class TestAutoImportConfig:
    """Tests for the `AutoImportConfig`."""

    @patch("autoimport.config.get_pyproject_path")
    def test_valid_pyproject(
        self, mock_get_pyproject_path: MagicMock, create_tmp_file: Callable
    ) -> None:
        """
        Given: a valid `pyproject.toml`,
        When: the `AutoImportConfig` class is instantiated,
        Then: a config value can be retrieved
        """
        config_toml = toml.dumps({"tool": {"autoimport": {"foo": "bar"}}})
        pyproject_path = create_tmp_file(content=config_toml, filename="pyproject.toml")
        mock_get_pyproject_path.return_value = pyproject_path
        autoimport_config = AutoImportConfig()

        result = autoimport_config.get_option("foo")

        assert result == "bar"

    @patch("autoimport.config.get_pyproject_path")
    def test_no_pyproject(self, mock_get_pyproject_path: MagicMock) -> None:
        """
        Given: no supplied `pyproject.toml`,
        When: the `AutoImportConfig` class is instantiated,
        Then: the situation is handled gracefully
        """
        mock_get_pyproject_path.return_value = None
        autoimport_config = AutoImportConfig()

        result = autoimport_config.get_option("foo")

        assert result is None

    @patch("autoimport.config.get_pyproject_path")
    def test_valid_pyproject_with_no_autoimport_section(
        self, mock_get_pyproject_path: MagicMock, create_tmp_file: Callable
    ) -> None:
        """
        Given: a valid `pyproject.toml`,
        When: the `AutoImportConfig` class is instantiated,
        Then: a config value can be retrieved
        """
        config_toml = toml.dumps({"foo": "bar"})
        pyproject_path = create_tmp_file(content=config_toml, filename="pyproject.toml")
        mock_get_pyproject_path.return_value = pyproject_path
        autoimport_config = AutoImportConfig()

        result = autoimport_config.get_option("foo")

        assert result is None
