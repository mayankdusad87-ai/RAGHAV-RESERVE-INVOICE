import requests
import streamlit as st

RESEND_API_KEY = st.secrets.get(
    "RESEND_API_KEY",
    ""
)

FROM_EMAIL = "onboarding@resend.dev"

# ==========================================
# SEND EMAIL
# ==========================================

def send_email(
    to_email,
    subject,
    html_content
):

    url = "https://api.resend.com/emails"

    headers = {

        "Authorization":
            f"Bearer {RESEND_API_KEY}",

        "Content-Type":
            "application/json"
    }

    payload = {

        "from":
            FROM_EMAIL,

        "to":
            [to_email],

        "subject":
            subject,

        "html":
            html_content
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    return response.json()

# ==========================================
# APPROVAL EMAIL
# ==========================================

def send_approval_email(

    vendor_email,
    vendor_name,
    invoice_number,
    amount

):

    html = f"""

    <h2>Invoice Approved</h2>

    <p>Dear {vendor_name},</p>

    <p>
    Your invoice
    <b>{invoice_number}</b>
    has been approved.
    </p>

    <p>
    Approved Amount:
    ₹ {amount:,.2f}
    </p>

    <p>
    Regards,<br>
    RAGHAV RESERV Finance Team
    </p>
    """

    return send_email(

        vendor_email,

        "Invoice Approved - RAGHAV RESERV",

        html
    )

# ==========================================
# REJECTION EMAIL
# ==========================================

def send_rejection_email(

    vendor_email,
    vendor_name,
    invoice_number,
    rejection_reason

):

    html = f"""

    <h2>Invoice Rejected</h2>

    <p>Dear {vendor_name},</p>

    <p>
    Your invoice
    <b>{invoice_number}</b>
    has been rejected.
    </p>

    <p>
    Reason:
    <b>{rejection_reason}</b>
    </p>

    <p>
    Please review and resubmit.
    </p>

    <p>
    Regards,<br>
    RAGHAV RESERV Finance Team
    </p>
    """

    return send_email(

        vendor_email,

        "Invoice Rejected - RAGHAV RESERV",

        html
    )
