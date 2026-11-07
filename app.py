"""Entry point: a three-page site. Run: streamlit run app.py"""
import streamlit as st

from ui import inject_css

st.set_page_config(page_title="RAG Lab", layout="wide")
inject_css()

pages = [
    st.Page("views/home.py", title="Home", default=True),
    st.Page("views/demo.py", title="Live Demo"),
    st.Page("views/conclusion.py", title="Conclusion"),
]
st.navigation(pages).run()