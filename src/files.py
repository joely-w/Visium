import zipfile
import os
from collections import deque
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import json

from src.utilities import Node, dfs


class Files:
    def __init__(self, path):
        self.path = path
        pass

    def delete(self):
        pass

    def unzip(self, file):
        pass

    def upload(self, file: FileStorage) -> dict:
        """
        Uploads file to objects path.
        TODO handle re uploading files.
        TODO add validation for ZIP only along with failure information.
        :param FileStorage file: Target file to upload.
        :return dict: Converted file tree structure
        """
        filepath = os.path.join(self.path, secure_filename(file.filename))
        try:
            file.save(filepath)
        except:
            return {}

        return self.traverse(filepath).toJson()

    def traverse(self, filepath: str) -> Node:
        """
        Convert all filepaths within zip contained in `filepath` into a tree structure for frontend.
        :return Node: Root node for tree structure.
        """
        root = Node('root', [])
        with zipfile.ZipFile(filepath, 'r') as zf:
            files = zf.namelist()
            for file in files:
                dfs(root, deque(file.split('/')))
        return root
