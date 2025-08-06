import streamlit as st

def apply_fullscreen_css():
    st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {padding:1rem; max-width:100%;}
    </style>
    """, unsafe_allow_html=True)

def center_title(title):
    st.markdown(f"<h2 style='text-align:center;color:#FF9913;'>{title}</h2>", unsafe_allow_html=True)

def section_header(title):
    st.markdown(f"<h4 style='text-align:center;color:#FF9913;'>{title}</h4>", unsafe_allow_html=True)

def center_button(label, key):
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        return st.button(label, key=key, use_container_width=True)
