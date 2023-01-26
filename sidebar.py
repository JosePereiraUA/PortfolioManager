import streamlit as st
import pandas as pd
import portfolio_manager

def update_investment_fund_tabs():
    # Updates the Display toggle on the investment_funds DataFrame.
    # Called when changing the sidebar investment fund picker
    
    N = len(st.session_state.investment_funds)
    for i in range(N):
        is_investment_fund_selected = st.session_state.investment_funds.loc[i, "Name"] in st.session_state.investment_fund_picker
        st.session_state.investment_funds.loc[i, "Display"] = is_investment_fund_selected

def display_sidebar():
        
    with st.sidebar:
        
        # Investment fund picker
        st.multiselect(
            "Investment funds",
            key       = "investment_fund_picker",
            help      = "Select which investment funds to add movements to.",
            options   = st.session_state.investment_funds,
            on_change = update_investment_fund_tabs,
            default   = portfolio_manager.get_active_investment_funds())
        
        # Upload portfolio
        st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
        csv_file_upload = st.file_uploader("Load portfolio",
            "csv", key = "csv_loader",
            help = "Load a previously saved portfolio.",
            on_change = portfolio_manager.toggle_load_portfolio_from_csv)
        
        # Download portfolio
        st.download_button("Save portfolio", data = st.session_state.portfolio,
            help = "Save the current portfolio to a file.",
            file_name = "portofolio.csv", mime = "text/csv")
        
        # ---
        # Consume file upload action 
        if csv_file_upload and st.session_state.consume_new_csv_file_upload:
            portfolio_manager.load_portfolio_from_csv(csv_file_upload)
            st.session_state.consume_new_csv_file_upload = False
            st.experimental_rerun()