from flask import Flask, render_template
from flask.json import jsonify
import euromonitor as em
import plot as qpt
import data
import json


app = Flask(__name__, static_url_path="/static")

### Page Routes ###

# Index Route
# app.py
# Index Route
@app.route('/')
def hello():
    marketsize_response = data.get_marketsize()
    marketsize_data = json.loads(marketsize_response)
    graphJSON = qpt.generate_bar(marketsize_data['data'], "Geography", "Value")

    # Convert Figure object to JSON-serializable dictionary
    graphJSON_dict = graphJSON.to_dict()

    return render_template('index.html',
                           categories=em.get_categories(),
                           countries=em.get_countries(),
                           graphJSON=json.dumps(graphJSON_dict))

@app.route('/categories')
def get_categories():
    return render_template('categories.html', categories=em.get_categories(), countries=em.get_countries())