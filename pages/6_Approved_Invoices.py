import streamlit as st
import pandas as pd

from utils.styles import load_css
from utils.database import (
    get_all_invoices
)

st.set_page_config(layout="wide")

load_css()

st.title("✅ Approved Invoices")

password = st.text_input(
    "Enter Admin Password",
    type="password"
)

if password == "admin123":

    rows = get_all_invoices()

    approved_rows = [

        row for row in rows.data

        if row["status"] == "Approved"
    ]

    if approved_rows:

        table_data = []

        for row in approved_rows:

            table_data.append({

                "Vendor":
                    row["vendor_name"],

                "Invoice":
                    row["invoice_number"],

                "Amount":
                    row["total_amount"],

                "Approved By":
                    row.get("approved_by", ""),

                "Approval Date":
                    row.get("approval_date", "")

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
            "No approved invoices found"
        )

else:

    st.warning(
        "Enter correct password"
    )
