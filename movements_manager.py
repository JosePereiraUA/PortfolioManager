import historical_data_manager
from datetime import date
import streamlit as st
import pandas as pd

def update_movements_csv():
    # Continuously stores movement data to CSV
    if not 'movements_csv'in st.session_state:
        st.session_state.movements_csv = "No data."
    if 'movements' in st.session_state:
        st.session_state.movements_csv = st.session_state.movements.to_csv().encode('utf-8')

def count_movements(investment_id = None):
    return st.session_state.movements.loc[
        st.session_state.movements.index.get_level_values(0) == investment_id].shape[0]

def get_investment_funds_with_movements():
    # Always returns the investment fund code
    return st.session_state.movements.index.get_level_values(0)

def get_movements_of_investment_fund(investment_id):
    if count_movements(investment_id) == 0:
        return None
    else:
        return st.session_state.movements.loc[investment_id]

def get_first_movement_of_type(investment_id, movement_type):
    df  = st.session_state.movements.loc[investment_id].sort_values(by=['Date'])
    for i in range(len(st.session_state.movements.loc[investment_id])):
        row = df.iloc[i]
        if row['Type'] == movement_type:
            return row

def reindex_movements(investment_id):
    df = st.session_state.movements
    N  = count_movements(investment_id)
    df = df.reset_index()
    df.loc[df["Investment_fund"] == investment_id, "Movement_Index"] = range(N)
    df = df.set_index(["Investment_fund", "Movement_Index"])
    return df

def add_movement(investment_id):
    df = st.session_state.movements
    N = count_movements(investment_id)
    df.loc[(investment_id, N), :] = [date.today(), 0, 0.0]
    df["Type"] = pd.to_numeric(df["Type"], downcast='integer')
    df["Date"] = pd.to_datetime(df["Date"])
    df.sort_index()
    historical_data_manager.calc_historical_data_from_movements(investment_id)

def remove_movement(investment_id = None, movement_id = None):
    st.session_state.movements.drop((investment_id, movement_id), inplace = True)
    st.session_state.movements = reindex_movements(investment_id)
    st.session_state.movements["Date"] = pd.to_datetime(st.session_state.movements["Date"])
    historical_data_manager.calc_historical_data_from_movements(investment_id)
    
def remove_all(investment_id = None):
    st.session_state.movements = st.session_state.movements.loc[
        st.session_state.movements.index.get_level_values(0) != investment_id]
    st.session_state.movements["Date"] = pd.to_datetime(st.session_state.movements["Date"])
    historical_data_manager.calc_historical_data_from_movements(investment_id)