import plotly.offline as pyo
import plotly.graph_objs as go
import data
import json
import plot as qpt

### Load the data into an appropriate object
marketsize_response = data.get_marketsize()
marketsize_data = json.loads(marketsize_response)

### Generate a figure
x = "Geography"
y = "Value"

fig = go.Figure(data=qpt.generate_bar(marketsize_data['data'], x, y))

# Save the figure to an HTML file
pyo.plot(fig, filename='bar_chart.html')
