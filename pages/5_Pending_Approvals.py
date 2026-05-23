import streamlit as st

from utils.styles import load_css
from utils.database import (
    get_all_invoices,
    update_status
)

st.set_page_config(layout="wide")

load_css()

st.title("⏳ Pending Approvals")

password = st.text_input(
    "Enter Admin Password",
    type="password"
)

if password == "admin123":

    rows = get_all_invoices()

    pending_rows = [

        row for row in rows.data

        if row["status"] == "Pending"
    ]

    if pending_rows:

        for row in pending_rows:

            st.markdown("---")

            c1, c2, c3 = st.columns([2,2,2])

            with c1:

                st.subheader(
                    row["invoice_number"]
                )

                st.write(
                    f"Vendor: {row['vendor_name']}"
                )

                st.write(
                    f"Email: {row['vendor_email']}"
                )

            with c2:

                st.write(
                    f"Amount: ₹ {row['total_amount']:,.2f}"
                )

                st.write(
                    f"Category: {row['category']}"
                )

                st.write(
                    f"Date: {row['invoice_date']}"
                )

            with c3:

                if row["file_url"]:

                    st.link_button(
                        "View Invoice",
                        row["file_url"]
                    )

