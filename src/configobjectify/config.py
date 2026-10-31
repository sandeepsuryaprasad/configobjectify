import keyword
from re import sub
from configparser import ConfigParser, SectionProxy
from pathlib import Path
from typing import Optional


class Config:
    def __init__(self, filepath: str | Path, section: str):
        self.section: str = section.upper()
        self.config_file = self._get_config_file(filepath)
        self._parser: ConfigParser = self._get_parser()
        self._data: SectionProxy = self._parse_to_dict
        self._attr: Optional[str] = None

    def _get_config_file(self, filename: str | Path) -> Path:
        """Validate the configuration file path and return it as a Path object.

        Args:
        filename: Path to the configuration file.

        Returns:
        A Path object representing the validated INI file.

        Raises:
        FileNotFoundError: If the path does not point to an existing file.
        ValueError: If the file does not have an .ini extension.
        """
        path = Path(filename)
        if not path.is_file():
            raise FileNotFoundError(f"{filename!r} not found")
        if path.suffix.lower() != ".ini":
            raise ValueError(f"Invalid file extension: {path.suffix!r}")
        return path

    def _get_parser(self) -> ConfigParser:
        """Return a configured `ConfigParser` instance.
        The parser reads configuration data from `valid.ini`.
        """
        parser = ConfigParser()
        parser.read(self.config_file)
        return parser

    def _normalize_key(self, key):
        normalized_key = sub(r"[-.\s]+", "_", key)
        if keyword.iskeyword(normalized_key):
            normalized_key = "_" + normalized_key
        return normalized_key

    @property
    def _parse_to_dict(self) -> SectionProxy:
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
            raise KeyError(f"Invalid section {self.section!r}")
        temp_data = self._parser[self.section]
        return {self._normalize_key(key): value for key, value in temp_data.items()}


    @property
    def value(self) -> str:
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