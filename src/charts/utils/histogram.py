import math
from typing import List, Tuple, Optional
import plotly.graph_objects as go


def calculateBins(edges: List[float]) -> Tuple[List, List]:
    """
    Calculate bin midpoints and widths given edges.
    This calculates a Plotly-friendly array of bins given a list of edges.
    :param list[float] edges: List of edges to calculate bins from.
    :return Tuple[list, list]: List of bins, list of widths of bins.
    """
    widths = []
    bins = []

    # calculate widths of bins and bin midpoints
    for i in range(len(edges) - 1):
        width = edges[i + 1] - edges[i]
        widths.append(width)
        bins.append(edges[i] + 0.5 * width)

    return bins, widths


def latexName(name: str) -> str:
    """
    Converts string to string that will be rendered by MathJax renderer.
    :param str name: Name to convert.
    :return str: String that can be parsed by MathJax.
    """
    name_latex = name.replace('#', '\\')
    return f"${name_latex}$"


def createBar(name: str, frame: List[float], bins: List[float], widths: List[float], colour: str,
              errors: Optional[Tuple[List[float], List[float]]] = None, ) -> go.Bar:
    """
    Create Plotly Bar object from edge list and dataset.
    :param str colour: Bar colour.
    :param str name: Name of sample, will show on legend.
    :param list[float] frame: Height of each interval.
    :param list[float] bins: Precalculated intervals.
    :param list[float] widths: Widths of each interval.
    :param Optional[list[float]] errors: Error of each point, no errors plotted if None.
    :return go.Bar: Plotly Bar object.
    """
    marker = dict(color=colour)
    if errors:
        return go.Bar(
            name=latexName(name), x=bins, y=frame, width=widths, marker=marker,
            error_y=dict(symmetric=False, array=errors[0], arrayminus=errors[1], color='blue', thickness=1.5))
    return go.Bar(
        name=latexName(name), x=bins, y=frame, width=widths,
        marker=marker)


def predRatio(predicted, data) -> Tuple[float, float, float, List[float]]:
    """
    Calculates config/predicted ratio. Ratio is zero if either entry is 0.
    :param data: True data.
    :param predicted: Predicted data.
    :return Tuple[float, float, float, List[float]]: Maximum, minimum, upper error (symmetric) and data.
    """
    res = []
    maximum, minimum = 1.25, 0.5
    n = len(predicted)
    error = 0.5 * 1 / (math.sqrt(n))
    for i in range(n):
        numerator = toFloat(data[i])
        denominator = toFloat(predicted[i])
        if numerator and denominator:
            ratio = toFloat(data[i]) / predicted[i]
            if ratio > maximum:
                maximum = ratio
            if ratio < minimum:
                minimum = ratio
            res.append(ratio)
        else:
            res.append(None)
    return maximum, minimum, error, res


def colours() -> dict:
    """
    Neater to define here, colours for each bar in chart. Change colours for bars here.
    :return:
    """
    return {
        "tH": "#fe0000",
        "tWH": "#650000",
        "t#bar{t} + #geq1c": "#ccccfe",
        "t#bar{t} + #geq1b": "#6766cc",
        "t#bar{t} + light": "#ffffff",
        "t#bar{t} + H": "#00ffff",
        "t#bar{t} + V": "#66cc66",
        "t + Z": "#006766",
        "Wt-,t-,s-channel": "#ffff00",
        "Non-top bkg": "#ffcc00",
        "Rare top": "#afcec6",
        "Non-prompt": "#cb00cc"
    }


def toFloat(number: str) -> float:
    """
    Attempts to convert config to a float, returns 0 if failed.
    :param str number: Number to convert.
    :return float: Converted float.
    """
    try:
        return float(number)
    except ValueError:
        return 0
