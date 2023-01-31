import historical_data_display
import portfolio_manager
import movements_manager
import movements_display
import streamlit as st
import alert_display
import pandas as pd
import sidebar

# --- INIT VARIABLES -----------------------------------------------------------
st.set_page_config(layout="wide", page_title = 'Portfolio Manager')

# Apply custom CSS configuration 
with open("main.css") as f:
	st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

if not 'alerts' in st.session_state:
	st.session_state.alerts = []

if not 'consume_new_csv_file_upload' in st.session_state:
	st.session_state.consume_new_csv_file_upload = False

# Initialize the list of all supported investment funds
if not 'investment_funds' in st.session_state:
	st.session_state.investment_funds = pd.DataFrame(
		{"Name":
			["Caixa Acções Líderes Globais", "Caixa Seleção Global Arrojado"],
		"Code":
			[0, 1],
		"Ticker":
			["0P0000ZFDE.F", "0P00000SZ7.F"],
		"Display":
			[False, False]
		 })

# Initialize the list of movements for each investment fund
if not 'movements' in st.session_state:
	columns         = ['Date', 'Type', 'Amount']
	row_indexes     = ['Investment_fund', 'Movement_Index']
	row_multi_index = pd.MultiIndex.from_product([[], []], names = row_indexes)
	st.session_state.movements = pd.DataFrame(columns = columns,
		index = row_multi_index)

# Initialize the historical data
if not 'historical_data' in st.session_state:
	st.session_state.historical_data = {}
if not 'historical_data_monthly' in st.session_state:
	st.session_state.historical_data_monthly = {}
if not 'historical_data_quarterly' in st.session_state:
	st.session_state.historical_data_quarterly = {}
if not 'historical_data_annually' in st.session_state:
	st.session_state.historical_data_annually = {}

# --- MAIN CYCLE ---------------------------------------------------------------
movements_manager.update_movements_csv()
sidebar.display_sidebar()

# Set the number and order of tabs
tabs = st.tabs(["Overview"] + portfolio_manager.get_active_investment_funds())

# Populate the 'Overview' tab
tabs[0].write("This is your investment portofolio overview.")
tab_id = 1

# Populate the investment fund tabs
list_of_all_investment_funds_with_movements = movements_manager.get_investment_funds_with_movements()
for index, row in st.session_state.investment_funds.iterrows():
	investment_id, display_tab = row["Code"], row["Display"]
	if display_tab:
		alert_display.display_alerts(tabs[tab_id], investment_id)
		
		if movements_manager.count_movements(investment_id) > 0:
			historical_data_display.display_investment_fund_overview(tabs[tab_id], investment_id)
     
		date_col, type_col, amount_col, remove_col, dashboard_col = tabs[tab_id].columns([1, 1, 1, 1, 4])
		movements_cols = [date_col, type_col, amount_col, remove_col]

		# Show list of movements, if they exist
		if investment_id in list_of_all_investment_funds_with_movements:
			movements = movements_manager.get_movements_of_investment_fund(investment_id)
			for (movement_id, movement) in movements.iterrows():
				movements_display.display_movement(movements_cols, investment_id, movement, movement_id)

		# Always show the movement controls
		movements_display.display_movements_controls(movements_cols, investment_id)
  
		# Display historical data
		historical_data_display.display_historical_data(dashboard_col, investment_id)
  
		tab_id += 1

print("---")
