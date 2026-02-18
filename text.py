import streamlit as st

def print_text():
    st.write(st.session_state.chat_input)
    st.session_state.chat_input = st.session_state.chat_input
    # st.rerun()

st.chat_input("Start a conversation!", on_submit=print_text, key="chat_input")