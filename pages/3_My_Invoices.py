import streamlit as st
import pandas as pd

from utils.styles import load_css
from utils.database import (
    get_vendor_invoices
)

st.set_page_config(layout="wide")

load_css()

st.title("📋 My Invoices")

vendor_email = st.text_input(
    "Enter Vendor Email"
)

if vendor_email:

    rows = get_vendor_invoices(
        vendor_email
    )

    if rows.data:

        table_data = []

        for row in rows.data:

            table_data.append({

                "Invoice":
                    row["invoice_number"],

                "Amount":
                    row["total_amount"],

                "Status":
                    row["status"]

            })

        df = pd.DataFrame(
            table_data
        )

        st.dataframe(
            df,
            use_container_width=True
        )

    else:

        st.info(
            "No invoices found"
        )
