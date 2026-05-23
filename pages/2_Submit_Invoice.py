import streamlit as st
import time

from utils.styles import load_css

from utils.database import (
    insert_invoice,
    supabase
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    layout="wide"
)

load_css()

# =====================================================
# TITLE
# =====================================================

st.title("📤 Submit Invoice")

st.markdown(
    "### * Mandatory Fields"
)

# =====================================================
# EMAIL
# =====================================================

vendor_email = st.text_input(
    "Vendor Email *"
)

# =====================================================
# UPLOAD OPTION
# =====================================================

upload_option = st.radio(

    "Choose Upload Method",

    [
        "📷 Capture From Camera",
        "📁 Upload File"
    ],

    horizontal=True
)

uploaded_file = None

# =====================================================
# CAMERA
# =====================================================

if upload_option == "📷 Capture From Camera":

    uploaded_file = st.camera_input(
        "Take Invoice Photo"
    )

# =====================================================
# FILE UPLOAD
# =====================================================

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

# =====================================================
# DETAILS SECTION
# =====================================================

st.markdown("---")

st.subheader("📄 Invoice Details")

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

# =====================================================
# FINANCIAL SECTION
# =====================================================

st.markdown("---")

st.subheader("💰 Financial Details")

f1, f2 = st.columns(2)

with f1:

    invoice_amount = st.number_input(

        "Invoice Amount",

        min_value=0.0,

        step=1.0
    )

with f2:

    gst_amount = st.number_input(

        "GST Amount",

        min_value=0.0,

        step=1.0
    )

# =====================================================
# TOTAL
# =====================================================

total_amount = (
    invoice_amount + gst_amount
)

st.success(
    f"Total Including GST: ₹ {total_amount:,.2f}"
)

# =====================================================
# SUBMIT BUTTON
# =====================================================

if st.button("🚀 Submit Invoice"):

    missing = []

    # ==========================================
    # VALIDATION
    # ==========================================

    if not vendor_email:
        missing.append("Vendor Email")

    if not vendor_name:
        missing.append("Vendor Name")

    if not invoice_number:
        missing.append("Invoice Number")

    if not invoice_date:
        missing.append("Invoice Date")

    if missing:

        st.error(
            "Missing Fields: "
            + ", ".join(missing)
        )

    else:

        try:

            file_url = ""

            # ======================================
            # FILE UPLOAD
            # ======================================

            if uploaded_file:

                try:

                    unique_name = (

                        f"{int(time.time())}_"
                        f"{uploaded_file.name}"

                    )

                    upload_response = supabase.storage.from_(

                        "invoice-files"

                    ).upload(

                        unique_name,

                        uploaded_file.getvalue()

                    )

                    st.write(
                        "Upload Response:",
                        upload_response
                    )

                    file_url = (

                        f"{st.secrets['SUPABASE_URL']}"
                        f"/storage/v1/object/public/"
                        f"invoice-files/{unique_name}"

                    )

                    st.success(
                        "File uploaded successfully"
                    )

                except Exception as upload_error:

                    st.error(
                        f"File Upload Error: {upload_error}"
                    )

            # ======================================
            # DATABASE DATA
            # ======================================

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

            st.write(
                "Data Being Inserted:",
                data
            )

            # ======================================
            # INSERT INTO DATABASE
            # ======================================

            response = insert_invoice(data)

            st.write(
                "Insert Response:",
                response
            )

            st.success(
                "✅ Invoice Submitted Successfully"
            )

        except Exception as e:

            st.error(
                f"Main Error: {str(e)}"
            )
