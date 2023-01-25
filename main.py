import streamlit as st
import pandas as pd
import sidebar
import portfolio_manager

movement_types = ["Buy", "Sell"]
st.set_page_config(layout="wide")

# ---


def update_movement_date(investment_id=None, movement_id=None):
	st.session_state.movements.loc[(investment_id, movement_id),
								   "Date"] = st.session_state["date_%d_%d" % (investment_id, movement_id)]


def update_movement_type(investment_id=None, movement_id=None):
	str_type = st.session_state["type_%d_%d" % (investment_id, movement_id)]
	st.session_state.movements.loc[(
		investment_id, movement_id), "Type"] = movement_types.index(str_type)


def update_movement_amount(investment_id=None, movement_id=None):
	st.session_state.movements.loc[(investment_id, movement_id),
								   "Amount"] = st.session_state["amount_%d_%d" % (investment_id, movement_id)]


def display_movement(containers, investment_id, movement, movement_id):

	# Only the first movement in the cache should display column titles
	lv = "visible" if movement_id == 0 else "collapsed"
	date_col, type_col, amount_col, remove_col = containers

	date_col_container = date_col.container()
	date_col_container.markdown('<p style="font-size: 0px;">⠀</p>', unsafe_allow_html = True)
	date_col_container.date_input("Date", key="date_%d_%d" % (investment_id, movement_id),
						value=movement["Date"], on_change=update_movement_date,
						args=[investment_id, movement_id], label_visibility=lv)
 
	type_col_container = type_col.container()
	type_col_container.markdown('<p style="font-size: 2px;">⠀</p>', unsafe_allow_html = True)
	type_col_container.selectbox("Type", movement_types, key="type_%d_%d" % (investment_id, movement_id),
					   index=movement["Type"], on_change=update_movement_type,
					   args=[investment_id, movement_id], label_visibility=lv)
 
	amount_col_container = amount_col.container()
	amount_col_container.markdown('<p style="font-size: 2px;">⠀</p>', unsafe_allow_html = True)
	amount_col_container.number_input('Amount (€)', min_value=0.0, step=0.01,
							format='%.2f', key="amount_%d_%d" % (investment_id, movement_id),
							value=movement["Amount"], on_change=update_movement_amount,
							args=[investment_id, movement_id], label_visibility=lv)
 
	remove_col_container = remove_col.container()
	height_adjustment = 23 if movement_id == 0 else 5
	remove_col_container.markdown(
		'<p style="font-size: %dpx;">⠀</p>' % (height_adjustment), unsafe_allow_html=True)
	remove_col_container.button("Remove", key="remove_%d_%d" % (investment_id, movement_id),
		on_click=portfolio_manager.remove_movement, args=[investment_id, movement_id])


def display_movements_controls(containers, investment_id):
	containers[0].button("\+", help="Add a new movement.", key="add_%d" % (investment_id),
		on_click=portfolio_manager.add_movement, args=[investment_id])
	if st.session_state.movements.loc[st.session_state.movements.index.get_level_values(0) == investment_id].shape[0] > 0:
		containers[3].button("Remove all", help="Remove all movements.",
			key="remove_all_%d" % (investment_id),
			on_click=portfolio_manager.remove_all, args=[investment_id])


# --- INIT VARIABLES -----------------------------------------------------------
if not 'consume_new_csv_file_upload' in st.session_state:
	st.session_state.consume_new_csv_file_upload = False

# Initialize the list of all supported investment funds
if not 'investment_funds' in st.session_state:
	st.session_state.investment_funds = pd.DataFrame(
		{"Name":
		 ["Caixa Acções Líderes Globais", "Caixa Seleção Global Arrojado"],
		 "Code":
			 [0, 1],
			 "Display":
			 [False, False]
		 })

# Initialize the list of movements for each investment fund
if not 'movements' in st.session_state:
	columns = ['Date', 'Type', 'Amount']
	row_indexes = ['Investment_fund', 'Movement_Index']
	row_multi_index = pd.MultiIndex.from_product([[], []], names=row_indexes)
	st.session_state.movements = pd.DataFrame(columns=columns,
											  index=row_multi_index)


# --- MAIN CYCLE ---------------------------------------------------------------
portfolio_manager.update_portfolio()
sidebar.display_sidebar()

# Set the number and order of tabs
list_of_investment_funds_to_display = list(st.session_state.investment_funds[
	st.session_state.investment_funds["Display"] == True]["Name"])
st.session_state.tabs = ["Overview"] + list_of_investment_funds_to_display
tabs = st.tabs(st.session_state.tabs)

# Populate the 'Overview' tab
tabs[0].write("This is your investment portofolio overview.")
tab_id = 1

# Populate the investment fund tabs
for index, row in sidebar.st.session_state.investment_funds.iterrows():
	investment_id, display_tab = row["Code"], row["Display"]
	if display_tab:
		date_col, type_col, amount_col, remove_col, dashboard_col = tabs[tab_id].columns([
																						 1, 1, 1, 1, 4])
		movements_cols = [date_col, type_col, amount_col, remove_col]

		# Show list of movements, if they exist
		if investment_id in st.session_state.movements.index.get_level_values(0):
			for movement_id, movement in st.session_state.movements.loc[investment_id].iterrows():
				display_movement(movements_cols, investment_id,
								 movement, movement_id)

		# Always show the + button
		display_movements_controls(movements_cols, investment_id)
		# tabs[tab_id].button("\+", help = "Add a new entry.", key = "add_%d" % (investment_id),
		#     on_click = portfolio_manager.add_movement, args = [investment_id])
		tab_id += 1

print("---")
