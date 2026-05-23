import streamlit as st
import pandas as pd

from utils.styles import load_css
from utils.database import (
    get_all_invoices
)

st.set_page_config(layout="wide")

load_css()

st.title("❌ Rejected Invoices")

password = st.text_input(
    "Enter Admin Password",
    type="password"
)

if password == "admin123":

    rows = get_all_invoices()

    rejected_rows = [

        row for row in rows.data

        if row["status"] == "Rejected"
    ]

    if rejected_rows:

        table_data = []

        for row in rejected_rows:

            table_data.append({

                "Vendor":
                    row["vendor_name"],

                "Invoice":
                    row["invoice_number"],

                "Amount":
                    row["total_amount"],

                "Reason":
                    row.get(
                        "rejection_reason",
                        ""
                    )

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
            "No rejected invoices found"
        )

else:

    st.warning(
        "Enter correct password"
    )
