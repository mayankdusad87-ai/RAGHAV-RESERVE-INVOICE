from supabase import create_client
import streamlit as st
from datetime import datetime

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# ==========================================
# INSERT INVOICE
# ==========================================

def insert_invoice(data):

    return supabase.table(
        "invoices"
    ).insert(data).execute()

# ==========================================
# GET VENDOR INVOICES
# ==========================================

def get_vendor_invoices(email):

    return supabase.table(
        "invoices"
    ).select("*").eq(
        "vendor_email",
        email
    ).order(
        "id",
        desc=True
    ).execute()

# ==========================================
# GET ALL INVOICES
# ==========================================

def get_all_invoices():

    return supabase.table(
        "invoices"
    ).select("*").order(
        "id",
        desc=True
    ).execute()

# ==========================================
# UPDATE STATUS
# ==========================================

def update_status(

    invoice_id,
    status,
    rejection_reason="",
    approved_by="Admin"

):

    return supabase.table(
        "invoices"
    ).update({

        "status":
            status,

        "rejection_reason":
            rejection_reason,

        "approved_by":
            approved_by,

        "approval_date":
            str(datetime.now())

    }).eq(
        "id",
        invoice_id
    ).execute()

# ==========================================
# CHECK DUPLICATE INVOICE
# ==========================================

def check_duplicate_invoice(

    vendor_email,
    invoice_number

):

    response = supabase.table(
        "invoices"
    ).select("*").eq(
        "vendor_email",
        vendor_email
    ).eq(
        "invoice_number",
        invoice_number
    ).execute()

    # ======================================
    # IF RECORD EXISTS
    # ======================================

    if response.data:

        for row in response.data:

            # --------------------------------
            # BLOCK IF PENDING
            # --------------------------------

            if row["status"] == "Pending":

                return {

                    "duplicate": True,

                    "message":
                        "Invoice already submitted and pending approval."
                }

            # --------------------------------
            # BLOCK IF APPROVED
            # --------------------------------

            elif row["status"] == "Approved":

                return {

                    "duplicate": True,

                    "message":
                        "Invoice already approved."
                }

            # --------------------------------
            # ALLOW IF REJECTED
            # --------------------------------

            elif row["status"] == "Rejected":

                return {

                    "duplicate": False
                }

    # ======================================
    # NO DUPLICATE FOUND
    # ======================================

    return {

        "duplicate": False
    }
