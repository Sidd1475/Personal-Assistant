import uuid
import streamlit as st
import requests

from database import (
    initialize_db,
    get_conversations,
    save_message,
    get_messages,
    save_conversation,
    generate_chat_id,
    delete_conversation
)

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Personal AI Assistant",
    page_icon="🤖",
    layout="wide"
)

initialize_db()

WEBHOOK_URL = st.secrets["N8N_WEBHOOK_URL"]


# ---------------- SESSION INITIALIZATION ----------------

if "active_id" not in st.session_state:
    conversations = get_conversations()

    if conversations:
        st.session_state.active_id = conversations[0][0]
    else:
        st.session_state.active_id = None

if "pending_delete_id" not in st.session_state:
    st.session_state.pending_delete_id = None

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("🤖 Personal AI")

    if st.button("+ New Chat", use_container_width=True):
        st.session_state.active_id = generate_chat_id()
        st.session_state.pending_delete_id = None
        st.rerun()

    st.divider()
    st.subheader("Chat History")

    conversations = get_conversations()

    if not conversations:
        st.info("No previous conversations found.")

    for chat_id, title in conversations:
        col1, col2 = st.columns([5, 1])
        with col1:
            is_active = chat_id == st.session_state.active_id

            if st.button(
                f"{'🟢 ' if is_active else '💬 '}{title}",
                key=f"chat_{chat_id}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                st.session_state.active_id = chat_id
                st.rerun()
        with col2:
            if st.button(
                "🗑️",
                key=f"delete_{chat_id}",
                help="Delete this chat"
            ):
                st.session_state.pending_delete_id = chat_id
                st.rerun()

    # Delete Confirmation 
    pending_id = st.session_state.get("pending_delete_id")

    if pending_id:
        st.divider()
        st.warning("Are you sure you want to permanently delete this chat?")

        confirm_col, cancel_col = st.columns(2)

        with confirm_col:
            if st.button("Delete",type="primary",use_container_width=True):
                delete_conversation(pending_id)

                if st.session_state.active_id == pending_id:
                    remaining = get_conversations()
                    st.session_state.active_id = (
                        remaining[0][0] if remaining else None
                    )
                    st.session_state.pending_delete_id = None
                    st.rerun()
        with cancel_col:
            if st.button("Cancel",use_container_width=True):
                st.session_state.pending_delete_id = None
                st.rerun()

# ---------------- CHAT INTERFACE ----------------

active_id = st.session_state.active_id

conversations = get_conversations()

active_title = next(
    (chat[1] for chat in conversations if chat[0] == active_id),
    "Personal AI Assistant"
)

st.title(active_title)
st.caption("Powered by n8n + Google Gemini")

messages = get_messages(active_id)

# Display saved messages
 
for role, content in messages:
    with st.chat_message(role):
        st.markdown(content)


# ---------------- USER INPUT ----------------

if prompt := st.chat_input("Ask your personal assistant..."):

    # Generate a temporary ID if this is a new chat
    if not st.session_state.active_id:
        st.session_state.active_id = generate_chat_id()

    chat_id = st.session_state.active_id

    # Check whether this conversation already exists
    existing_messages = get_messages(chat_id)

    # Save conversation only when the first message arrives
    if not existing_messages:
        save_conversation(chat_id, prompt)

    # Save user message
    save_message(chat_id, "user", prompt)

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:
                response = requests.post(
                    WEBHOOK_URL,
                    json={
                        "sessionId": chat_id,
                        "message": prompt
                    },
                    timeout=120
                )

                response.raise_for_status()

                result = response.json()

                reply = (
                    result.get("reply")
                    or result.get("output")
                )

                if not reply:
                    raise ValueError(
                        f"Unexpected n8n response: {result}"
                    )

                reply = str(reply)

                # Save successful assistant response
                save_message(
                    chat_id,
                    "assistant",
                    reply
                )

                st.markdown(reply)

            except Exception as e:
                st.error(f"Request failed: {str(e)}")

    st.rerun()

