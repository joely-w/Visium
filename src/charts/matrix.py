from typing import Union

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from src.charts.chart import Chart
from src.charts.utils import matrix as util


class MatrixChart(Chart):
    def __init__(self, filepath1: str, filepath2: str = None, relative=True):
        super().__init__()

        # Load and process data
        self.readTxt(filepath1, relative)
        self.headers1, self.matrix1 = self.getData(0)
        if filepath2:
            self.readTxt(filepath2, relative)
            self.headers2, self.matrix2 = self.getData(1)

        headers, matrix = self.mergeMatrices()
        self.fig = go.Figure(data=go.Heatmap(
            z=matrix,
            x=headers,
            y=headers,
            hoverongaps=False, zmin=-100, zmax=100, text=matrix, texttemplate="%{text}",
            colorscale='RdBu_r'
        ))

    def getData(self, data_index: int):
        return util.processData(self.data[data_index])

    def mergeMatrices(self):
        """
        Make matrices the same size by filling each matrix with empty column and row if it does not contain header.
        If matrices have identical columns in different positions then first occurring position chosen.
        """
        if self.matrix2 is None:
            return

        # We now create a new matrix, and populate it with values from matrix1 and matrix2.

        # List of all unique parameters
        headers = list(set(self.matrix1.columns).union(set(self.matrix2.columns)))
        # Our target matrix
        matrix = np.zeros(shape=(len(headers), len(headers)))
        # Think of this double loop as iterating through every element in our new matrix
        for j in range(len(headers)):
            for i in range(len(headers)):
                # Check if we are in upper or lower triangle
                if i == j:
                    matrix[j][i] = 100.0
                elif i > j:
                    value = self.findElement(self.matrix1, headers[i], headers[j])
                    matrix[j][i] = value
                else:
                    value = self.findElement(self.matrix2, headers[i], headers[j])
                    matrix[j][i] = value
        return headers, matrix.tolist()

    def findElement(self, matrix: pd.DataFrame, column: str, row: str) -> Union[float, str]:
        try:
            return matrix[row][column]
        except KeyError:
            return -999