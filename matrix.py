import pandas as pd
import streamlit as st
import wbdata as wb
import random
import numpy as np
from euromonitor import EuromonitorAPI, EuromonitorDB

import json

# Read the configuration from config.json
with open('config.json') as file:
    config = json.load(file)

# Extract the configuration options
geographies = config['geographies']
metrics = config['metrics']

def get_countries():
    db = EuromonitorDB()
    countries = db.get_em_countries()
    df = pd.DataFrame(countries)
    return df

# This next code loops over assigned geographies, and builds a dict of selected geographies with the info from get_countries()
em_geographies = get_countries()

selected_geographies = {}

for geo_id in geographies:
    geography_info = em_geographies[em_geographies['id'] == geo_id]
    if not geography_info.empty:
        geography_dict = {
            'geoid': geo_id,
            'country': geography_info['name'].values[0],
            'iso_code': geography_info['iso_code'].values[0],
        }
        selected_geographies[geo_id] = geography_dict


col1, col2 = st.columns([0.3, 0.7])

with col1:
    # Get sources from WBData package
    # A source is a subject containing a list of indicators

    metric_weightings = {}

    for metric in metrics:
        metric_name = metric['Name']
        values = [f"{round(i * 0.25, 2)} ({round(i * 25, 2)}%)" for i in range(-4, 9)]

        selected_rank = st.selectbox(metric_name, values, index=8)
        metric_weightings[metric_name] = float(selected_rank.split()[0])
        opt = [
            {
                "Name": "Ascending",
                "Sort": 1
            },
            {
                "Name": "Descending",
                "Sort": 0
            }
        ]

        direction = st.radio(metric_name + " direction", options=[item["Name"] for item in opt])
        selected_option = next((item for item in opt if item["Name"] == direction), None)
        sort_direction = selected_option["Sort"]


def generate_dataframe(geographies, metrics, metric_weightings):
    def format_percentage_value(value):
        return f"{value:.0%}" if value is not None else "N/A"

    def format_number_value(value):
        return f"{value:,.2f}" if value is not None else "N/A"

    data = []

    random.seed(42)  # Set a random seed for repeatability

    for geography in geographies:
        country_code = geography['iso_code']
        for metric in metrics:
            metric_name = metric['Name']
            metric_type = metric['Type']
            metric_source = metric['Source']
            if metric_source == 'Worldbank':
                value = retrieve_worldbank_data(metric, country_code)
            elif metric_source == 'Euromonitor':
                value = retrieve_euromonitor_data(metric, geography)
            else:
                if metric_type == 'Percentage':
                    value = round(random.uniform(-1, 1), 2)
                elif metric_type == 'Number':
                    value = random.randint(1000, 100000)
                else:
                    continue

            if metric_type == 'Percentage':
                formatted_value = format_percentage_value(value)
            elif metric_type == 'Number':
                formatted_value = format_number_value(value)
            else:
                continue

            value = value if value is not None else 0  # Assign default value of 0 if value is None
            weighting = metric_weightings.get(metric_name, 1.0)
            if isinstance(value, complex):
                # Handle complex numbers here (e.g., ignore or convert to a real number)
                pass
            else:
                weighted = round(float(value) * weighting, 2)


            data.append({
                'Geography': geography['country'],
                'Metric': metric_name,
                'Value': formatted_value,
                'Type': metric_type,
                'Weighted': weighted
            })

    df = pd.DataFrame(data)
    return df

def retrieve_worldbank_data(metric, country_code):
    indicator_id = metric['ID']
    # Retrieve the data for the desired date range
    data = wb.get_data(indicator=indicator_id, country=country_code)

    most_recent_value = None

    if data:
        # Sort the data by date in descending order
        sorted_data = sorted(data, key=lambda x: x['date'], reverse=True)

        # Retrieve the value of the most recent entry
        most_recent_value = sorted_data[0]['value']

        if most_recent_value is None:
            # If the most recent value is empty, get the value from the entry before it
            if len(sorted_data) > 1:
                most_recent_value = sorted_data[1]['value']
            else:
                most_recent_value = None

    return most_recent_value

