from typing import Tuple, List

import numpy as np
import plotly.graph_objects as go
from pandas import DataFrame
from plotly.subplots import make_subplots

from src.charts.chart import Chart
from src.charts.utils import matrix as util


class MatrixChart(Chart):
    def __init__(self, filepath1: str, filepath2: str = None, relative=True):
        super().__init__()
        self.fig = make_subplots(rows=2, cols=2, specs=[[{"type": "heatmap", "colspan": 2}, None],
                                                        [{"type": "scatter"}, {"type": "scatter"}]])
        # Load and process data
        self.readTxt(filepath1, relative)

        self.headers1, self.matrix1 = util.processData(self.data[0])

        if filepath2:
            self.readTxt(filepath2, relative)
            self.headers2, self.matrix2 = util.processData(self.data[1])
            titles, matrix = self.mergeMatrices()
        else:
            titles, matrix = self.headers1['paramNames'], self.matrix1
            self.headers2, self.matrix2 = None, None
        titles, matrix = util.dropMatrix(matrix, titles)
        # Make friendly
        matrix = matrix.values.tolist()
        self.nuisanceParams()
        self.fig.update_traces(colorbar_orientation='h', selector=dict(type='heatmap'))
        self.fig.update_layout(coloraxis_colorbar_x=-0.15)
        self.fig.add_trace(go.Heatmap(
            z=matrix,
            x=titles,
            y=titles,
            hoverongaps=False, zmin=-100, zmax=100, text=matrix, texttemplate="%{text}",
            colorscale='RdBu_r'
        ), row=1, col=1)

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
        # Now to generate the scatter plot
        self.fig.add_trace(
            go.Scatter(name='ratio', y=self.headers1['paramNames'],
                       x=self.headers1['nuisance'],
                       showlegend=False, mode='markers', error_x=dict(symmetric=False, array=self.headers1['error_up'],
                                                                      arrayminus=self.headers1['error_down'])),
            row=2, col=1)
        if self.headers2:
            self.fig.add_trace(
                go.Scatter(name='ratio', y=self.headers1['paramNames'],
                           x=self.headers1['nuisance'],
                           showlegend=False, mode='markers',
                           error_x=dict(symmetric=False, array=self.headers2['error_up'],
                                        arrayminus=self.headers2['error_down'])),
                row=2, col=2)
        pass
