from flask import Flask, Blueprint, request
import euromonitor as em
from flask.json import jsonify
import json

data = Blueprint("data", __name__, static_url_path="/static", static_folder="static")

## Data Routes ###

# Provides JSON Object of Market Sizes being returned
@data.route('/data/market_size', methods=['GET', 'POST'])
def get_marketsize(category=None, geographies=None):
    if request.method == 'POST':
        df = em.get_market_size(category, geographies)
        df_dict = df.to_dict(orient='records')
        return df_dict
    else:
        df = em.get_market_size()
        df_dict = df.to_dict(orient='records')
        return json.dumps({'data': df_dict})

