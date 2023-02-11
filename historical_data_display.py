import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import streamlit as st
import datetime
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
    monthly = st.session_state.historical_data_monthly[investment_id]
    
    container.markdown('<p style="font-size: 15px;">⠀</p>', unsafe_allow_html = True)
    total_value_col, total_invested_col, total_profit_col, total_profit_percentage_col, elapsed_time_col, annualized_profit_col, total_UPs_col = container.columns(7)
    
    total_value = df.iloc[-1]["Total value"]
    total_invested = df.iloc[-1]["Invested"]
    total_profit = total_value - total_invested
    if total_invested == 0.0:
        total_profit_percentage = 0.0
    else:
        total_profit_percentage = (total_profit / total_invested) * 100
    movements = st.session_state.movements.loc[investment_id].sort_values(by=['Date'])
    
    elapsed_time = datetime.date.today() - movements['Date'].iat[0].date()
    if elapsed_time > datetime.timedelta(365):
        elapsed_time_years = elapsed_time.days / 365.2425
        elapsed_time_str = "%.1f years" % (elapsed_time_years)
    elif elapsed_time == datetime.timedelta(1):
        elapsed_time_str = "%d day" % (elapsed_time.days)
    else:
        elapsed_time_str = "%d days" % (elapsed_time.days)
    
    if len(monthly) > 1:
        last_total_value = monthly.iloc[-2]["Total value"]
        last_total_invested = monthly.iloc[-2]["Invested"]
    else: # Case less than 1 month invested
        last_total_value = 0
        last_total_invested = 0
        
    total_profit_delta   = total_value - last_total_value
    total_invested_delta = total_invested - last_total_invested
    if last_total_invested == 0.0:
        last_profit = 0.0
    else:
        last_profit = ((last_total_value - last_total_invested) / last_total_invested) * 100
    total_profit_percentage_delta = total_profit_percentage - last_profit
    
    annualized_return = (((monthly['Monthly return'] + 1).prod()) ** (12 / len(monthly['Monthly return'])) - 1) * 100

    total_UPs = df.iloc[-1]["UPs"]
    last_total_UPs = monthly.iloc[-2]["UPs"]
    total_UPs_delta = total_UPs - last_total_UPs

    total_value_col.metric(label = "Value (€)",
        value = "%.2f€" % (total_value),
        help  = "The current total value of the investment. The movements refers to the variation in the last month.",
        delta = "%.2f€" % (total_profit_delta))
    
    total_invested_col.metric(label = "Invested (€)",
        value = "%.2f€" % (total_invested),
        help  = "The total invested. The movements refers to the variation in the last month.",
        delta = "%.2f€" % (total_invested_delta))
    
    total_profit_col.metric(label = "Total profit (€)",
        value = "%.2f€" % (total_profit),
        help  = "The profit value. The movements refers to the variation in the last month.",
        delta = "%.2f€" % (total_profit_delta - total_invested_delta))
    
    total_profit_percentage_col.metric(label = "Total profit (%)",
        value = "%.1f%%" % (total_profit_percentage),
        help  = "The percentage difference between the total value invested and current value of the fund. The percentage movements refers to the variation in the last month.",
        delta = "%.1f%%" % (total_profit_percentage_delta))
    
    elapsed_time_col.metric(label = "Elapsed time",
        value = elapsed_time_str,
        help  = "The total duration of this investment.")
    
    annualized_profit_col.metric(label = "Annualized profit (%)",
        value = "%.1f%%" % (annualized_return),
        help  = "The annualized percentage difference between the total value invested and the value of the fund.")
    
    total_UPs_col.metric(label = "Total UPs",
        value = "%.1f UPs" % (total_UPs),
        help  = "The total number of UPs currently in the fund. The movement refers to the variation in the last month.",
        delta = "%.1f UPs" % (total_UPs_delta))
    
    container.markdown('<p style="font-size: 15px;">⠀</p>', unsafe_allow_html = True)