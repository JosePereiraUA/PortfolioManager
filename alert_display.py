import streamlit as st

class Alert:
    def __init__(self, unique_id = 'default', investment_id = 'all', message = 'Opps! Something is wrong!'):
        self.unique_id = unique_id
        self.investment_id = investment_id
        self.message = message
        
def display_alerts(container, investment_id):
    # print([x.investment_id for x in st.session_state.alerts])
    # print(investment_id)
    for alert in st.session_state.alerts:
        if alert.investment_id in ['all', investment_id]:
            # print("ALERT!")
            container.error(alert.message, icon = '🔥')
            
def add_unique_alert(alert):
    print("CALLED")
    unique_ids = [a.unique_id for a in st.session_state.alerts]
    print(alert.unique_id in unique_ids)
    if not alert.unique_id in unique_ids:
        st.session_state.alerts.append(alert)

def remove_unique_alert(unique_id):
    not_found = lambda x: not x.unique_id == unique_id
    st.session_state.alerts = list(filter(not_found, st.session_state.alerts))