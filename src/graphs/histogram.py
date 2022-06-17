import plotly.graph_objects as go
import process_data

def createGraph(data: dict):
    bins, widths = process_data.calculateBins(data['Figure'][0]['BinEdges'])
    bars = []

    # Create bar charts
    for i in range(len(data['Samples']) - 1, 1, -1):
        frame = data['Samples'][i]['Yield']
        name = data['Samples'][i]['Name']
        bars.append(process_data.calculateBar(name, frame, bins, widths))
    # Create scatter plots
    bars.append(go.Scatter(x=bins, y=data['Data'][0]['Yield'],
                           name='Data', mode='markers',
                           marker=dict(size=12, color='black')))

    bars.append(process_data.calculateBar(data['Samples'][0]['Name'], data['Samples'][0]['Yield'], bins, widths,
                                          [data['Total'][0]['UncertaintyUp'],
                                           [-1 * el for el in data['Total'][0]['UncertaintyDown']]]))
    fig = go.Figure(data=bars)
    fig.update_layout(barmode='stack')
    return fig.to_dict()
