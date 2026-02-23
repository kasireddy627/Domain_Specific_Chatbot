from auth.otp_service import generate_otp, validate_otp
from auth.user_repository import get_user_by_email, create_user
from utils.validators import validate_email, validate_name

def request_otp(name: str, email: str):
    """
    Step 1: Generate OTP for login
    """

    # Basic validation
    if not name or not email:
        return {"success": False, "message": "Name and email required."}
    
    if not validate_name(name):
        return {"success": False, "message": "Name must be at least 2 characters long."}

    if not validate_email(email):
        return {"success": False, "message": "Invalid email format."}
    
    otp = generate_otp(email)

    # For development: return OTP so we can display it
    return {
        "success": True,
        "message": "OTP generated successfully.",
        "otp": otp
    }


def verify_otp_and_login(name: str, email: str, entered_otp: str):
    """
    Step 2: Validate OTP and log user in
    """

    if not validate_otp(email, entered_otp):
        return {"success": False, "message": "Invalid or expired OTP."}

    user = get_user_by_email(email)

    if not user:
        user_id = create_user(name, email)
        return {
            "success": True,
            "message": "New user created and logged in.",
            "user_id": user_id,
            "name": name,
            "email": email
        }

    return {
        "success": True,
        "message": "User logged in successfully.",
        "user_id": user["id"],
        "name": user["name"],
        "email": user["email"]
    }