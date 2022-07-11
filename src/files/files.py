import yaml
from os import path

from .. import definitions


class File:
    def __init__(self):
        self.data = None
        pass

    def readYaml(self, filepath, relative=True):
        """
        :param str filepath: Path to file. If relative=True (default) then path should be relative to project root,
        otherwise path should be absolute. Data is loaded into self.data property.
        :param bool relative: Defaults to True, sets whether filepath should be treated as relative or absolute.
        :return:
        """
        if relative:
            filepath = path.join(definitions.ROOT_DIR, filepath)

        with open(filepath, "r") as stream:
            try:
                self.data = yaml.safe_load(stream)
                return True
            except yaml.YAMLError or FileNotFoundError:
                return False

    def readTxt(self, filepath, relative=True):
        """
        :param str filepath: Path to file. If relative=True (default) then path should be relative to project root,
        otherwise path should be absolute. Data is loaded into self.data property.
        :param bool relative: Defaults to True, sets whether filepath should be treated as relative or absolute.
        :return:
        """
        if relative:
            filepath = path.join(definitions.ROOT_DIR, filepath)

        with open(filepath, "r") as stream:
            try:
                self.data = stream.readlines()
                return True
            except FileNotFoundError:
                return False
