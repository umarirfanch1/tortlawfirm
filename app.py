import streamlit as st
from boxsdk import JWTAuth, Client
import json
from datetime import date

# ---------- Box.com Configuration ----------
BOX_CONFIG_PATH = 'box_config.json'  # Save your JSON config as this file
FOLDER_ID = '0'  # Replace with your Box folder ID for uploads

# Authenticate with Box
auth = JWTAuth.from_settings_file(BOX_CONFIG_PATH)
client = Client(auth)
folder = client.folder(folder_id=FOLDER_ID)

# ---------- Page Setup ----------
st.set_page_config(
    page_title="Summit Legal Mass Tort Intake",
    page_icon="⚖️",
    layout="wide"
)

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
        uploaded_files = st.file_uploader("Upload any relevant documents", type=["pdf", "jpg", "png"], accept_multiple_files=True)

    elif page == "Additional Info":
        st.header("Step 3: Additional Information")
        represented = st.radio("Are you currently represented by another attorney?", ["Yes", "No"])
        consent = st.checkbox("I authorize Summit Legal to contact me regarding my case")
        referral_source = st.text_area("How did you hear about Summit Legal?")

    submitted = st.form_submit_button("Submit Intake Form")

    if submitted:
        # Prepare intake data dictionary
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
            "documents_uploaded": [file.name for file in uploaded_files] if uploaded_files else [],
            "represented": represented,
            "consent": consent,
            "referral_source": referral_source
        }

        # Upload files to Box
        if uploaded_files:
            for file in uploaded_files:
                try:
                    result = folder.upload_stream(file, file.name)
                    st.success(f"Uploaded {file.name} to Box (ID: {result.id})")
                except Exception as e:
                    st.error(f"Failed to upload {file.name} to Box: {str(e)}")

        # Upload JSON metadata to Box
        try:
            json_bytes = json.dumps(intake_data).encode('utf-8')
            folder.upload_stream(json_bytes, f"{first_name}_{last_name}_intake.json")
            st.success("Intake form data saved to Box")
        except Exception as e:
            st.error(f"Failed to save intake data to Box: {str(e)}")

        st.markdown("---")
        st.success("Form submitted successfully! Ready for Make.com workflow automation.")
        st.json(intake_data)

# ---------- Footer ----------
st.markdown("---")
st.markdown("""
© 2025 Summit Legal. All Rights Reserved.  
[Contact Us](#) | [Privacy Policy](#) | [Terms of Service](#)
""")
