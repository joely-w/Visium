from typing import List, Tuple

import numpy as np
import pandas as pd


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
    return np.array(paramNames), index + 4


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
    df = pd.DataFrame(matrix, columns=headers, index=headers)
    return df


def columnCheck(column: List[any]) -> bool:
    """
    Check if column should be shown.
    :return bool: True = remove column, False = keep column.
    """
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
    matrix = getMatrix(data, pointer, headers)
    upper = matrix.where(np.triu(np.ones(matrix.shape), k=1).astype(np.bool))
    to_drop = dict()
    for i in range(len(upper.columns)):
        if columnCheck(upper[upper.columns[i]]):
            to_drop[upper.columns[i]] = i
    matrix.drop(list(to_drop.keys()), axis=0, inplace=True)
    matrix.drop(list(to_drop.keys()), axis=1, inplace=True)
    headers = np.delete(headers, list(to_drop.values()), axis=0)
    return headers.tolist(), matrix
