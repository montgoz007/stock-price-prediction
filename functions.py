########################################################################################################
# This is a place to store functions so they don't crowd my notebooks and can be used in multiple places
########################################################################################################


######################
# 01
# Seasonal decomposition in plotly
import pandas as pd
import numpy as np
from plotly import graph_objects as go
from plotly.subplots import make_subplots
from statsmodels.tsa.seasonal import DecomposeResult, seasonal_decompose

def plot_seasonal_decompose(result:DecomposeResult, dates:pd.Series=None, title:str="Seasonal Decomposition"):
    x_values = dates if dates is not None else np.arange(len(result.observed))
    return (
        make_subplots(
            rows=4,
            cols=1,
            subplot_titles=["Observed", "Trend", "Seasonal", "Residuals"],
        )
        .add_trace(
            go.Scatter(x=x_values, y=result.observed, mode="lines", name='Observed'),
            row=1,
            col=1,
        )
        .add_trace(
            go.Scatter(x=x_values, y=result.trend, mode="lines", name='Trend'),
            row=2,
            col=1,
        )
        .add_trace(
            go.Scatter(x=x_values, y=result.seasonal, mode="lines", name='Seasonal'),
            row=3,
            col=1,
        )
        .add_trace(
            go.Scatter(x=x_values, y=result.resid, mode="lines", name='Residual'),
            row=4,
            col=1,
        )
        .update_layout(
            height=900, title=f'<b>{title}</b>', margin={'t':100}, title_x=0.5, showlegend=False
        )
    )
######################################################################

######################################################################
# 02
# Granger causality
from statsmodels.tsa.stattools import grangercausalitytests

def grangerTests(df, feat_cause, max_lag):
    for feature in df.columns:
        if feature not in ('Date', feat_cause) and feature[-4:-1] != 'lag':
            #print(f"Testing {feature}...")
            gct = grangercausalitytests(df[[feature, feat_cause]], maxlag=max_lag, verbose=0)
            for i in range (1, max_lag+1):
                p_val = gct[i][0]['params_ftest'][1]
                if p_val <= 0.05:
                    print(f"{feature} granger causes {feat_cause} at lag: {i}. P={round(p_val, 3)}")
###########################################################################

######################################################################
# 03
# day signal
def daySignal(day_change):
    if day_change > 0:
        return 1
    elif day_change < 0:
        return -1
    else:
        return 0
###########################################################################

######################################################################
# 04
# adding date parts to df
def addDateParts(df):
    df['day_of_year'] = df.index.day
    df['day_of_week'] = df.index.dayofweek
    df['week'] = df.index.week
    df['month'] = df.index.month
    return df
###########################################################################