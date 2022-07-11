from src.charts.chart import Chart
from src.charts.utils import matrix as util

import plotly.graph_objects as go


class MatrixChart(Chart):
    def __init__(self, filepath: str, relative=True):
        super().__init__()

        # Load and process data
        self.readTxt(filepath, relative)

        self.headers, self.matrix = util.processData(self.data)

        # Create figure
        self.fig = go.Figure(data=go.Heatmap(
            z=self.matrix,
            x=self.headers,
            y=self.headers,
            hoverongaps=False))

        self.show()


MatrixChart(
    r"D:\Visium\uploads\download\Fits\tHbb_v34_v2.txt",
    False)
