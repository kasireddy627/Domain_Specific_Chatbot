import time
import streamlit as st

from auth.otp_service import generate_otp
from auth.user_repository import get_user_by_email, create_user
from utils.validators import validate_email, validate_name
from services.email_service import send_otp_email


def request_otp(name: str, email: str):

    if not name or not email:
        return {"success": False, "message": "Name and email required."}

    if not validate_name(name):
        return {"success": False, "message": "Invalid name."}

    if not validate_email(email):
        return {"success": False, "message": "Invalid email."}

    otp = generate_otp()

    # Store in session HERE
    st.session_state["otp_data"] = {
        "email": email,
        "otp": otp,
        "expires": time.time() + 300
    }

    send_otp_email(email, otp)

    print("Generated OTP:", st.session_state["otp_data"])  # DEBUG

    return {"success": True}


def verify_otp_and_login(name: str, email: str, entered_otp: str):

    otp_data = st.session_state.get("otp_data")

    print("Stored OTP Data:", otp_data)
    print("Entered OTP:", entered_otp)

    if not otp_data:
        return {"success": False, "message": "Invalid or expired OTP."}

    if otp_data["email"] != email:
        return {"success": False, "message": "Invalid OTP."}

    if time.time() > otp_data["expires"]:
        st.session_state.pop("otp_data", None)
        return {"success": False, "message": "OTP expired."}

    if otp_data["otp"] != entered_otp:
        return {"success": False, "message": "Invalid OTP."}

    # OTP success
    st.session_state.pop("otp_data", None)

    user = get_user_by_email(email)

    if not user:
        user_id = create_user(name, email)
        return {
            "success": True,
            "user_id": user_id,
            "name": name,
            "email": email
        }

    return {
        "success": True,
        "user_id": user["id"],
        "name": user["name"],
        "email": user["email"]
    }