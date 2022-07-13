from os import path

import yaml

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

        try:
            print(filepath, flush=True)
            with open(filepath, "r") as stream:
                self.data = yaml.safe_load(stream)
                return True
        except FileNotFoundError or yaml.YAMLError:
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
        try:
            print(filepath, flush=True)
            with open(filepath, "r") as stream:
                self.data = stream.readlines()
                return True
        except FileNotFoundError:
            return False
