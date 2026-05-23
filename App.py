import streamlit as st
from utils.styles import load_css

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="RAGHAV RESERV",
    page_icon="🏢",
    layout="wide"
)

load_css()

# ==========================================
# HERO
# ==========================================

st.markdown("""
<div class="hero">

<h1>🏢 RAGHAV RESERV</h1>

<h3>
Enterprise Invoice Submission &
Approval Platform
</h3>

</div>
""", unsafe_allow_html=True)

# ==========================================
# HOME
# ==========================================

c1, c2 = st.columns(2)

with c1:

    st.markdown("""
    <div class="card">

    <h2>📤 Vendor Portal</h2>

    <p>
    Submit invoices and track approvals
    </p>

    </div>
    """, unsafe_allow_html=True)

with c2:

    st.markdown("""
    <div class="card">

    <h2>🛠 Admin Portal</h2>

    <p>
    Review and approve invoices
    </p>

    </div>
    """, unsafe_allow_html=True)

st.info(
    "Use left sidebar navigation to access pages."
)
