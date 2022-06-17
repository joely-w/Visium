from typing import Optional
import plotly.graph_objects as go
import json
# @TODO get filepath working through Flask CLI.

try:
    with open('../data/colours.json') as file:
        colours = json.loads(file.read())
except FileNotFoundError:
    # In case colours.json is deleted 
    colours = {}


def calculateBins(edges: list[float]):
    """
    Calculate bin midpoints and widths given edges.
    This calculates a Plotly-friendly array of bins given a list of edges.
    :param list[float] edges: List of edges to calculate bins from.
    :return list[list[float]]: List of bins, list of widths of bins.
    """
    widths = []
    bins = []
    # calculate widths of bins and bin midpoints
    for i in range(len(edges) - 1):
        width = edges[i + 1] - edges[i]
        widths.append(width)
        bins.append(edges[i] + 0.5 * width)
    return bins, widths


def calculateBar(name: str, frame: list[float], bins: list[float], widths: list[float],
                 errors: Optional[list[list[float]]] = None) -> go.Bar:
    """
    Create Plotly Bar object from edge list and dataset.
    :param str name: Name of sample, will show on legend.
    :param list[float] frame: Height of each interval.
    :param list[float] bins: Precalculated intervals.
    :param list[float] widths: Widths of each interval.
    :param Optional[list[float]] errors: Error of each point, no errors plotted if None.
    :return go.Bar: Plotly Bar object.
    """
    marker = dict()
    if name in colours:
        marker = dict(color=colours[name])
    if errors:
        return go.Bar(
            name=name, x=bins, y=frame, width=widths,
            marker=marker, error_y=dict(
                type='data',
                symmetric=False,
                array=errors[0],
                arrayminus=errors[1],
                color='blue', thickness=1.5))

    return go.Bar(
        name=name, x=bins, y=frame, width=widths,
        marker=marker)
