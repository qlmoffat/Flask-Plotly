import json
import pandas as pd

import pandas as pd
import json

def get_market_size(category=None, geographies=None):
    with open('mocks/market_size.json') as file:
        data = json.load(file)
        data = data['marketSizes']

        market_sizes = []
        
        for i in data:
            if category and i['categoryName'] != category:
                continue
            
            for v in i['data']:
                if geographies and i['geographyName'] not in geographies:
                    continue
                
                market_size = {
                    'Category': i['categoryName'],
                    'Geography': i['geographyName'],
                    'Data Type': i['dataType'],
                    'unitName': i['unitName'],
                    'Year': v['year'],
                    'Value': v['value']
                }
                market_sizes.append(market_size)
        
        df = pd.DataFrame(market_sizes, columns=['Category', 'Geography', 'Data Type', 'unitName', 'Year', 'Value'])
        
    return df

    
def filter(category, country):
    data = pd.read_json(get_market_size())
    cat_filtered = data[data['categoryName'] > category]
    country_filtered = cat_filtered[cat_filtered['geographyName'] > country]
    return country_filtered
    
def get_categories():
    with open('mocks/categories.json') as file:
        data = json.load(file)
        
    return data

def get_countries():
    with open('mocks/countries.json') as file:
        data = json.load(file)
    return data