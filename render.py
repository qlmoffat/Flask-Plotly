from flask import Flask, Blueprint, render_template
import plot as qpt
import plotly
import json
import data

render = Blueprint("render", __name__, static_url_path="/static", static_folder="static")

### Render Routes

# Barplot Route
@render.route('/barplot', methods=['GET', 'POST'])
def generate_chart():
    marketsize_response = data.get_marketsize()
    marketsize_data = json.loads(marketsize_response)
    graphJSON = qpt.generate_bar(marketsize_data['data'], "Geography", "Value")

    # Convert Figure object to JSON-serializable dictionary
    graphJSON_dict = graphJSON.to_dict()

    graphJSON=json.dumps(graphJSON_dict)
    return render_template('plot.html', graphJSON=graphJSON)