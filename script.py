import plotly.offline as pyo
import plotly.graph_objs as go
import data
import json
import plot as qpt
import pandas as pd

def p():
    ### Load the data into an appropriate object
    marketsize_response = data.get_marketsize()
    marketsize_data = json.loads(marketsize_response)

    ### Generate a figure
    x = "Geography"
    y = "Value"

    fig = go.Figure(data=qpt.generate_bar(marketsize_data['data'], x, y))

    # Save the figure to an HTML file
    pyo.plot(fig, filename='bar_chart.html')

marketsize_response = data.get_marketsize()
marketsize_data = json.loads(marketsize_response)

Category = []
Geography = []

for i in marketsize_data['data']:
    Category.append(i['Category'])
    Geography.append(i['Geography'])

Category = list(dict.fromkeys(Category))
Geography = list(dict.fromkeys(Geography))

def get_values(value, key):
    data = json.loads(value())

    result_list = []

    for i in data['data']:
        result_list.append(i[key])
        
    unique_list = list(dict.fromkeys(result_list))
    return unique_list

    
#out = get_values(data.get_marketsize, 'Category')
#print(out)
