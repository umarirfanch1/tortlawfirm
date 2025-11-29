import streamlit as st
from datetime import date

# ---------- Styling ----------
st.set_page_config(
    page_title="Summit Legal Mass Tort Intake",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for aesthetics
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
    }
    .stTextInput>div>div>input {
        border-radius: 6px;
    }
    .stFileUploader>div>div>input {
        border-radius: 6px;
    }
    </style>
    """, unsafe_allow_html=True
)

# ---------- Header ----------
st.image("https://via.placeholder.com/250x80.png?text=Summit+Legal+Logo", width=250)
st.title("Mass Tort Client Intake Form")
st.markdown("""
Welcome to **Summit Legal**, your trusted partner in mass tort cases.  
Please complete the intake form below so our legal team can evaluate your case efficiently.
""")

st.markdown("---")

# ---------- Form ----------
with st.form("intake_form", clear_on_submit=True):
    st.header("Personal Information")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    dob = st.date_input("Date of Birth", max_value=date.today())
    address = st.text_area("Home Address")

    st.header("Mass Tort Case Details")
    st.selectbox("Type of Mass Tort", [
        "Hair Dye and Cancer Risk", 
        "Ethylene Oxide (EtO)", 
        "Sexual Abuse Cases", 
        "Depo-Provera", 
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
    st.date_input("Date of Incident / Exposure", max_value=date.today())
    st.text_area("Describe your experience or injury in detail")
    st.file_uploader("Upload any relevant documents", type=["pdf", "jpg", "png"])

    st.header("Additional Information")
    st.radio("Are you currently represented by another attorney?", ["Yes", "No"])
    st.checkbox("I authorize Summit Legal to contact me regarding my case")
    st.text_area("How did you hear about Summit Legal?")

    submitted = st.form_submit_button("Submit Intake Form")

    if submitted:
        # Simulate saving to database or JSON
        intake_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "dob": str(dob),
            "address": address,
            "mass_tort_type": st.session_state.get("mass_tort_type", "Not Selected"),
            "incident_date": str(st.session_state.get("incident_date", date.today())),
            "case_description": st.session_state.get("case_description", ""),
            "represented": st.session_state.get("represented", "No"),
            "consent": st.session_state.get("consent", False),
            "referral_source": st.session_state.get("referral_source", "")
        }
        st.success("Thank you! Your intake form has been submitted successfully.")
        st.json(intake_data)

# ---------- Footer ----------
st.markdown("---")
st.markdown("""
© 2025 Summit Legal. All Rights Reserved.  
[Contact Us](#) | [Privacy Policy](#) | [Terms of Service](#)
""")
