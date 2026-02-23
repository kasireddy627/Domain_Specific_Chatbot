import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import streamlit as st


def send_otp_email(to_email, otp):

    # Read from Streamlit secrets (Cloud-safe)
    sender = st.secrets["EMAIL_ADDRESS"]
    password = st.secrets["EMAIL_PASSWORD"]

    subject = "Your Login OTP - MLStack Architect"

    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background: white; padding: 30px; border-radius: 8px;">
                
                <h2 style="color: #333;">MLStack Architect</h2>
                
                <p>Hello,</p>
                
                <p>You requested to log in to your account.</p>
                
                <p style="font-size: 18px;">Your One-Time Password (OTP) is:</p>
                
                <div style="font-size: 28px; font-weight: bold; letter-spacing: 4px; 
                            background: #f0f0f0; padding: 15px; text-align: center; 
                            border-radius: 6px;">
                    {otp}
                </div>
                
                <p>This OTP is valid for <strong>5 minutes</strong>.</p>
                
                <p>If you did not request this login, you can safely ignore this email.</p>
                
                <hr>
                <p style="font-size: 12px; color: gray;">
                    MLStack Architect | Production-Ready GenAI System
                </p>
            </div>
        </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to_email
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, to_email, msg.as_string())