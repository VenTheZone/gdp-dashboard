import streamlit as st
import time
from datetime import datetime

st.set_page_config(page_title="NeoClub - Cyberpunk Chat", layout="wide")

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'username' not in st.session_state:
    st.session_state.username = ''

# Custom CSS injection
with open('style.css') as f:
    st.markdown(f'{f.read()}', unsafe_allow_html=True)

def main():
    st.title("NeoClub")

    # Login section
    if not st.session_state.username:
        with st.form("login_form"):
            username = st.text_input("Enter your handle, samurai...", max_chars=20)
            if st.form_submit_button("Enter Night City"):
                if username.strip():
                    st.session_state.username = username
                    st.experimental_rerun()

    else:
        # Chat interface
        st.markdown("### Welcome to Night City, " + st.session_state.username)
        
        # Messages area
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.messages:
                with st.container():
                    st.markdown(f"""
                    
                        {msg['username']}
                        {msg['timestamp']}
                        {msg['content']}
                    
                    """, unsafe_allow_html=True)

        # Input area
        with st.form("chat_form", clear_on_submit=True):
            message = st.text_area("Message", height=100)
            if st.form_submit_button("Send"):
                if message.strip():
                    new_message = {
                        'username': st.session_state.username,
                        'content': message,
                        'color': '#ff2e97',
                        'timestamp': datetime.now().strftime('%H:%M')
                    }
                    st.session_state.messages.append(new_message)
                    st.experimental_rerun()

if __name__ == "__main__":
    main()
