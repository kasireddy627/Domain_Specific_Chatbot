import streamlit as st
import uuid

from auth.auth_controller import request_otp, verify_otp_and_login
from services.conversation_service import handle_user_message
from services.memory_service import (
    get_chat_messages,
    get_user_chats,
    delete_all_chats,
)

st.set_page_config(
    page_title="Full Stack Data Science AI Mentor",
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
    "generated_otp": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==========================
# LOGIN PAGE (HOME)
# ==========================
def login_ui():
    st.markdown("# Full Stack Data Science AI Mentor")
    st.markdown("### Intelligent AI Mentor for ML, DL & MLOps")
    st.markdown("---")

    name = st.text_input("Name")
    email = st.text_input("Email")

    if st.button("Request OTP"):
        response = request_otp(name, email)

        if response["success"]:
            st.session_state.generated_otp = response["otp"]
            st.success("OTP Sent")
            st.info(f"DEV OTP: {response['otp']}")
        else:
            st.error(response["message"])

    if st.session_state.generated_otp:
        entered_otp = st.text_input("Enter OTP")

        if st.button("Verify"):
            login_response = verify_otp_and_login(name, email, entered_otp)

            if login_response["success"]:
                st.session_state.authenticated = True
                st.session_state.user = login_response
                st.session_state.generated_otp = None
                st.rerun()
            else:
                st.error(login_response["message"])


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

        # -------- Settings Section --------
        with st.expander("Settings"):
            st.session_state.dark_theme = st.toggle("Dark Theme")

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
    st.markdown("# Welcome, {}".format(user["name"]))
    st.markdown("### Your Full Stack Data Science AI Mentor")
    st.markdown("---")

    # About section (shown only when no messages yet)
    if not st.session_state.messages:
        st.markdown("### Who am I?")
        st.markdown("""
I am a domain-focused AI mentor designed to help you with:

- Data Science Roadmaps
- Machine Learning Concepts
- Deep Learning Architectures
- MLOps & Deployment
- Real-world Project Design
- Interview Preparation
""")

        st.markdown("### What can you ask?")
        st.markdown("""
- "Give me a full stack DS roadmap"
- "Explain gradient boosting clearly"
- "How to deploy ML model on AWS?"
- "Prepare me for ML interviews"
""")

    # Initialize chat ID
    if not st.session_state.current_chat_id:
        st.session_state.current_chat_id = str(uuid.uuid4())

    # Display messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
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