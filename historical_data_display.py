import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import streamlit as st
import mpld3

def display_historical_data(container, investment_id):
    
    with container:
        
        # Invested chart
        st.line_chart(st.session_state.historical_data[investment_id],
            y = ["Invested", "Total value"])
        
        # UP Value chart
        st.line_chart(st.session_state.historical_data[investment_id],
            y = "UP value")