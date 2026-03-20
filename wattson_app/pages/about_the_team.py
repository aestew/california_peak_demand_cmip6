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
    st.image("https://raw.githubusercontent.com/aestew/california_peak_demand_cmip6/refs/heads/main/wattson_app/images/amy.png", caption="### Amy Steward")
    # st.subheader("Amy Steward")
    st.write("**Role:** Lead Researcher, ML Engineer")
   

with col2:
    st.image("https://raw.githubusercontent.com/aestew/california_peak_demand_cmip6/refs/heads/main/wattson_app/images/chad.png", caption="### Chad Adelman")
    # st.subheader("Chad Adelman")
    st.write("**Role:** RAG Evaluator & Data Support")
    

with col3:
    st.image("https://raw.githubusercontent.com/aestew/california_peak_demand_cmip6/refs/heads/main/wattson_app/images/kristen.png", caption="### Kristen Lin")
    # st.subheader("Kristen Lin")
    st.write("**Role:** Data Infra")

with col4:
    st.image("https://raw.githubusercontent.com/aestew/california_peak_demand_cmip6/refs/heads/main/wattson_app/images/vishnu.png", caption="### Vishnu Gorur")
    # st.subheader("Vishnu Gorur")
    st.write("**Role:** GenAI Engineer")


# --- Contact Section ---
st.divider()
st.header("Contact Us")
st.write("Have questions? Email us at asteward@berkeley.edu.")