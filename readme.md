# Get Started
1. Clone Repo
2. Install requirements.txt
3. Run with run.py
4. Navigate to http://127.0.0.1:5000/

# Project Layout

## Flask
* app.py -> Core page level routes
* run.py -> Initialise the application.
* data.py

## Euromonitor
* euromonitor.py -> will control the relationship with the Euromonitor API

## Plotting
* render.py -> will render the various charts/tables from Plotly

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