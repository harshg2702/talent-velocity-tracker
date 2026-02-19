import streamlit as st
import requests
import re
from datetime import datetime

st.title("📊 LinkedIn Workforce Velocity Tracker")

company = st.text_input("Enter Company Name")

if st.button("Fetch Employee Count"):

    if not company:
        st.warning("Please enter a company name.")
        st.stop()

    api_key = st.secrets["RAPIDAPI_KEY"]

    url = "https://google-search74.p.rapidapi.com/"

    querystring = {
        "query": f'site:linkedin.com/company {company} "employees"',
        "limit": "5"
    }

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "google-search74.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code != 200:
        st.error("API call failed. Please try again.")
        st.stop()

    data = response.json()

    if "results" not in data or len(data["results"]) == 0:
        st.error("No results found.")
        st.stop()

    snippet = data["results"][0].get("description", "")

    match = re.search(r'([\d,]+)\s+employees', snippet)

    if match:
        employee_count = int(match.group(1).replace(",", ""))

        st.success(f"{company} has approximately {employee_count:,} employees")
        st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    else:
        st.error("Employee count not found in search results.")
