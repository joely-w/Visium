from src.files import files


class Chart(files.File):
    def __init__(self):
        super().__init__()
        self.fig = None

    def show(self):
        """
        For local development, show the plot using Plotly's local browser method.
        :return:
        """
        if not self.fig:
            raise ValueError('Figure property not set! Make sure the Chart class is only used as an inherited class.')
        self.fig.show()

    def generate(self):
        """
        For web frontend. Return dictionary containing schema for chart.
        :return dict: Schema for Plotly
        """
        return self.fig.to_dict()
