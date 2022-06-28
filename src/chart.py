import json
import os
from typing import List, Optional, Tuple

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utilities import calculateBins, latexName, predRatio

script_dir = os.path.dirname(__file__)


class Chart:
    def __init__(self, data):
        # Create bar chart
        self.data = data
        self.bins, self.widths = calculateBins(data['Figure'][0]['BinEdges'])
        self.fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                                 x_title=data['Figure'][0]['XaxisLabel'],
                                 vertical_spacing=0.001, row_heights=[0.7, 0.3])
        self.fig.update_layout(barmode='stack', legend=dict(font=dict(size=20)))

        # Load colours
        try:
            with open(os.path.join(script_dir, 'colours.json')) as file:
                self.colours = json.loads(file.read())
        except FileNotFoundError:
            self.colours = {}

    def createBarChart(self) -> None:
        """
        Creates bar charts elements in graph.
        :return: None
        """
        # Create normal bars
        for i in range(len(self.data['Samples']) - 1, 1, -1):
            frame = self.data['Samples'][i]['Yield']
            name = self.data['Samples'][i]['Name']
            self.fig.add_trace(self.createBar(name, frame, self.bins, self.widths, ), row=1, col=1)
        # Add uncertainty to top bar
        error_up = self.data['Total'][0]['UncertaintyUp']
        error_down = [float(-1 * el) for el in self.data['Total'][0]['UncertaintyDown']]
        self.fig.add_trace(self.createBar(self.data['Samples'][0]['Name'], self.data['Samples'][0]['Yield'],
                                          self.bins, self.widths, (error_up, error_down)), row=1, col=1)
        self.fig.update_yaxes(title_text="Events", row=1, col=1)

    def createScatter(self) -> None:
        """
        Create scatter graph elements in chart.
        :return:
        """
        if 'Data' not in self.data:
            return
        self.fig.add_trace(go.Scatter(x=self.bins, y=self.data['Data'][0]['Yield'],
                                      name='Data', mode='markers',
                                      marker=dict(size=12, color='black')), row=1, col=1)

    def createError(self):
        """
        Create bottom graph showing predicted:data ratio.
        :return:
        """
        marker = dict(size=12, color='black')
        if 'Data' in self.data:
            maxi, mini, error, predicted = predRatio(self.data['Total'][0]['Yield'], self.data['Data'][0]['Yield'])
            self.fig.add_trace(
                go.Scatter(x=[0, 1, 1, 0], y=[1 + error, 1 + error, 1 - error, 1 - error], fill='toself',
                           fillcolor='rgba(102, 102, 255, 0)',
                           line=dict(color='rgba(102, 102, 255, 0)'),
                           hoverinfo="skip",
                           name="Uncertainty", fillpattern=dict(shape="/", fgcolor="rgba(102, 102, 255, 1)")), row=2,
                col=1)
            self.fig.add_trace(go.Scatter(name='ratio', x=self.bins, y=predicted, showlegend=False, mode='markers',
                                          marker=marker),
                               row=2, col=1)
            self.fig.update_yaxes(title_text="Data/Pred", row=2, col=1, range=[mini, maxi])

        self.fig.add_trace(
            go.Scatter(x=[0, 1], y=[1, 1], line=dict(dash='dot', color='black', shape='linear'), showlegend=False,
                       mode='lines'), row=2, col=1)

    def createBar(self, name: str, frame: List[float], bins: List[float], widths: List[float],
                  errors: Optional[Tuple[List[float], List[float]]] = None) -> go.Bar:
        """
        @TODO factor out into utils class
        Create Plotly Bar object from edge list and dataset.
        :param str name: Name of sample, will show on legend.
        :param list[float] frame: Height of each interval.
        :param list[float] bins: Precalculated intervals.
        :param list[float] widths: Widths of each interval.
        :param Optional[list[float]] errors: Error of each point, no errors plotted if None.
        :return go.Bar: Plotly Bar object.
        """
        marker = dict()
        if name in self.colours:
            marker = dict(color=self.colours[name])
        if errors:
            return go.Bar(
                name=latexName(name), x=bins, y=frame, width=widths,
                marker=marker, error_y=dict(symmetric=False,
                                            array=errors[0],
                                            arrayminus=errors[1],
                                            color='blue', thickness=1.5))

        return go.Bar(
            name=latexName(name), x=bins, y=frame, width=widths,
            marker=marker)

    def generate(self) -> dict:
        """
        Generates chart to send to client side.
        :return dict: Chart schema to parse client side.
        """
        # Top graph
        self.createBarChart()
        self.createScatter()
        # Bottom graph
        self.createError()
        return self.fig.to_dict()
