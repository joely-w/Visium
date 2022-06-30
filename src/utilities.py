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
        self.id, self.title = val, val
        self.rootpath = copy.deepcopy(rootpath)
        if children:
            self.folder = True
            self.children = children
        else:
            self.folder = False
            self.children = []

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def addChild(self, el) -> None:
        self.folder = True
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
        if el.id == node:
            dfs(el, path, rootpath)
            rootpath.pop()
            return
    el = Node(node, [], rootpath)
    root.addChild(el)
    dfs(el, path, rootpath)
    rootpath.pop()
    return


def latexName(name: str) -> str:
    """
    Converts string to string that will be rendered by Latex or treated as a standard string.
    @TODO parse entries with a +.
    :param str name: Name to convert.
    :return str: String that can be parsed by MathJax.
    """
    name_latex = name.replace('#', '\\')
    return f"${name_latex}$"


def toFloat(number: str) -> float:
    """
    Attempts to convert config to a float, returns 0 if failed.
    :param str number: Number to convert.
    :return float: Converted float.
    """
    try:
        return float(number)
    except ValueError:
        return 0


def predRatio(predicted, data) -> Tuple[float, float, float, List[float]]:
    """
    Calculates config/predicted ratio. Ratio is zero if either entry is 0.
    :param data: True data.
    :param predicted: Predicted data.
    :return Tuple[float, float, float, List[float]]: Maximum, minimum, upper error (symmetric) and data.
    """
    res = []
    maximum, minimum = 1.25, 0.5
    n = len(predicted)
    error = 0.5 * 1 / (math.sqrt(n))
    for i in range(n):
        numerator = toFloat(data[i])
        denominator = toFloat(predicted[i])
        if numerator and denominator:
            ratio = toFloat(data[i]) / predicted[i]
            if ratio > maximum:
                maximum = ratio
            if ratio < minimum:
                minimum = ratio
            res.append(ratio)
        else:
            res.append(None)
    return maximum, minimum, error, res


def calculateBins(edges: List[float]) -> Tuple[list, list]:
    """
    Calculate bin midpoints and widths given edges.
    This calculates a Plotly-friendly array of bins given a list of edges.
    :param list[float] edges: List of edges to calculate bins from.
    :return Tuple[list, list]: List of bins, list of widths of bins.
    """
    widths = []
    bins = []
    # calculate widths of bins and bin midpoints
    for i in range(len(edges) - 1):
        width = edges[i + 1] - edges[i]
        widths.append(width)
        bins.append(edges[i] + 0.5 * width)
    return bins, widths
