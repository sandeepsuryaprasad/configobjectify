from pathlib import Path
from configparser import ConfigParser
from typing import Optional


class Config:
    """Provides a convenient way to access configuration values by section.
    The class reads configuration data from `config.ini` and exposes
    configuration keys through attribute access. A configuration section
    is selected when the instance is created, and individual values can
    then be accessed using the `value` property.

    Args:
        section: Name of the configuration section to access.

    Raises:
        KeyError: If the specified section does not exist in the
            configuration file.
    """

    def __init__(self, filepath: str, section: str):
        self.section: str = section.upper()
        self.config_file = self._get_config_file(filepath)
        self._parser: ConfigParser = self._get_parser()
        self._data: dict = self._parse_to_dict
        self._attr: Optional[str] = None

    def _get_config_file(self, filename) -> Path:
        path = Path(filename)
        if not path.is_file():
            raise FileNotFoundError(f"{filename!r} not found")
        if not path.suffix.lower() == ".ini":
            raise ValueError(f"Invalid file extension: {path.suffix!r}")
        return path

    def _get_parser(self) -> ConfigParser:
        """Return a configured `ConfigParser` instance.
        The parser reads configuration data from `config.ini`.
        """
        parser = ConfigParser()
        parser.read(self.config_file)
        return parser

    @property
    def _parse_to_dict(self) -> dict:
        """Return the selected configuration section as a dictionary.
        Each configuration key in the selected section is stored as a
        key-value pair in the returned dictionary.

        Returns:
            A dictionary containing the configuration values for the
            selected section.

        Raises:
            KeyError: If the selected section does not exist.
        """
        if not self._parser.has_section(self.section):
            raise KeyError(f"Invalid section {self.section}")
        return self._parser[self.section]

    @property
    def value(self):
        """Return the value of the most recently accessed configuration key.
        Returns:
            The configuration value associated with the accessed key,
            or an empty string if the key does not exist.
        """
        return self._data.get(self._attr, "")

    def __getattr__(self, name):
        """Capture access to an undefined attribute.
        The attribute name is stored internally and the current
        `Config` instance is returned, allowing configuration values
        to be accessed through expressions such as `config.device_name.value`.

        Args:
            name: Name of the configuration attribute being accessed.

        Returns:
            The current `Config` instance.
        """
        self._attr = name
        return self

    def __repr__(self):
        """Return the string representation of the configuration object.
        Returns:
            A string containing the selected configuration section.
        """
        return f'Config("{self.section}")'