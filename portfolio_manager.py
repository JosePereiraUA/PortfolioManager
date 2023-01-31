import streamlit as st
import pandas as pd
import movements_manager
import historical_data_manager
from datetime import datetime

def toggle_load_portfolio_from_csv():
    st.session_state.consume_new_csv_file_upload = True
    
def activate_investment_fund(investment_id):
    # Sets the Display of the investment fund to True. Gets DataFrame series
    # from investment ID code
    st.session_state.investment_funds.loc[
        st.session_state.investment_funds["Code"] == investment_id, "Display"] = True

    # Check if this is the first activation. If it is, trigger the loading of
    # historical data from online sources
    investment_funds_loaded = historical_data_manager.get_investment_funds_with_historical_data()
    if not investment_id in investment_funds_loaded:
        historical_data_manager.load_historical_data(investment_id)

def deactivate_investment_fund(investment_id):
    st.session_state.investment_funds.loc[
        st.session_state.investment_funds["Code"] == investment_id, "Display"] = False

def load_portfolio_from_csv(contents):
    # The contents of the file automatically replace all previous saved movements.
    st.session_state.movements = pd.read_csv(contents, index_col=[0,1],
        skipinitialspace=True, parse_dates = [2],
        dtype = {"Type": int, "Amount": float})
    st.session_state.movements["Date"] = st.session_state.movements["Date"].dt.date
    st.session_state.movements["Date"] = pd.to_datetime(st.session_state.movements["Date"])
    
    # Activate all investment funds found in the file
    N = len(st.session_state.investment_funds)
    for investment_id in range(N):
        investment_funds_with_movements = movements_manager.get_investment_funds_with_movements()
        is_investment_fund_in_file = st.session_state.investment_funds.loc[investment_id, "Code"] in investment_funds_with_movements
        if is_investment_fund_in_file:
            activate_investment_fund(investment_id)
            
        # Re-calculate historical data
        historical_data_manager.calc_historical_data_from_movements(investment_id)

def get_active_investment_funds(name_or_code = "Name"):
    return list(st.session_state.investment_funds[
        st.session_state.investment_funds["Display"] == True][name_or_code])