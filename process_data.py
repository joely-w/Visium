import yaml
import plotly.graph_objects as go
import json

try:
    with open('../data/colours.json') as file:
        colours = json.loads(file.read())
except FileNotFoundError:
    # In case colours.json is deleted 
    colours = {}


def getData():
    """
    Parse YAML data, works one directory deep only.
    
    @TODO make file paths work relatively.
    
    :return dict: YAML data as dictionary.
    """
    with open('../data/SR_postfit.yaml', 'r') as stream:
        return yaml.safe_load(stream)


def calculateBins(edges: list[float]):
    widths = []
    bins = []
    # calculate widths of bins and bin midpoints
    for i in range(len(edges) - 1):
        width = edges[i + 1] - edges[i]
        widths.append(width)
        bins.append(edges[i] + 0.5 * width)
    return bins, widths


def calculateBar(name: str, frame: list[float], bins: list[float], widths: list[float]) -> go.Bar:
    """
    Create Plotly Bar object from edge list and dataset.
    
    :param str name: Name of sample, will show on legend.
    :param list[float] frame: Height of each interval.
    :param list[float] edges: Edges of each interval.
    
    :return go.Bar: Plotly Bar object. 
    """
    marker = dict()
    if name in colours:
        marker = dict(color=colours[name])
    return go.Bar(
        name=name,
        x=bins,
        y=frame, width=widths, marker=marker)
