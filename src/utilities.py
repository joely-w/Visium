from typing import List, Tuple


def latexName(name: str) -> str:
    """
    Converts string to string that will be rendered by Latex or treated as a standard string.
    @TODO parse entries with a +.
    :param str name: Name to convert.
    :return str: String that can be parsed by MathJax.
    """
    name_latex = name.replace('#', '\\')
    # If there is no LaTeX command, don't parse as LaTeX
    if name_latex == name:
        return name
    return f"${name_latex}$"


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


def predRatio(predicted, data) -> Tuple[float, float, List[float]]:
    """
    Calculates config/predicted ratio. Ratio is zero if either entry is 0.
    :param data: True data.
    :param predicted: Predicted data.
    :return Tuple[float, float, List[float]]: Maximum, minimum and config.
    """
    res = []
    maximum, minimum = 1.25, 0.5
    for i in range(len(predicted)):
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
    return maximum, minimum, res


def calculateBins(edges: List[float]) -> Tuple[list, list]:
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
