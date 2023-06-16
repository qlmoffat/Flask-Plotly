from flask import Flask, render_template, request
from flask.json import jsonify
import euromonitor as em
import plot as qpt
import data
import json
import pandas as pd


app = Flask(__name__, static_url_path="/static")

### Page Routes ###


# Index Route
@app.route('/')
def hello():
    marketsize_response = data.get_marketsize()
    marketsize_data = json.loads(marketsize_response)
    graphJSON = qpt.generate_bar(marketsize_data['data'], "Geography", "Value")

    # Convert Figure object to JSON-serializable dictionary
    graphJSON_dict = graphJSON.to_dict()
    
    def get_values(data, key):
        result_list = []

        for i in data['data']:
            result_list.append(i[key])
            
        unique_list = list(dict.fromkeys(result_list))
        return unique_list

    categories=get_values(marketsize_data, 'Category')
    countries=get_values(marketsize_data, 'Geography')

    return render_template('index.html',
                           categories=categories,
                           countries=countries,
                           graphJSON=json.dumps(graphJSON_dict))
@app.route('/configure', methods=['POST'])
def configure():
    selected_category = request.form.get('category')
    selected_countries = request.form.getlist('country[]')

    # Get the market size data based on the selected category and countries
    marketsize_data = data.get_marketsize(category=selected_category, geographies=selected_countries)
    # Generate_bar expects dataframe, x and y values
    graphJSON = qpt.generate_bar(marketsize_data, "Geography", "Value")

    # Convert Figure object to JSON-serializable dictionary
    graphJSON_dict = graphJSON.to_dict()
    # Get unique categories and countries for rendering in the form
    categories = pd.unique([entry['Category'] for entry in data.get_marketsize()]).tolist()
    countries = pd.unique([entry['Geography'] for entry in data.get_marketsize()]).tolist()

    return render_template('index.html',
                           categories=categories,
                           countries=countries,
                           graphJSON=json.dumps(graphJSON_dict), show_reset_button=True)
