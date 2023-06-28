from flask import Flask, render_template, request
from euromonitor import EuromonitorDB
import json
import pandas as pd


app = Flask(__name__, static_url_path="/static")

### Page Routes ###


# Index Route
@app.route('/')
def hello():
    db = EuromonitorDB()
    categories = db.get_categories_by_level(0)
    return categories
    
