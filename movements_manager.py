import streamlit as st
from datetime import date

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
    return st.session_state.movements.loc[investment_id]

def reindex_movements(investment_id):
    df = st.session_state.movements
    N  = count_movements(investment_id)
    df = df.reset_index()
    df.loc[df["Investment_fund"] == investment_id, "Movement_Index"] = range(N)
    df = df.set_index(["Investment_fund", "Movement_Index"])
    return df

def add_movement(investment_id):
    N = count_movements(investment_id)
    st.session_state.movements.loc[(investment_id, N), :] = [date.today(), 0, 0.0]
    
def remove_movement(investment_id = None, movement_id = None):
    st.session_state.movements.drop((investment_id, movement_id), inplace = True)
    st.session_state.movements = reindex_movements(investment_id)
    
def remove_all(investment_id = None):
    st.session_state.movements = st.session_state.movements.loc[
        st.session_state.movements.index.get_level_values(0) != investment_id]