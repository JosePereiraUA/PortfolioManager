import movements_manager
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

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
        print("Ticker value for code", investment_id, "couldn't be found.")
        return None
        
    # Download data from Yahoo Finance
    data   = yf.Ticker(ticker.values[0])
    hist   = data.history(period="max")
    
    # Clean data
    up_value = hist[['Close']].copy()
    up_value = up_value.rename(columns={'Close':'UP value'})
    up_value.reset_index(inplace = True)
    up_value["Date"] = up_value["Date"].apply(lambda d: d.date())
    up_value = up_value.set_index(['Date'])
    
    # Add data to the session_date.historical_data
    historical_data = pd.concat([historical_data, up_value])
    st.session_state.historical_data[investment_id] = historical_data
    reset_historical_data(investment_id)

def calc_historical_data_from_movements(investment_id):
    reset_historical_data(investment_id)
    df = st.session_state.historical_data[investment_id]
    movements = movements_manager.get_movements_of_investment_fund(investment_id)
    if movements is None: # Case no movements exist (after remove all, for example)
        return
    
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