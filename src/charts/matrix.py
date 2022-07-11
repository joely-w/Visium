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
            hoverongaps=False, zmin=-100, zmax=100, text=self.matrix, texttemplate="%{text}"))
