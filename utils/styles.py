import streamlit as st

def load_css():

    st.markdown("""
    <style>

    .stApp {

        background: linear-gradient(
            135deg,
            #eef4ff,
            #dbeafe
        );
    }

    h1, h2, h3 {

        color: #0f172a;

        font-weight: 700;
    }

    label {

        color: #111827 !important;

        font-weight: 700 !important;

        font-size: 15px !important;
    }

    .hero {

        background: linear-gradient(
            135deg,
            #0f172a,
            #1e3a8a
        );

        padding: 45px;

        border-radius: 28px;

        text-align: center;

        color: white;

        margin-bottom: 35px;
    }

    .card {

        background: white;

        padding: 28px;

        border-radius: 22px;

        margin-bottom: 24px;

        box-shadow: 0 8px 25px rgba(0,0,0,0.06);

        border: 1px solid #dbeafe;
    }

    .stButton > button {

        background: linear-gradient(
            90deg,
            #2563eb,
            #0284c7
        );

        color: white;

        border: none;

        border-radius: 14px;

        padding: 14px 28px;

        font-size: 16px;

        font-weight: 700;

        width: 100%;
    }

    </style>
    """, unsafe_allow_html=True)
