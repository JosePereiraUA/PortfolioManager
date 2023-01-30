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
        
def display_investment_fund_overview(container, investment_id):
    df = st.session_state.historical_data[investment_id]
    
    container.markdown('<p style="font-size: 15px;">⠀</p>', unsafe_allow_html = True)
    total_value_col, total_invested_col, total_profit_col, total_profit_percentage_col, elapsed_time_col, annualized_profit_col = container.columns(6)
    
    movements = st.session_state.movements.loc[investment_id]
    earliest_date = movements["Date"].min()
    initial_value = movements[movements["Date"] == earliest_date]["Amount"].values[0]
    total_value = df.iloc[-1]["Total value"]
    total_invested = df.iloc[-1]["Invested"]
    total_profit = total_value - total_invested
    total_profit_percentage = (total_profit / total_invested) * 100
    elapsed_time = df.index[-1] - df.index[0]
    
    monthly = st.session_state.historical_data_monthly[investment_id]
    last_total_value = monthly.iloc[-2]["Total value"]
    last_total_invested = monthly.iloc[-2]["Invested"]
    total_profit_delta   = total_value - last_total_value
    total_invested_delta = total_invested - last_total_invested
    last_profit = ((last_total_value - last_total_invested) / last_total_invested) * 100
    total_profit_percentage_delta = total_profit_percentage - last_profit
    
    total_value_col.metric(label = "Value (€)",
        value = "%.2f€" % (total_value),
        help = "The current total value of the investment. The movements refers to the variation in the last month.",
        delta = "%.1f€" % (total_profit_delta))
    
    total_invested_col.metric(label = "Invested (€)",
        value = "%.2f€" % (total_invested),
        help = "The total invested. The movements refers to the variation in the last month.",
        delta = "%.1f€" % (total_invested_delta))
    
    total_profit_col.metric(label = "Total profit (€)",
        value = "%.2f€" % (total_profit),
        help = "The profit value. The movements refers to the variation in the last month.",
        delta = "%.1f€" % (total_profit_delta - total_invested_delta))
    
    total_profit_percentage_col.metric(label = "Total profit (%)",
        value = "%.1f%%" % (total_profit_percentage),
        help = "The percentage difference between the total value invested and current value of the fund. The percentage movements refers to the variation in the last month.",
        delta = "%.1f%%" % (total_profit_percentage_delta))
    
    elapsed_time_col.metric(label = "Elapsed time",
        value = "%d days" % (elapsed_time.days),
        help = "The total duration of this investment.")
    
    annualized_profit_col.metric(label = "Annualized profit (%)",
        value = "TODO",
        help = "The annualized percentage difference between the total value invested and the value of the fund.")
    
    container.markdown('<p style="font-size: 15px;">⠀</p>', unsafe_allow_html = True)