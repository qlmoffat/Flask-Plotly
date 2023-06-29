import pandas as pd
import streamlit as st
import random

geographies = ["Geography A", "Geography B", "Geography C"]

metrics = [
    {
        "Name": "Metric 1",
        "Type": "Percentage"
    },
    {
        "Name": "Metric 2",
        "Type": "Number"
    },
    {
        "Name": "Metric 3",
        "Type": "Number"
    },
    {
        "Name": "Metric 4",
        "Type": "Percentage"
    },
    {
        "Name": "Metric 5",
        "Type": "Number"
    },
    {
        "Name": "Metric 6",
        "Type": "Number"
    }
]

col1, col2 = st.columns([1, 1])

with col1:
    metric_weightings = {}

    for metric in metrics:
        metric_name = metric['Name']
        values = [f"{round(i * 0.25, 2)} ({round(i * 25, 2)}%)" for i in range(-4, 5)]
        
        selected_rank = st.selectbox(metric_name, values, index=8)
        metric_weightings[metric_name] = float(selected_rank.split()[0])
        
def generate_dataframe(geographies, metrics, metric_weightings):
    data = []
    
    for geography in geographies:
        for metric in metrics:
            metric_name = metric['Name']
            metric_type = metric['Type']
            
            if metric_type == 'Percentage':
                value = round(random.uniform(-1, 1), 2)
            elif metric_type == 'Number':
                value = random.randint(1000, 100000)
                
            weighting = metric_weightings.get(metric_name, 1.0)
            weighted = round(value * weighting, 2)
            
            data.append({
                'Geography': geography,
                'Metric': metric_name,
                'Value': value,
                'Type': metric_type,
                'Weighted': weighted
            })
    
    df = pd.DataFrame(data)
    return df

with col2:
    # Usage example
    df = generate_dataframe(geographies, metrics, metric_weightings)

    st.dataframe(df)

    # Add sections to df_pivot

    df_pivot = df.pivot(index='Geography', columns='Metric', values='Weighted')
    metric_weights = {metric: metric_weightings[metric] for metric in df_pivot.columns}

    # Calculate the rank position within each metric and multiply by metric weight
    df_ranks = df_pivot.rank(axis=0, method='min')
    df_weighted_ranks = df_ranks * df_ranks.columns.to_series().map(metric_weights)

    # Calculate the score by summing the weighted ranks
    df_pivot['Score'] = df_weighted_ranks.sum(axis=1)

    # Sort the dataframe by score in descending order
    df_pivot_sorted = df_pivot.sort_values(by='Score', ascending=False)

    # Reorder columns with "Score" first, then other columns
    cols = ['Score'] + [col for col in df_pivot_sorted.columns if col != 'Score']
    df_pivot_sorted = df_pivot_sorted[cols]

    st.dataframe(df_pivot_sorted)
