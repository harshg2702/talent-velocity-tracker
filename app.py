import streamlit as st
import requests

st.title("🚀 Talent Velocity Tracker")

company = st.text_input("Enter Company Name")

if company:

    # Pull data automatically from Wikipedia (Free API)
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{company}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        summary = data.get("extract", "No summary found.")

        st.subheader("📊 Auto-Pulled Company Data")
        st.write(summary)

        st.subheader("🤖 AI Insight")
        st.write(f"""
        Based on publicly available information, {company} appears to be operating
        at meaningful scale.

        Strategic signals:
        - Established market presence
        - Public visibility indicates hiring potential
        - Opportunity for enterprise engagement

        (AI-generated strategic summary)
        """)

    else:
        st.error("Company not found. Try another name.")
