from flask import Flask, Blueprint
import euromonitor as em
from flask.json import jsonify
import json

data = Blueprint("data", __name__, static_url_path="/static", static_folder="static")

## Data Routes ###

# Provides JSON Object of Market Sizes being returned
@data.route('/data/market_size')
def get_marketsize():
    df = em.get_market_size()
    df_dict = df.to_dict(orient='records')
    return json.dumps({'data': df_dict})