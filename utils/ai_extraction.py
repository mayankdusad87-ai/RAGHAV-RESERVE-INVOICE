import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# ==========================================
# AI EXTRACTION
# ==========================================

def extract_invoice_data(text):

    prompt = f"""

    Extract the following fields
    from invoice text:

    - Vendor Name
    - Invoice Number
    - Invoice Date
    - GST Amount
    - Total Amount

    Invoice Text:

    {text}

    Return clean JSON.
    """

    response = client.chat.completions.create(

        model="gpt-4o-mini",

        messages=[

            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
