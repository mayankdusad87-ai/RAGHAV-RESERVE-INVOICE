import streamlit as st

# ==========================================
# ADMIN AUTH
# ==========================================

def admin_login():

    password = st.text_input(
        "Enter Admin Password",
        type="password"
    )

    if password == "admin123":

        return True

    return False
