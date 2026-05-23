from supabase import create_client
import streamlit as st

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

def update_status(invoice_id, status):

    return supabase.table(
        "invoices"
    ).update({

        "status": status

    }).eq(
        "id",
        invoice_id
    ).execute()
