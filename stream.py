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

# Function retrieves the top-level category
def get_children(parent):
    db = EuromonitorDB()
    categories = db.get_categories(parentId=parent)
    df = pd.DataFrame(categories)
    df.reset_index(drop=True)
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

def get_datatypes(industry_code):
    api = EuromonitorAPI()
    slices = api.get_datatypes_by_industry_code(industry_code)
    df = pd.DataFrame(slices)
    return df

# Create a two-column layout
col1, col2 = st.columns([1, 1])

# Form content in the left column
with col1:
    # Get top-level categories
    industry = get_toplevel()

    # Create a selectbox for categories
    selected_industry = st.selectbox("Industry", options=industry['name'], label_visibility="visible")

    # Get the selected category ID
    selected_industry_id = industry.loc[industry['name'] == selected_industry, 'id'].values[0]
    
    # Get the selected category's parent ID
    selected_parent_id = industry.loc[industry['name'] == selected_industry, 'parentId'].values[0]

    # Get the selected category's industryCode
    selected_category_industry_code = industry.loc[industry['name'] == selected_industry, 'industryCode'].values[0]
    
    categories = get_children(int(selected_industry_id))    
    
    selected_categories = st.multiselect("Categories", options=categories['name'], default=None, label_visibility="visible")
    selected_categories_ids = categories.loc[categories['name'].isin(selected_categories), 'id'].values.tolist()

    # Get countries
    countries_df = get_countries()

    selected_countries = st.multiselect("Countries", options=countries_df['name'], default=None, label_visibility="visible")

    # Get the selected country IDs
    selected_country_ids = countries_df.loc[countries_df['name'].isin(selected_countries), 'id'].values.tolist()

    # Get slices for the selected industry code
    slices = get_slices(selected_category_industry_code)

    st.selectbox("Slices", options=slices['name'], label_visibility="visible")
    
    # Get dtypes for the selected industry code
    types = get_datatypes(selected_category_industry_code)
    st.text(types)

    type_selector = st.selectbox("Data Types", options=types['name'], label_visibility="visible")
    
    selected_type_id = types.loc[types['name'] == type_selector, 'id'].values[0]

# Right column for displaying response
with col2:
    
    # Define the API endpoint and parameters
    base_url = "https://api.euromonitor.com/statistics/marketsizes"
    inflation_type = "Current"
    unified_currency = "USD"
    exchange_rate = "YearOnYear"
    data_type_ids = selected_type_id

    # Format the URL
    url = f"{base_url}?GeographyIds={selected_country_ids}&Limit=1000&CategoryIds={selected_categories_ids}&InflationType={inflation_type}&industryCodes={selected_category_industry_code}&unifiedCurrency={unified_currency}&exchangeRate={exchange_rate}&dataTypeIds={data_type_ids}"

    # Make the API request
    response = api.make_request(url)
    # Decode the bytes into a string
    response_str = response.decode("utf-8")

    # Parse the JSON response
    response_data = json.loads(response_str)

    if response_data["marketSizes"][0]["unitName"] == "Not calculable":
        st.write("This query cannot be returned for this Geography/Country")
    else:
        dfs = []
        for market_size in response_data["marketSizes"]:
            geography_name = market_size["geographyName"]
            category_name = market_size["categoryName"]
            data = market_size["data"]
            
            # Extract year and value from the data list
            years = [str(item["year"]) for item in data]
            values = [item["value"] for item in data]
            
            # Create a DataFrame for the current market size
            df = pd.DataFrame({"Year": years, "Value": values})
            df["Geography"] = geography_name
            df["Category"] = category_name
            dfs.append(df)

        # Concatenate all the DataFrames
        df_combined = pd.concat(dfs)

        # Determine the y-axis label based on unitMultiplier and currency
        unit_multiplier = response_data["marketSizes"][0]["unitMultiplier"]
        currency = response_data["marketSizes"][0]["unitName"]

        # Set the column names for the final DataFrame
        column_names = ["Category", "Geography", "Year", "Value"]

        # Reorder the columns based on the column names
        df_combined = df_combined.reindex(columns=column_names)

        # Rename the column headers
        df_combined.columns = ["Category", "Geography", "Year", "Value"]


        if unit_multiplier == 1000000:
            y_axis_label = f"{currency} Million"
        elif unit_multiplier == 1000:
            y_axis_label = f"{currency} Thousand"
        else:
            y_axis_label = currency

        # Create radio buttons for display options
        display_options = ["Table", "Graph"]
        selected_display_option = st.radio("Display Option", display_options)

        # Display content based on selected option
        if selected_display_option == "Table":
            # Display the DataFrame
            csv_data = df_combined.to_csv(index=False)
            st.download_button("Download CSV", data=csv_data, file_name="data.csv", mime="text/csv")
            st.dataframe(df_combined)
        else:
    # Create a radio button for selecting the grouping option
            grouping_option = st.radio("Grouping Option", ("Categories", "Geographies"))

            # Check the selected grouping option
            if grouping_option == "Categories":
                # Create a line chart for each selected category
                for selected_category in selected_categories:
                    # Filter the DataFrame based on the selected category
                    filtered_df = df_combined[df_combined['Category'] == selected_category]

                    # Create a line chart for the selected category with all geographies
                    fig = go.Figure()

                    # Iterate over each geography and add a scatter trace to the chart
                    for geography, group_data in filtered_df.groupby('Geography'):
                        fig.add_trace(go.Scatter(x=group_data['Year'], y=group_data['Value'], mode='lines', name=geography))

                    # Customize the chart title
                    fig.update_layout(title=f"Value over Years - Category: {selected_category}",
                                    xaxis_title='Year', yaxis_title=y_axis_label)

                    # Display the chart
                    st.plotly_chart(fig)

            else:  # Grouping Option is "Geographies"
                # Create a line chart for each selected geography
                for selected_geography in selected_countries:
                    # Filter the DataFrame based on the selected geography
                    filtered_df = df_combined[df_combined['Geography'] == selected_geography]

                    # Create a line chart for the selected geography with all categories
                    fig = go.Figure()

                    # Iterate over each category and add a scatter trace to the chart
                    for category, group_data in filtered_df.groupby('Category'):
                        fig.add_trace(go.Scatter(x=group_data['Year'], y=group_data['Value'], mode='lines', name=category))

                    # Customize the chart title
                    fig.update_layout(title=f"Value over Years - Geography: {selected_geography}",
                                    xaxis_title='Year', yaxis_title=y_axis_label)

                    # Display the chart
                    st.plotly_chart(fig)

