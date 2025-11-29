import streamlit as st
from datetime import date

# ---------- Page Config ----------
st.set_page_config(
    page_title="Summit Legal Mass Tort Intake",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Custom CSS ----------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f4f6f8;
        font-family: 'Helvetica', sans-serif;
    }
    h1, h2, h3 {
        color: #1F2937;
    }
    .stButton>button {
        background-color: #4F46E5;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 8px 24px;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 6px;
        padding: 6px;
    }
    .stFileUploader>div>div>input {
        border-radius: 6px;
    }
    </style>
    """, unsafe_allow_html=True
)

# ---------- Header ----------
st.image("https://www.simmonsandfletcher.com/wp-content/uploads/2024/11/Mass-Tort.jpg", width=300)
st.title("Mass Tort Client Intake Form")
st.markdown("""
Welcome to **Summit Legal**, your trusted partner in mass tort cases.  
Please complete the intake form below so our legal team can evaluate your case efficiently.
""")
st.markdown("---")

# ---------- Sidebar Navigation ----------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Personal Info", "Case Details", "Additional Info"])

# ---------- Form ----------
with st.form("intake_form", clear_on_submit=False):

    if page == "Personal Info":
        st.header("Step 1: Personal Information")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        dob = st.date_input("Date of Birth", max_value=date.today())
        address = st.text_area("Home Address")

    elif page == "Case Details":
        st.header("Step 2: Case Details")
        mass_tort_type = st.selectbox("Type of Mass Tort", [
            "Hair Dye and Cancer Risk", 
            "Ethylene Oxide (EtO)", 
            "Sexual Abuse Cases", 
            "Depo-Provera (Contraceptive Injection)", 
            "Fire Litigation", 
            "The California FAIR Plan",
            "Roundup", 
            "OXBRYTA", 
            "Tylenol", 
            "Dacthal", 
            "Polychlorinated Biphenyls (PCBs)", 
            "Silicosis", 
            "Erythritol", 
            "Ultra-Processed Foods"
        ])
        incident_date = st.date_input("Date of Incident / Exposure", max_value=date.today())
        case_description = st.text_area("Describe your experience or injury in detail")
        documents = st.file_uploader("Upload any relevant documents", type=["pdf", "jpg", "png"], accept_multiple_files=True)

    elif page == "Additional Info":
        st.header("Step 3: Additional Information")
        represented = st.radio("Are you currently represented by another attorney?", ["Yes", "No"])
        consent = st.checkbox("I authorize Summit Legal to contact me regarding my case")
        referral_source = st.text_area("How did you hear about Summit Legal?")

    submitted = st.form_submit_button("Submit Intake Form")

    if submitted:
        intake_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "dob": str(dob),
            "address": address,
            "mass_tort_type": mass_tort_type,
            "incident_date": str(incident_date),
            "case_description": case_description,
            "documents_uploaded": [doc.name for doc in documents] if documents else [],
            "represented": represented,
            "consent": consent,
            "referral_source": referral_source
        }
        st.success("Thank you! Your intake form has been submitted successfully.")
        st.json(intake_data)

# ---------- Footer ----------
st.markdown("---")
st.markdown("""
© 2025 Summit Legal. All Rights Reserved.  
[Contact Us](#) | [Privacy Policy](#) | [Terms of Service](#)
""")
