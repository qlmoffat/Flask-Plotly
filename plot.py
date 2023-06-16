import plotly.io as pio

pio.renderers.default = 'vscode'
pio.templates.default = 'plotly'

import plotly.graph_objects as go

def generate_bar(data, x, y):
    x_values = []
    y_values = []
    for i in data:
        x_values.append(i[x])
        y_values.append(i[y])

    title = "{} plotted with {}".format(x, y)
    
    fig = go.Figure(
        data=[go.Bar(x=x_values, y=y_values)],
        layout_title_text=title
    )

    return fig



def generate_table(data):
    fig = go.Figure(data=[go.Table(header=dict(values=['A Scores', 'B Scores']),
                    cells=dict(values=[[100, 90, 80, 90], [95, 85, 75, 95]]))])
    return fig