from typing import List, Tuple

import numpy as np
import pandas as pd


def findElement(matrix: pd.DataFrame, column: str, row: str) -> float:
    """
    Find an element in a matrix.
    :param pd.Dataframe matrix: Matrix to search
    :param str column: Column of element
    :param str row: Row of element
    :returns float: If element exists in matrix, returns value. Otherwise, returns -999 (not found).
    """
    try:
        return matrix[row][column]
    except KeyError:
        return -999


def getParamNames(data: List[str]) -> Tuple[np.array, int]:
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


def getMatrix(data: List[str], pointer: int, headers: any) -> pd.DataFrame:
    """
    Convert matrix text into 2D array of strings.
    TODO tidy up.
    :param List[str] data: Data frame from correlation matrix text file.
    :param int pointer: Pointer to correlation matrix start.
    :return List[List[str]]: Correlation matrix with string entries.
    """
    matrix = []
    while data[pointer] != "\n":
        raw_row = np.array(data[pointer].replace("\n", "").split("   "))
        # Remove last element and reverse
        row = raw_row[:-1][::-1].astype(float)

        matrix.append(np.around(100.0 * row, decimals=3))
        pointer += 1
    return pd.DataFrame(matrix, columns=headers, index=headers)


def columnCheck(column: List[any], index: int) -> bool:
    """
    Check if column should be shown.
    :return bool: True = remove column, False = keep column.
    """
    for count, element in enumerate(column):
        if index == count:
            continue
        if abs(element) >= 20:
            return False
    return True


def dropMatrix(matrix: pd.DataFrame, headers: List[str]):
    """
    Drops row/columns of matrix that don't contain a PMCC > 30 .
    """

    to_drop = dict()
    for i in range(len(matrix.columns)):
        if columnCheck(matrix[matrix.columns[i]], i):
            to_drop[matrix.columns[i]] = i
    matrix.drop(list(to_drop.keys()), axis=0, inplace=True)
    matrix.drop(list(to_drop.keys()), axis=1, inplace=True)
    headers = np.delete(headers, list(to_drop.values()), axis=0)
    return headers.tolist(), matrix
    pass


def processData(data: List[str]) -> Tuple[List[str], pd.DataFrame]:
    """
    Obtain matrix and corresponding parameters from data.
    TODO extract nuisance values from data.
    """
    headers, pointer = getParamNames(data)
    return headers, getMatrix(data, pointer, headers)
