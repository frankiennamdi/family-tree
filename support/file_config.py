import configparser

from file_finder import FileFinder
from support.env_interpolation import EnvInterpolation


class FileConfig:
    """
        Load a .cfg file into a parser and interpolate environment variables
    """
    def __init__(self, config_file='app_config.cfg'):
        self.parser = configparser.ConfigParser(interpolation=EnvInterpolation())
        self.parser.read(FileFinder.resolve(config_file))

    def get_value(self, section, key, default=None):
        return self.parser.get(section, key, fallback=default)
