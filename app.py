import streamlit as st
import requests
from datetime import datetime

# PAGE CONFIG
st.set_page_config(page_title="StudyMate AI", page_icon="🤖", layout="centered")

# --- API CONFIG ---
API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
    "Content-Type": "application/json"
}

# --- SIDEBAR ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4712/4712107.png", width=100)
st.sidebar.title("StudyMate AI")
st.sidebar.markdown("""
Your personal AI study assistant 
Helps explain programming, algorithms, and CS concepts.
""")
st.sidebar.divider()
st.sidebar.markdown("**Made by:** Jakub Pawlusek")
st.sidebar.markdown("**Tech stack:** Python, Streamlit, OpenRouter API")

# --- MAIN TITLE ---
st.title("StudyMate AI")
st.caption("An AI tutor for computer science students — built with Streamlit & GPT-style API.")

# --- CHAT HISTORY ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- USER INPUT ---
with st.container():
    user_input = st.text_input("Ask a question about computer science:", placeholder="e.g. Explain Dijkstra's algorithm")

# --- SEND MESSAGE ---
if st.button("Send"):
    if user_input.strip() != "":
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.spinner("Thinking..."):
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are StudyMate, a friendly AI tutor that explains computer science clearly and helps students learn."},
                    *st.session_state.chat_history
                ],
                "temperature": 0.7,
                "max_tokens": 500
            }

            response = requests.post(API_URL, headers=HEADERS, json=payload)

            if response.status_code == 200:
                data = response.json()
                answer = data["choices"][0]["message"]["content"]
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
            else:
                st.error(f"API error: {response.status_code} - {response.text}")

# --- CHAT DISPLAY ---
st.markdown("### Conversation:")
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f"**You:** {chat['content']}")
    else:
        st.markdown(f"**StudyMate:** {chat['content']}")
        st.markdown("---")

# --- FOOTER ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    f"<small>Built by <b>Jakub Pawlusek</b> • {datetime.now().year} • Jagiellonian University</small>",
    unsafe_allow_html=True,
)
