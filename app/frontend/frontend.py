import uuid

import streamlit as st
import httpx

API_URL =  "http://127.0.0.1:8000/api/v1/chat"

st.title("NovaTech - Internal Company Assistant")

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "message_history" not in st.session_state:
    st.session_state.message_history = []

with st.sidebar:
    if st.button("New Chat", use_container_width=True):
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.message_history = []
        st.rerun()

for message in st.session_state.message_history:
    with st.chat_message(message["role"]):
        st.text(message["content"])

user_input = st.chat_input("Enter message...")
if user_input:
    with st.chat_message("user"):
        st.session_state.message_history.append({"role": "user", "content": user_input})
        st.text(user_input)
    with st.chat_message("assistant"):
        try:
            with httpx.stream(
                "POST",
                API_URL,
                json={"query": user_input, "user_id": st.session_state.thread_id},
                timeout=120.0,
            ) as response:
                response.raise_for_status()
                with st.spinner("Thinking..."):
                    answer = st.write_stream(response.iter_text())
                    st.session_state.message_history.append(
                        {"role": "assistant", "content": answer}
                    )
        except Exception as e:
            st.error(f"some error occured:{e}")