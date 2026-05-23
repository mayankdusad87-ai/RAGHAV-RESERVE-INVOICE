import streamlit as st
import time

from utils.styles import load_css
from utils.database import (
    insert_invoice,
    supabase
)

st.set_page_config(layout="wide")

load_css()

st.title("📤 Submit Invoice")

st.markdown(
    "### * Mandatory Fields"
)

# ==========================================
# EMAIL
# ==========================================

vendor_email = st.text_input(
    "Vendor Email *"
)

# ==========================================
# UPLOAD
# ==========================================

upload_option = st.radio(
    "Choose Upload Method",
    [
        "📷 Capture From Camera",
        "📁 Upload File"
    ],
    horizontal=True
)

uploaded_file = None

if upload_option == "📷 Capture From Camera":

    uploaded_file = st.camera_input(
        "Take Invoice Photo"
    )

else:

    uploaded_file = st.file_uploader(
        "Upload Invoice",
        type=[
            "pdf",
            "png",
            "jpg",
            "jpeg",
            "docx"
        ]
    )

# ==========================================
# DETAILS
# ==========================================

c1, c2 = st.columns(2)

with c1:

    vendor_name = st.text_input(
        "Vendor Name *"
    )

    invoice_number = st.text_input(
        "Invoice Number *"
    )

with c2:

    invoice_date = st.date_input(
        "Invoice Date *"
    )

    category = st.selectbox(
        "Category",
        [
            "Raw Material",
            "Transport",
            "Labour",
            "Equipment",
            "Services",
            "Other"
        ]
    )

# ==========================================
# FINANCIAL
# ==========================================

f1, f2 = st.columns(2)

with f1:

    invoice_amount = st.number_input(
        "Invoice Amount",
        min_value=0.0
    )

with f2:

    gst_amount = st.number_input(
        "GST Amount",
        min_value=0.0
    )

total_amount = (
    invoice_amount + gst_amount
)

st.success(
    f"Total Including GST: ₹ {total_amount:,.2f}"
)

# ==========================================
# SUBMIT
# ==========================================

if st.button("Submit Invoice"):

    missing = []

    if not vendor_email:
        missing.append("Vendor Email")

    if not vendor_name:
        missing.append("Vendor Name")

    if not invoice_number:
        missing.append("Invoice Number")

    if missing:

        st.error(
            "Missing Fields: "
            + ", ".join(missing)
        )

    else:

        try:

            file_url = ""

            if uploaded_file:

                unique_name = (
                    f"{int(time.time())}_"
                    f"{uploaded_file.name}"
                )

                supabase.storage.from_(
                    "invoice-files"
                ).upload(
                    unique_name,
                    uploaded_file.getvalue()
                )

                file_url = (
                    f"{st.secrets['SUPABASE_URL']}"
                    f"/storage/v1/object/public/"
                    f"invoice-files/{unique_name}"
                )

            data = {

                "vendor_name":
                    vendor_name,

                "vendor_email":
                    vendor_email,

                "invoice_number":
                    invoice_number,

                "invoice_date":
                    str(invoice_date),

                "category":
                    category,

                "invoice_amount":
                    invoice_amount,

                "gst_amount":
                    gst_amount,

                "total_amount":
                    total_amount,

                "status":
                    "Pending",

                "file_url":
                    file_url
            }

            insert_invoice(data)

            st.success(
                "Invoice Submitted Successfully"
            )

        except Exception as e:

            st.error(str(e))
