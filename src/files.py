import zipfile
import os
from collections import deque
from typing import List

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from utilities import Node, dfs


class Files:
    def __init__(self, path):
        self.path = path
        pass

    def pdf(self, folder_name, filepath):
        return os.path.join(self.path, folder_name, filepath)

    def list(self) -> List[str]:
        return [name for name in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, name))]

    def upload(self, file: FileStorage) -> dict:
        """
        Uploads file to objects path.
        TODO handle re uploading files.
        TODO add validation for ZIP only along with failure information.
        :param FileStorage file: Target file to upload.
        :return dict: Converted file tree structure
        """
        filepath = os.path.abspath(os.path.join(self.path, secure_filename(file.filename)))
        try:
            file.save(filepath)
            with zipfile.ZipFile(filepath, "r") as zf:
                zf.extractall(filepath.split('.')[0])
        except:
            return {}

        return dict(name=secure_filename(file.filename).split(".")[0])
        # self.traverse(filepath).toJson()

    def access(self, folder_name):
        filepath = os.path.join(self.path, secure_filename(folder_name + '.zip'))
        res = self.traverse(filepath)
        return res.toJson()

    def traverse(self, filepath: str) -> Node:
        """
        Convert all filepaths within zip contained in `filepath` into a tree structure for frontend.
        :return Node: Root node for tree structure.
        """
        root = Node('root', [], [])
        with zipfile.ZipFile(filepath, 'r') as zf:
            files = zf.namelist()
            for file in files:
                dfs(root, deque(file.split('/')))
        return root
