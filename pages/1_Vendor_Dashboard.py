import streamlit as st
from utils.styles import load_css

st.set_page_config(layout="wide")

load_css()

st.title("📊 Vendor Dashboard")

st.success(
    "Welcome to Vendor Dashboard"
)
