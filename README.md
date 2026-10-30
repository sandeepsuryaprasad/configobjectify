## configobjectify

[![CI](https://github.com/sandeepsuryaprasad/configobjectify/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/sandeepsuryaprasad/configbjectify/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/configobjectify)](https://pypi.org/project/configobjectify/)

A lightweight Python library that provides an object-oriented 
interface for accessing values from INI configuration files. Instead of retrieving 
values using dictionary-style or section-based lookups, you can access configuration 
keys through dot notation.

## Installation
```console
pip install configobjectify
```

## Usage
Consider the following `config.ini` file,
```console
[APPLE]
device_name = iPhone
model = iPhone 17
os_version = 26.0

[GOOGLE]
device_name = Pixel
model = Pixel 10
os_version = 16
```

```console
>>> from configobjectify import Config
>>> config = Config("config.ini", "APPLE")
>>> config.device_name.value
'iPhone'
>>> config.model.value
'iPhone 17'
>>> config.os_version.value
'26.0'
```
### Selecting a different section
```console
>>> config = Config("config.ini", "GOOGLE")
>>> config.device_name.value
'Pixel'
>>> config.model.value
'Pixel 10'
>>> config.os_version.value
'16.0'
```
NOTE: Section names are normalized to uppercase by the library before lookup.

### Handling missing configuration keys
```console
>>> config = Config("config.ini", "APPLE")
>>> config.country_of_origin.value
>>> ''
```

### Installed version
To get to know the version of `configobjectify`,
```console
>>> import configobjectify
>>> print(configobjectify.__version__)
```
or
```console
>>> from configobjectify import __version__
>>> print(__version__)
```

### Requirements
* Python 3.12 or later

### Contributing
Contributions, bug reports, and feature suggestions are welcome. Please open an issue to 
discuss a proposed change before submitting a pull request.

### License

This package is distributed under the terms of [MIT](https://github.com/sandeepsuryaprasad/configobjectify/blob/main/LICENSE) license

