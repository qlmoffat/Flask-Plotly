import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from euromonitor import EuromonitorDB, EuromonitorAPI
import json


api = EuromonitorAPI()

# Function retrieves the top-level category
def get_toplevel():
    db = EuromonitorDB()
    categories = db.get_categories(level=0)
    df = pd.DataFrame(categories)
    return df

# Function to GET Countries options
def get_countries():
    db = EuromonitorDB()
    countries = db.get_em_countries()
    df = pd.DataFrame(countries)
    return df

# Function to get slices for a given industry code
def get_slices(industry_code):
    api = EuromonitorAPI()
    slices = api.get_dataslices_by_industry_code(industry_code)
    df = pd.DataFrame(slices)
    return df

# Create a two-column layout
col1, col2 = st.columns([1, 1])

# Form content in the left column
with col1:
    # Get top-level categories
    categories_df = get_toplevel()

    # Create a selectbox for categories
    selected_category = st.selectbox("Categories", options=categories_df['name'], label_visibility="visible")

    # Get the selected category ID
    selected_category_id = categories_df.loc[categories_df['name'] == selected_category, 'id'].values[0]
    # Get the selected category's parent ID
    selected_parent_id = categories_df.loc[categories_df['name'] == selected_category, 'parentId'].values[0]

    # Get the selected category's industryCode
    selected_category_industry_code = categories_df.loc[categories_df['name'] == selected_category, 'industryCode'].values[0]

    # Get countries
    countries_df = get_countries()

    # Create a selectbox for countries
    selected_country = st.selectbox("Countries", options=countries_df['name'], label_visibility="visible")

    # Get the selected country ID
    selected_country_id = countries_df.loc[countries_df['name'] == selected_country, 'id'].values[0]

    # Check IDs of selected variables
    st.write("Selected Category ID:", selected_category_id)
    st.write("Selected Category Industry Code:", selected_category_industry_code)
    st.write("Selected Country ID:", selected_country_id)

    # Get slices for the selected industry code
    slices = get_slices(selected_category_industry_code)

    st.selectbox("Slices", options=slices['name'], label_visibility="visible")

# Right column for displaying response
with col2:
    # Define the API endpoint and parameters
    base_url = "https://api.euromonitor.com/statistics/marketsizes"
    inflation_type = "Current"
    unified_currency = "USD"
    exchange_rate = "YearOnYear"
    data_type_ids = 107

    # Format the URL
    url = f"{base_url}?GeographyIds={selected_country_id}&Limit=1000&CategoryIds={selected_category_id}&InflationType={inflation_type}&industryCodes={selected_category_industry_code}&unifiedCurrency={unified_currency}&exchangeRate={exchange_rate}&dataTypeIds={data_type_ids}"

    # Make the API request
    response = api.make_request(url)
    # Decode the bytes into a string
    response_str = response.decode("utf-8")

    # Parse the JSON response
    response_data = json.loads(response_str)

    # Extract the "data" from the response
    data = response_data["marketSizes"][0]["data"]

    # Convert the data to a DataFrame
    df = pd.DataFrame(data)

    # Determine the y-axis label based on unitMultiplier and currency
    unit_multiplier = response_data["marketSizes"][0]["unitMultiplier"]
    currency = response_data["marketSizes"][0]["unitName"]

    if unit_multiplier == 1000000:
        y_axis_label = f"{currency} Million"
    elif unit_multiplier == 1000:
        y_axis_label = f"{currency} Thousand"
    else:
        y_axis_label = currency

    # Create a radio button to select between table and graph
    display_option = st.radio("Display Option", ["Table", "Graph"])

    if display_option == "Table":
        # Display the DataFrame as a table
        st.table(df)
    else:
        # Create a line chart
        fig = go.Figure(data=go.Scatter(x=df['year'], y=df['value'], mode='lines'))

        # Set chart title and axis labels
        fig.update_layout(title='Value over Years', xaxis_title='Year', yaxis_title=y_axis_label)

        # Display the chart
        st.plotly_chart(fig)