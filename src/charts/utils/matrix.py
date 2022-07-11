from typing import List, Tuple, Optional, Union
import pandas as pd
import numpy as np


def getParamNames(data: List[str]) -> Tuple[List[str], int]:
    """
    Parses all parameter names from correlation data.
    :param List[str] data: Data frame from correlation matrix text file.
    :return List[str], int: List of parameter names, correlation matrix pointer.
    """
    paramNames = []
    index = 1
    # End of params ends with \n
    while data[index] != "\n":
        paramNames.append(data[index].split(" ")[0])
        index += 1
    return paramNames, index + 4


def processRow(row: List[Union[str, float]]) -> List[float]:
    """
    Reverse row using two pointers and converts entries to float.
    Also removes first & last element which is always a newline.
    :param List[str] row: Row of data, will be converted to a list of floats, hence the union.
    :return List[float]: Reverse row of "floated" data.
    """
    head, tail = 1, len(row) - 2
    while head <= tail:
        row[head] = float(row[head]) * 100
        row[tail] = float(row[tail]) * 100
        head += 1
        tail -= 1
    return row[1:-1]


def getMatrix(data: List[str], pointer: int) -> List[Optional[List[float]]]:
    """
    Convert matrix text into 2D array of strings.
    :param List[str] data: Data frame from correlation matrix text file.
    :param int pointer: Pointer to correlation matrix start.
    :return List[List[str]]: Correlation matrix with string entries.
    """
    matrix = []
    while data[pointer] != "\n":
        row = data[pointer].split("   ")
        matrix.append(processRow(row))
        pointer += 1
    return matrix


def processData(data: List[str]):
    """
    Process data from
    :param List[str] data: Data frame from correlation matrix text file.
    :return List[str], List[List[str]]: List of headers, correlation matrix with string entries.
    """
    headers, pointer = getParamNames(data)
    matrix = getMatrix(data, pointer)
    return headers, matrix
