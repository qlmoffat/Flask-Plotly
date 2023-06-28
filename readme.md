# Get Started
1. Clone Repo
2. Create a virtual environment
3. Install requirements.txt

## Flask
4. Run with python3 run.py
5. Navigate to http://localhost:5000/

## Streamlit
4. Run with streamlit run stream.py
5. Navigate to http://localhost:8501/

# Project Layout
## Flask
* app.py -> Core page level routes
* run.py -> Initialise the application.
* data.py

## Streamlit
* stream.py -> Streamlit App

## Euromonitor
* euromonitor.py -> controls the relationship with the Euromonitor API

## Plotting
* render.py -> will render the various charts/tables from Plotly for the Flask Application

TODO:
1. Barchart
2. Pie chart
3. Table

## Data Wrangling
* data.py -> will wrangle data and create various measures

TODO:
1. Group_by:
    * Year
    * Country
    * Category
2. Measures:
    * Value
    * CAGR
    * Forecast