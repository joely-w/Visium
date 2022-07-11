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
    head, tail = 0, len(row) - 1
    while head <= tail:
        row[head] = float(row[head]) * 100
        row[tail] = float(row[tail]) * 100
        head += 1
        tail -= 1
    return row


def getMatrix(data: List[str], pointer: int) -> pd.DataFrame:
    """
    Convert matrix text into 2D array of strings.
    TODO update return types to numpy.
    :param List[str] data: Data frame from correlation matrix text file.
    :param int pointer: Pointer to correlation matrix start.
    :return List[List[str]]: Correlation matrix with string entries.
    """

    matrix = []
    while data[pointer] != "\n":
        row = (np.array(data[pointer].replace("\n", "").split("   ")))[:-1][::-1].astype(float)
        matrix.append(np.around(100.0 * row, decimals=3))
        pointer += 1
    matrix = np.array(matrix)
    df = pd.DataFrame(matrix)
    return df


def columnCheck(column: List[any]) -> bool:
    for element in column:
        if not np.isnan(element) and abs(element) >= 20:
            return False
    return True


def processData(data: List[str]):
    """
    Trim all non correlated features from matrix.
    :param List[str] data: Data frame from correlation matrix text file.
    :return List[str], List[List[str]]: List of headers, correlation matrix with string entries.
    """
    headers, pointer = getParamNames(data)
    headers = np.array(headers)
    matrix = getMatrix(data, pointer)
    upper = matrix.where(np.triu(np.ones(matrix.shape), k=1).astype(np.bool))
    to_drop = [column for column in upper.columns if columnCheck(upper[column])]
    matrix.drop(to_drop, axis=0, inplace=True)
    matrix.drop(to_drop, axis=1, inplace=True)
    headers = np.delete(headers, to_drop, axis=0)
    return headers.tolist(), matrix.values.tolist()