def retrieve_euromonitor_data(metric, country_code):
    api = EuromonitorAPI()
    # Data type is either "Metric" or "CAGR initially"
    data_type = metric['DataType']
    
    ### Prepare the request
    base_url = "https://api.euromonitor.com/statistics/marketsizes"
    inflation_type = "Current"
    unified_currency = "USD"
    exchange_rate = "YearOnYear"

    # Format the URL
    url = f"{base_url}?GeographyIds={country_code['geoid']}&Limit=1000&CategoryIds={metric['ID']}&InflationType={inflation_type}&unifiedCurrency={unified_currency}&exchangeRate={exchange_rate}&dataTypeIds=103"
    # Make the API request
    response = api.make_request(url)
    
    # Check if the response is empty or not valid JSON
    if not response:
        return None
    
    try:
        # Decode the bytes into a string
        response_str = response.decode("utf-8")
        
        # Parse the JSON response
        response_data = json.loads(response_str)
    except json.JSONDecodeError:
        return None
    
    if data_type == 'Market Size':
        # Extract the most recent value
        market_sizes = response_data.get("marketSizes", [])
        if market_sizes:
            latest_market_size = market_sizes[-1]
            research_year = latest_market_size.get("researchYear")
            data = latest_market_size.get("data", [])
            
            # Find the value where data.year matches researchYear
            value = None
            for item in data:
                if item.get("year") == research_year:
                    value = item.get("value")
                    break
        else:
            value = None
        
    elif data_type == 'CAGR':
        # Extract the research year value
        research_year_value = None
        market_sizes = response_data.get("marketSizes", [])
        if market_sizes:
            latest_market_size = market_sizes[-1]
            research_year = latest_market_size.get("researchYear")
            data = latest_market_size.get("data", [])
            for item in data:
                if item.get("year") == research_year:
                    research_year_value = item.get("value")
                    break
        
        # Extract the value from 5 years prior
        prior_year_value = None
        if research_year_value:
            for item in data:
                if int(item.get("year")) == research_year - 5:
                    prior_year_value = item.get("value")
                    break
            
        # Calculate CAGR if both values are available
        if research_year_value is not None and prior_year_value is not None:
            cagr = (research_year_value - prior_year_value) ** (1/5) - 1
            value = cagr
        else:
            value = None
        
    else:
        value = None

    # Return the retrieved value
    return value



with col2:
    # Usage example
    selected_geography_list = list(selected_geographies.values())
    df = generate_dataframe(selected_geography_list, metrics, metric_weightings)

    # Add sections to df_pivot
    df_pivot = df.pivot(index='Geography', columns='Metric', values='Value')  # Use 'Value' instead of 'Weighted'
    
    # Calculate the weighted ranks
    df_weighted_ranks = df_pivot.apply(lambda x: x.rank(method='min', ascending=sort_direction == 1) * metric_weightings.get(x.name, 1.0))
    
    # Calculate the score by summing the weighted ranks
    df_pivot['Score'] = df_weighted_ranks.sum(axis=1)

    # Sort the dataframe by score in descending order
    df_pivot_sorted = df_pivot.sort_values(by='Score', ascending=False)

    # Reorder columns with "Score" first, then other columns
    cols = ['Score'] + [col for col in df_pivot_sorted.columns if col != 'Score']
    df_pivot_sorted = df_pivot_sorted[cols]

    # Format Percentage columns based on config.json
    percentage_columns = [metric['Name'] for metric in metrics if metric['Type'] == 'Percentage']
    for percentage_column in percentage_columns:
        if percentage_column in df_pivot_sorted.columns:
            df_pivot_sorted[percentage_column] = df_pivot_sorted[percentage_column].apply(
                lambda x: f"{x:.0%}" if pd.notnull(x) and isinstance(x, (int, float)) else x
            )

    # Format Number columns
    number_columns = [metric['Name'] for metric in metrics if metric['Type'] == 'Number']
    for number_column in number_columns:
        if number_column in df_pivot_sorted.columns:
            df_pivot_sorted[number_column] = df_pivot_sorted[number_column].apply(
                lambda x: f"{x:.2f}" if pd.notnull(x) and isinstance(x, float) else f"{x:.0f}" if pd.notnull(x) and isinstance(x, int) else x
            )

    # Display the styled dataframe using st.write()
    st.write(df_pivot_sorted.style)
