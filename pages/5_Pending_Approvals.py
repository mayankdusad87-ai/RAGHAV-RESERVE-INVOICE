import streamlit as st

from utils.styles import load_css

from utils.database import (
    get_all_invoices,
    update_status
)

from utils.email_service import (
    send_approval_email,
    send_rejection_email
)

st.set_page_config(
    layout="wide"
)

load_css()

st.title("⏳ Pending Approvals")

# =====================================================
# ADMIN PASSWORD
# =====================================================

password = st.text_input(
    "Enter Admin Password",
    type="password"
)

if password == st.secrets["ADMIN_PASSWORD"]:

    rows = get_all_invoices()

    pending_rows = [

        row for row in rows.data

        if row["status"] == "Pending"
    ]

    if pending_rows:

        for row in pending_rows:

            st.markdown("---")

            c1, c2, c3 = st.columns(
                [2,2,2]
            )

            # =========================================
            # COLUMN 1
            # =========================================

            with c1:

                st.subheader(
                    f"Invoice #{row['invoice_number']}"
                )

                st.write(
                    f"Vendor: {row['vendor_name']}"
                )

                st.write(
                    f"Email: {row['vendor_email']}"
                )

                st.write(
                    f"Category: {row['category']}"
                )

            # =========================================
            # COLUMN 2
            # =========================================

            with c2:

                st.write(
                    f"Invoice Amount: ₹ {row['invoice_amount']:,.2f}"
                )

                st.write(
                    f"GST Amount: ₹ {row['gst_amount']:,.2f}"
                )

                st.write(
                    f"Total Amount: ₹ {row['total_amount']:,.2f}"
                )

                st.write(
                    f"Invoice Date: {row['invoice_date']}"
                )

            # =========================================
            # COLUMN 3
            # =========================================

            with c3:

                # VIEW DOCUMENT

                if row["file_url"]:

                    st.link_button(
                        "📄 View Invoice",
                        row["file_url"]
                    )

                st.write("")

                # APPROVE BUTTON

                if st.button(

                    f"✅ Approve",
                    key=f"approve_{row['id']}"

                ):

                    update_status(

                        row["id"],
                        "Approved"
                    )

                    # SEND EMAIL

                    send_approval_email(

                        row["vendor_email"],
                        row["vendor_name"],
                        row["invoice_number"],
                        row["total_amount"]

                    )

                    st.success(
                        "Invoice Approved"
                    )

                    st.rerun()

                st.write("")

                # REJECTION REASON

                rejection_reason = st.text_area(

                    "Rejection Reason",

                    key=f"reason_{row['id']}"

                )

                # REJECT BUTTON

                if st.button(

                    f"❌ Reject",
                    key=f"reject_{row['id']}"

                ):

                    if not rejection_reason:

                        st.error(
                            "Please enter rejection reason"
                        )

                    else:

                        update_status(

                            row["id"],
                            "Rejected",
                            rejection_reason
                        )

                        # SEND EMAIL

                        send_rejection_email(

                            row["vendor_email"],
                            row["vendor_name"],
                            row["invoice_number"],
                            rejection_reason

                        )

                        st.error(
                            "Invoice Rejected"
                        )

                        st.rerun()

    else:

        st.success(
            "No Pending Approvals"
        )

else:

    st.warning(
        "Enter correct admin password"
    )
