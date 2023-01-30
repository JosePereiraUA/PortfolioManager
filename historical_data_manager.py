import movements_manager
import streamlit as st
import yfinance as yf
import alert_display
import pandas as pd
import numpy as np
import os

def get_investment_funds_with_historical_data():
    # Always returns the investment fund code
    return st.session_state.historical_data.keys()

def reset_historical_data(investment_id):
    df = st.session_state.historical_data[investment_id]
    df["UPs"]         = 0
    df["Invested"]    = 0.0
    df["Total value"] = 0.0

def load_historical_data(investment_id):
    
    # Initialize a new DataFrame
    columns         = ['UP value', 'UPs', 'Invested', 'Total value']
    historical_data = pd.DataFrame(columns = columns, index = pd.Index([], name = 'Date'))
    
    # Get ticker from investment ID
    df     = st.session_state.investment_funds
    ticker = df.loc[df["Code"] == investment_id, "Ticker"]
    if ticker is None:
        return None
    
    # Historical data has 2 sources:
    # 1) Yahoo Finance - Updated every day, but missing older data (Priority)
    # 2) Backup local files - May fill any missing older data
    
    # Load local data
    local_data_filename = os.path.join("local_database", ticker.values[0]+".csv")
    if os.path.isfile(local_data_filename):
        local_data = pd.read_csv(local_data_filename,
            usecols = [0, 1], parse_dates = [0], dtype = {"Último": float},
            decimal=",", dayfirst = True)
        local_data = local_data.rename(columns={'Data':'Date', 'Último' : 'UP value'})
        local_data["Date"] = local_data["Date"].apply(lambda d: d.date())
        local_data = local_data.set_index(['Date'])
    
    # Download data from Yahoo Finance
    online_data   = yf.Ticker(ticker.values[0])
    online_data   = online_data.history(period="max")
    
    # Clean data
    online_data = online_data[['Close']].copy()
    online_data = online_data.rename(columns={'Close':'UP value'})
    online_data.reset_index(inplace = True)
    online_data["Date"] = online_data["Date"].apply(lambda d: d.date())
    online_data = online_data.set_index(['Date'])
    
    # Merge local data and Yahoo Finance data
    if os.path.isfile(local_data_filename):
        data = online_data.combine_first(local_data)
    else:
        data = online_data
    
    # Add data to the session_date.historical_data
    historical_data = pd.concat([historical_data, data])
    st.session_state.historical_data[investment_id] = historical_data
    reset_historical_data(investment_id)

def calc_historical_data_from_movements(investment_id):
    reset_historical_data(investment_id)
    df = st.session_state.historical_data[investment_id]
    movements = movements_manager.get_movements_of_investment_fund(investment_id)
    
    # Consider hedge cases
    if movements is None: # Case no movements exist (after remove all, for example)
        return None
    
    # Alert users when there's missing data
    earliest_date = movements["Date"].min()
    if df.index.min() > earliest_date:
        alert_display.add_unique_alert(alert_display.Alert('missing_early_data',
            investment_id,
            "The loaded historical data from both local and online sources does not contain data entries that predate the earliest movement date in your portfolio (%s). The earliest date we could find is %s. Consider manually checking the local data source for this investment fund." % \
            (earliest_date, df.index.min())))
    else:
        alert_display.remove_unique_alert('missing_early_data')
    
    for (_, movement) in movements.iterrows():
        UP = df.asof(movement["Date"])["UP value"]
        
        if np.isnan(UP): # Case the introduced movement date is before available data
            UP = df.iloc[0]["UP value"]

        if movement["Type"] == 0: # Buy
            df.loc[df.index > movement["Date"], 'Invested'] += movement["Amount"]
            df.loc[df.index > movement["Date"], 'UPs'] += movement["Amount"] / UP
        if movement["Type"] == 1: # Sell
            df.loc[df.index > movement["Date"], 'Invested'] -= movement["Amount"]
            df.loc[df.index > movement["Date"], 'UPs'] -= movement["Amount"] / UP
    
    df["Total value"] = df["UPs"] * df["UP value"]