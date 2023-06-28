import streamlit as st
import pandas as pd
from euromonitor import EuromonitorDB, EuromonitorAPI
import requests
#from streamlit_tree_select import tree_select

api = EuromonitorAPI()

### Get Top-Level Category

# Function retrieves the top-level category
def get_toplevel():
    db = EuromonitorDB()
    categories = db.get_categories(level=0)
    df = pd.DataFrame(categories)
    return df

# Assign category options
categories_df = get_toplevel()

# Create a selectbox for categories
selected_category = st.selectbox("Categories", options=categories_df['name'], label_visibility="visible")

# Get the selected category ID
selected_category_id = categories_df.loc[categories_df['name'] == selected_category, 'id'].values[0]
# Get the selected category's parent ID
selected_parent_id = categories_df.loc[categories_df['name'] == selected_category, 'parentId'].values[0]

# Get the selected category's industryCode
selected_category_industry_code = categories_df.loc[categories_df['name'] == selected_category, 'industryCode'].values[0]

### Get Countries options
# Function to GET Countries options
def get_countries():
    db = EuromonitorDB()
    countries = db.get_em_countries()
    df = pd.DataFrame(countries)
    return df

# Create options
countries_df = get_countries()

# Create a selectbox for countries
selected_country = st.selectbox("Countries", options=countries_df['name'], label_visibility="visible")

# Get the selected country ID
selected_country_id = countries_df.loc[countries_df['name'] == selected_country, 'id'].values[0]


### Check IDs of Selected Variables

# Use the selected IDs and industryCode as needed
st.write("Selected Category ID:", selected_category_id)
st.write("Selected Category Industry Code:", selected_category_industry_code)
st.write("Selected Country ID:", selected_country_id)

### Get Slices for given Industry Code

#api = EuromonitorAPI()

def get_slices(industry_code):
    api = EuromonitorAPI()
    slices = api.get_dataslices_by_industry_code(industry_code)
    df = pd.DataFrame(slices)
    return df

slices = get_slices(selected_category_industry_code)

st.selectbox("Slices", options=slices['name'], label_visibility="visible")

### Get Market Size



# Define the API endpoint and parameters
base_url = "https://api.euromonitor.com/statistics/marketsizes"
geography_ids = selected_country_id
category_ids = selected_category_id
inflation_type = "Current"
industry_codes = selected_category_industry_code
unified_currency = "USD"
exchange_rate = "YearOnYear"
data_type_ids = 107

# Format the URL
url = f"{base_url}?GeographyIds={geography_ids}&Limit=1000&CategoryIds={category_ids}&InflationType={inflation_type}&industryCodes={industry_codes}&unifiedCurrency={unified_currency}&exchangeRate={exchange_rate}&dataTypeIds={data_type_ids}"

response = api.make_request(url)
st.write(response)