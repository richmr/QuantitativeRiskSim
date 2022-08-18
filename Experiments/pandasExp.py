# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 13:27:29 2022

@author: mrich
"""

import pandas as pd

# Define your series
s = pd.Series([9, 5, 3, 5, 5, 4, 6, 5, 5, 8, 7], name = 'value')
df = pd.DataFrame(s)

# Get the frequency, PDF and CDF for each value in the series

# Frequency
stats_df = df \
            .groupby('value')['value'] \
            .agg('count') \
            .pipe(pd.DataFrame) \
            .rename(columns = {'value': 'frequency'})

# PDF
stats_df['pdf'] = stats_df['frequency'] / sum(stats_df['frequency'])

# CDF
stats_df['cdf'] = stats_df['pdf'].cumsum()
stats_df = stats_df.reset_index()
stats_df

# Plot
stats_df.plot(x = 'value', y = ['pdf', 'cdf'], grid = True)
