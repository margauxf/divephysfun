import streamlit as st

st.set_page_config(
    page_title="Dive Physics Fun",
    page_icon="🤿",
)

st.write("# Welcome! 👋")

st.sidebar.success("Select a page above.")

st.markdown(
    """
    This app aims to provide an intuitive understanding of dive physics with interactive visualizations and calculators.
    """
)
st.subheader("🫧 Boyle's law")
st.markdown(
    """
    How pressure and volume relate in a confined gas system. Calculator included.""")