import streamlit as st
from htbuilder.units import rem
from htbuilder import div, styles

st.set_page_config(page_title="About the Team", page_icon="👥")

# --- CSS Styling (Optional, to match your theme) ---
st.html(div(style=styles(font_size=rem(3), line_height=1))["👥"])

st.title("Meet the Team")

st.markdown("""
We are a group of MIDS students and professionals that are passionate about leveraging technology to solve complex problems, including in energy demand forecasting and resource planning. Our team combines expertise in data analysis, machine learning, software development, and project management to create innovative solutions that can help shape the future of energy in California.
""")

# --- Team Members Area ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.image("https://placehold.co/400x400?text=Member+1", caption="### Amy Steward")
    # st.subheader("Amy Steward")
    st.write("**Role:** Data Analyst & Predictive Modeler")
    st.write("Fill in")

with col2:
    st.image("https://placehold.co/400x400?text=Member+2", caption="### Chad Adelman")
    # st.subheader("Chad Adelman")
    st.write("**Role:** Project Manager & RAG Evaluator")
    st.write("Fill in")

with col3:
    st.image("https://placehold.co/400x400?text=Member+3", caption="### Kristen Lin")
    # st.subheader("Kristen Lin")
    st.write("**Role:** Data Infra & Frontend Developer")
    st.write("Built the Streamlit UI... Fill in")

with col4:
    st.image("https://placehold.co/400x400?text=Member+4", caption="### Vishnu Gorur")
    # st.subheader("Vishnu Gorur")
    st.write("**Role:** GenAI and ML Engineer")
    st.write("Fill in")

# --- Contact Section ---
st.divider()
st.header("Contact Us")
st.write("Have questions? Email us at wattson@berkeley.edu.")