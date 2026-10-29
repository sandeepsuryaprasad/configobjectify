from importlib.metadata import version
from .config import Config

__version__ = version("configobjectify")

__all__ = ["Config", "__version__"]