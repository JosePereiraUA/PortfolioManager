import historical_data_manager
import movements_manager
import streamlit as st
import pandas as pd

movement_types = ["Buy", "Sell"]

def update_movement_date(investment_id = None, movement_id = None):
    st.session_state.movements.loc[(investment_id, movement_id),
        "Date"] = pd.to_datetime(st.session_state["date_%d_%d" % (investment_id, movement_id)])
    historical_data_manager.calc_historical_data_from_movements(investment_id)

def update_movement_type(investment_id = None, movement_id = None):
    str_type = st.session_state["type_%d_%d" % (investment_id, movement_id)]
    st.session_state.movements.loc[(
        investment_id, movement_id), "Type"] = movement_types.index(str_type)
    historical_data_manager.calc_historical_data_from_movements(investment_id)

def update_movement_amount(investment_id = None, movement_id = None):
    st.session_state.movements.loc[(investment_id, movement_id),
        "Amount"] = st.session_state["amount_%d_%d" % (investment_id, movement_id)]
    historical_data_manager.calc_historical_data_from_movements(investment_id)

def display_movement(containers, investment_id, movement, movement_id):

    # Only the first movement in the cache should display column titles
    is_label_visible = "visible" if movement_id == 0 else "collapsed"
    date_col, type_col, amount_col, remove_col = containers

    date_col.date_input("Date",
        key               = "date_%d_%d" % (investment_id, movement_id),
        help              = "The date the movement occurred.",
        value             = movement["Date"],
        on_change         = update_movement_date,
        args              = [investment_id, movement_id],
        label_visibility  = is_label_visible)
 
    type_col.selectbox("Type", movement_types,
        key               = "type_%d_%d" % (investment_id, movement_id),
        help              = "Type of movement (Buy/Sell).",
        index             = movement["Type"],
        on_change         = update_movement_type,
        args              = [investment_id, movement_id],
        label_visibility  = is_label_visible)
 
    amount_col.number_input('Amount (€)',
        min_value         = 0.0,
        step              = 0.01,
        format            = '%.2f',
        key               = "amount_%d_%d" % (investment_id, movement_id),
        help              = "The amount (in €) bought/sold in this movement.",
        value             = movement["Amount"],
        on_change         = update_movement_amount,
        args              = [investment_id, movement_id],
        label_visibility  = is_label_visible)
 
    remove_col_container  = remove_col.container()
    if movement_id == 0:
        remove_col_container.markdown(
            '<p style="font-size: 7px;">⠀</p>', unsafe_allow_html = True)
    remove_col_container.button("Remove",
        key               = "remove_%d_%d" % (investment_id, movement_id),
        help              = "Remove this movement.",
        on_click          = movements_manager.remove_movement,
        args              = [investment_id, movement_id])

def display_movements_controls(containers, investment_id):
    containers[0].button("\+",
        help     = "Add a new movement.",
        key      = "add_%d" % (investment_id),
        on_click = movements_manager.add_movement,
        args     = [investment_id])
    
    if movements_manager.count_movements(investment_id) > 0:
        containers[3].button("Remove all",
            help     = "Remove all movements.",
            key      = "remove_all_%d" % (investment_id),
            on_click = movements_manager.remove_all,
               args     = [investment_id])