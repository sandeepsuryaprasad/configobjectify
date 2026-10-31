from pathlib import Path

import pytest
from pytest import fixture
from configobjectify import Config

ini_contents = """
[APPLE]
device_name = iPhone
model = iPhone 17
os_version = 26.0


[GOOGLE]
device_name = Pixel
model = Pixel 10
os_version = 16
"""

invalid_identifiers = """
[APPLE]
device.name = iPhone
class = First
os version = 26.0
model-name = iPhone17
"""

@fixture
def ini_file(tmp_path: Path) -> Path:
    filename = Path.joinpath(tmp_path, "config.ini")
    filename.write_text(ini_contents, encoding="utf-8")
    return filename

@fixture
def invalid_py_identifiers_file(tmp_path: Path):
    filename = Path.joinpath(tmp_path, "config.ini")
    filename.write_text(invalid_identifiers, encoding="utf-8")
    return filename

@fixture
def text_file(tmp_path: Path) -> Path:
    filename = Path.joinpath(tmp_path, "config.txt")
    filename.write_text("Hell world", encoding="utf-8")
    return filename

def test_config_section_apple(ini_file):
    config = Config(ini_file, "APPLE")
    assert config.device_name.value == "iPhone"
    assert config.model.value == "iPhone 17"
    assert config.os_version.value == "26.0"

def test_config_section_google(ini_file):
    config = Config(ini_file, "google")
    assert config.device_name.value == "Pixel"
    assert config.model.value == "Pixel 10"
    assert config.os_version.value == "16"

def test_missing_key(ini_file):
    config = Config(ini_file, "APPLE")
    config.username.value == ""

def test_invalid_py_identifies_as_keys(invalid_py_identifiers_file):
    config = Config(invalid_py_identifiers_file, "APPLE")
    assert config.device_name.value == "iPhone"
    assert config._class.value == "First"
    assert config.os_version.value == "26.0"
    assert config.model_name.value == "iPhone17"

def test_invalid_section(ini_file):
    with pytest.raises(KeyError):
        config = Config(ini_file, "STAGING_ENV")

def test_invalid_file_extension(text_file):
    with pytest.raises(ValueError):
        config = Config(text_file, "google")
