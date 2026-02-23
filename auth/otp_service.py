import random
import time
import streamlit as st


import random

def generate_otp():
    return str(random.randint(100000, 999999))


def validate_otp(email: str, entered_otp: str) -> bool:
    """
    Validate OTP from session state.
    """

    otp_data = st.session_state.get("otp_data")

    print("Stored OTP Data:", otp_data)  # DEBUG
    print("Entered OTP:", entered_otp)   # DEBUG

    if not otp_data:
        print("No OTP data found in session.")
        return False

    if otp_data["email"] != email:
        print("Email mismatch.")
        return False

    if time.time() > otp_data["expires"]:
        print("OTP expired.")
        st.session_state.pop("otp_data", None)
        return False

    if otp_data["otp"] != entered_otp:
        print("OTP mismatch.")
        return False

    # Successful validation → remove OTP
    st.session_state.pop("otp_data", None)
    print("OTP validated successfully.")

    return True