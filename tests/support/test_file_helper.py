from os import path

from file_finder import FileFinder


class TestFileFinder:

    def test_find_file(self):
        file = FileFinder.resolve("app_config.cfg")
        assert path.exists(file)
        assert path.isfile(file)
