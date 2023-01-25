import streamlit as st
import pandas as pd
from datetime import date

def update_portfolio():
	if not 'portfolio'in st.session_state:
		st.session_state.portfolio = "No data."
	if 'movements' in st.session_state:
		st.session_state.portfolio = st.session_state.movements.to_csv().encode('utf-8')

def toggle_load_portfolio_from_csv():
	st.session_state.consume_new_csv_file_upload = True
	
def load_portfolio_from_csv(contents):
	st.session_state.movements = pd.read_csv(contents, index_col=[0,1], skipinitialspace=True, parse_dates = [2])
	N = len(st.session_state.investment_funds)
	for i in range(N):
		is_investment_fund_in_file = st.session_state.investment_funds.loc[i, "Code"] in st.session_state.movements.index.get_level_values(0)
		st.session_state.investment_funds.loc[i, "Display"] = is_investment_fund_in_file

def reindex_movements(investment_id):
	df = st.session_state.movements
	N  = df.loc[df.index.get_level_values(0) == investment_id].shape[0]
	df = df.reset_index()
	df.loc[df["Investment_fund"] == investment_id, "Movement_Index"] = range(N)
	df = df.set_index(["Investment_fund", "Movement_Index"])
	return df

def add_movement(investment_id):
	df = st.session_state.movements
	N  = df.loc[df.index.get_level_values(0) == investment_id].shape[0]
	st.session_state.movements.loc[(investment_id, N), :] = [date.today(), 0, 0.0]
	
def remove_movement(investment_id = None, movement_id = None):
	st.session_state.movements.drop((investment_id, movement_id), inplace = True)
	st.session_state.movements = reindex_movements(investment_id)
	
def remove_all(investment_id = None):
	st.session_state.movements = st.session_state.movements.loc[
		st.session_state.movements.index.get_level_values(0) != investment_id]