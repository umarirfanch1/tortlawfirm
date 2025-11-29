import subprocess
import sys

# -------------------- Runtime Box SDK Install --------------------
try:
    from boxsdk import JWTAuth, Client
    BOX_AVAILABLE = True
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "boxsdk==2.14.0"])
    from boxsdk import JWTAuth, Client
    BOX_AVAILABLE = True

import streamlit as st
import json
import os
from datetime import date

# -------------------- Streamlit Page Config --------------------
st.set_page_config(
    page_title="Mass Tort Client Intake Form",
    page_icon="⚖️",
    layout="wide"
)

# -------------------- Box Setup --------------------
FOLDER_ID = '0'  # Replace with your Box folder ID
BOX_CONFIG_PATH = 'box_config.json'
if BOX_AVAILABLE:
    try:
        auth = JWTAuth.from_settings_file(BOX_CONFIG_PATH)
        client = Client(auth)
        folder = client.folder(folder_id=FOLDER_ID)
    except Exception as e:
        BOX_AVAILABLE = False
        st.warning(f"Failed to authenticate with Box: {str(e)}. Files will be saved locally.")
else:
    st.warning("Box SDK not available. Files will be saved locally.")

# -------------------- Local fallback --------------------
UPLOAD_DIR = 'uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -------------------- UI --------------------
st.image("https://www.simmonsandfletcher.com/wp-content/uploads/2024/11/Mass-Tort.jpg", width=300)
st.title("Mass Tort Client Intake Form")
st.markdown("""
Welcome to **Summit Legal**, your trusted partner in mass tort cases.  
Please complete the intake form below so our legal team can evaluate your case efficiently.
""")
st.markdown("---")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Personal Info", "Case Details", "Additional Info"])

# -------------------- Form --------------------
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
        # Prepare intake data
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

        # Upload files
        if uploaded_files:
            for file in uploaded_files:
                try:
                    if BOX_AVAILABLE:
                        result = folder.upload_stream(file, file.name)
                        st.success(f"Uploaded {file.name} to Box (ID: {result.id})")
                    else:
                        with open(os.path.join(UPLOAD_DIR, file.name), "wb") as f:
                            f.write(file.getbuffer())
                            st.info(f"Saved {file.name} locally.")
                except Exception as e:
                    with open(os.path.join(UPLOAD_DIR, file.name), "wb") as f:
                        f.write(file.getbuffer())
                        st.warning(f"Failed to upload {file.name} to Box. Saved locally instead.")

        # Save JSON metadata
        intake_filename = f"{first_name}_{last_name}_intake.json"
        intake_bytes = json.dumps(intake_data).encode('utf-8')
        try:
            if BOX_AVAILABLE:
                folder.upload_stream(intake_bytes, intake_filename)
                st.success("Intake form data saved to Box")
            else:
                with open(os.path.join(UPLOAD_DIR, intake_filename), "wb") as f:
                    f.write(intake_bytes)
                    st.info("Intake form data saved locally")
        except Exception as e:
            with open(os.path.join(UPLOAD_DIR, intake_filename), "wb") as f:
                f.write(intake_bytes)
                st.warning("Failed to save data to Box. Saved locally instead.")

        st.markdown("---")
        st.success("Form submitted successfully! Ready for Make.com workflow automation.")
        st.json(intake_data)

# -------------------- Footer --------------------
st.markdown("---")
st.markdown("""
© 2025 Summit Legal. All Rights Reserved.  
[Contact Us](#) | [Privacy Policy](#) | [Terms of Service](#)
""")
