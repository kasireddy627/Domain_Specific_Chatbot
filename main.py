import streamlit as st
import uuid
from dotenv import load_dotenv
from database.init_db import init_db

# Load environment variables (for local testing)
load_dotenv()

# Ensure DB tables exist
init_db()

from auth.auth_controller import request_otp, verify_otp_and_login
from services.conversation_service import handle_user_message
from services.memory_service import (
    get_chat_messages,
    get_user_chats,
    delete_all_chats,
)

st.set_page_config(
    page_title="MLStack Architect",
    layout="wide"
)

# --------------------------
# Session Defaults
# --------------------------
defaults = {
    "authenticated": False,
    "user": None,
    "current_chat_id": None,
    "messages": [],
    "otp_sent": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==========================
# LOGIN PAGE
# ==========================
def login_ui():
    st.title("MLStack Architect")
    st.caption("Production-Ready Full Stack GenAI System")
    st.markdown("---")

    name = st.text_input("Name")
    email = st.text_input("Email")

    if st.button("Request OTP"):
        if not name or not email:
            st.warning("Please enter both name and email.")
            return

        response = request_otp(name, email)

        if response["success"]:
            st.session_state.otp_sent = True
            st.success("OTP sent to your email.")
        else:
            st.error(response.get("message", "Failed to send OTP."))

    # Show OTP input only after sending
    if st.session_state.otp_sent:
        entered_otp = st.text_input("Enter OTP")

        if st.button("Verify"):
            login_response = verify_otp_and_login(name, email, entered_otp)

            if login_response["success"]:
                st.session_state.authenticated = True
                st.session_state.user = login_response
                st.session_state.otp_sent = False
                st.rerun()
            else:
                st.error(login_response.get("message", "Invalid OTP."))


# ==========================
# CHAT PAGE
# ==========================
def chat_ui():
    user = st.session_state.user
    user_id = user["user_id"]

    # ---------------- Sidebar ----------------
    with st.sidebar:
        st.markdown(f"## {user['name']}")
        st.caption("Authenticated User")

        if st.button("New Chat"):
            st.session_state.current_chat_id = str(uuid.uuid4())
            st.session_state.messages = []
            st.rerun()

        st.markdown("### Chat History")

        chats = get_user_chats(user_id)

        if chats:
            for chat in chats:
                if st.button(chat["title"], key=chat["chat_id"]):
                    st.session_state.current_chat_id = chat["chat_id"]
                    st.session_state.messages = get_chat_messages(
                        user_id, chat["chat_id"]
                    )
                    st.rerun()
        else:
            st.caption("No previous chats")

        with st.expander("Settings"):
            if st.button("Delete All Chats"):
                delete_all_chats(user_id)
                st.session_state.messages = []
                st.session_state.current_chat_id = None
                st.rerun()

        st.markdown("---")

        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.messages = []
            st.session_state.current_chat_id = None
            st.rerun()

    # ---------------- Main Area ----------------
    st.title(f"Welcome, {user['name']}")
    st.caption("Your Full Stack Data Science AI Mentor")
    st.markdown("---")

    if not st.session_state.current_chat_id:
        st.session_state.current_chat_id = str(uuid.uuid4())

    if not st.session_state.messages:
        st.info("Start a new conversation about ML, DL, MLOps or Interviews.")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask your question...")

    if user_input:
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        try:
            with st.spinner("Thinking..."):
                response = handle_user_message(
                    user_id,
                    st.session_state.current_chat_id,
                    user_input
                )
        except Exception as e:
            if str(e) == "RATE_LIMIT":
                st.warning("Please wait before sending another message.")
                return
            else:
                st.error("System error occurred.")
                return

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )

        with st.chat_message("assistant"):
            st.markdown(response)


# ==========================
# ROUTING
# ==========================
if not st.session_state.authenticated:
    login_ui()
else:
    chat_ui()