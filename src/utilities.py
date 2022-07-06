"""
TODO refactor this out into separate more relevant files.
"""
import math
import json
import copy
from typing import List, Tuple, Deque, Optional


# Tree structure to convert the file list to
class Node:
    def __init__(self, val, children: Optional[List], rootpath):

        self.id, self.text = '/'.join(rootpath), val
        if children:
            self.type = 'folder'
            self.children = children
        else:
            self.type = 'file'
            self.children = []

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def addChild(self, el) -> None:
        self.type = 'folder'
        self.children.append(el)


def dfs(root: Node, path: Deque[str], rootpath: List[str] = []) -> None:
    """
    Populate tree with all elements (folders and files) in path.
    This populates in place so no return needed.
    :param rootpath: Path for node from root
    :param Node root: Root node
    :param path: Double ended queue which stores the current path to traverse
    :return None:
    """
    if len(path) == 0:
        return None
    # Get child node
    node = path.popleft()
    rootpath.append(node)
    for el in root.children:
        if el.text == node:
            dfs(el, path, rootpath)
            rootpath.pop()
            return
    el = Node(node, [], rootpath)
    root.addChild(el)
    dfs(el, path, rootpath)
    rootpath.pop()
    return





