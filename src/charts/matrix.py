from typing import Tuple, List

import numpy as np
import plotly.graph_objects as go
from pandas import DataFrame

from src.charts.chart import Chart
from src.charts.utils import matrix as util


class MatrixChart(Chart):
    def __init__(self, filepath1: str, filepath2: str = None, relative=True):
        super().__init__()

        # Load and process data
        self.readTxt(filepath1, relative)

        self.headers1, self.matrix1 = util.processData(self.data[0])

        if filepath2:
            self.readTxt(filepath2, relative)
            self.headers2, self.matrix2 = util.processData(self.data[1])
            headers, matrix = self.mergeMatrices()
        else:
            headers, matrix = self.headers1, self.matrix1

        headers, matrix = util.dropMatrix(matrix, headers)

        # Make friendly
        matrix = matrix.values.tolist()

        self.fig = go.Figure(data=go.Heatmap(
            z=matrix,
            x=headers,
            y=headers,
            hoverongaps=False, zmin=-100, zmax=100, text=matrix, texttemplate="%{text}",
            colorscale='RdBu_r'
        ))

    def mergeMatrices(self) -> Tuple[List[str], DataFrame]:
        """
        Make matrices the same size by filling each matrix with empty column and row if it does not contain header.
        If matrices have identical columns in different positions then first occurring position chosen.
        """
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
                    value = util.findElement(self.matrix1, headers[i], headers[j])
                    matrix[j][i] = value
                else:
                    value = util.findElement(self.matrix2, headers[i], headers[j])
                    matrix[j][i] = value
        return headers, DataFrame(matrix, columns=headers, index=headers)

    def nuisanceParams(self):
        pass
