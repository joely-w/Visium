from plotly.subplots import make_subplots
from .utils import histogram as util
from .chart import Chart

import plotly.graph_objects as go


class HistogramChart(Chart):
    def __init__(self, filepath: str, relative=True):
        super().__init__()

        # Load data
        self.readYaml(filepath, relative)

        # Calc bin edges
        self.bins, self.widths = util.calculateBins(self.data['Figure'][0]['BinEdges'])

        # Load colours
        self.colours = util.colours()

        # Generate figures
        self.formatFigure(), self.topFig(), self.bottomFig()

    def formatFigure(self):
        """
        Create a figure with subplots (one for histogram one for ratio graph).
        Also makes histogram stack so that data stacks properly.
        :return:
        """
        # Make subplots
        self.fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                                 x_title=self.data['Figure'][0]['XaxisLabel'],
                                 vertical_spacing=0.001, row_heights=[0.7, 0.3])
        # Update top figure layout
        self.fig.update_layout(barmode='stack', legend=dict(font=dict(size=20)))
        self.fig.update_yaxes(title_text="Events", row=1, col=1)

    def topFig(self):
        """
        Create top figure in chart. Includes bar chart and scatter plot.
        :return:
        """
        # Create bar chart with errors
        error_down = [-el for el in self.data['Total'][0]['UncertaintyDown']]
        error_up = self.data['Total'][0]['UncertaintyUp']

        for i in range(len(self.data['Samples']) - 1, 0, -1):
            frame = self.data['Samples'][i]['Yield']
            name = self.data['Samples'][i]['Name']

            # Create bar
            bar = util.createBar(name, frame, self.bins, self.widths, self.colours[name],
                                 (error_up, error_down) if i == 0 else None)

            # Add bar to figure
            self.fig.add_trace(bar, row=1, col=1)

        # Add scatter plot
        if 'Data' in self.data:
            self.fig.add_trace(go.Scatter(x=self.bins, y=self.data['Data'][0]['Yield'], name='Data', mode='markers',
                                          marker=dict(size=12, color='black')), row=1, col=1)

    def bottomFig(self):
        """
        Create bottom graph showing predicted:data ratio.
        :return:
        """
        marker = dict(size=12, color='black')
        if 'Data' in self.data:
            maxi, mini, error, predicted = util.predRatio(self.data['Total'][0]['Yield'], self.data['Data'][0]['Yield'])
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
