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
        "limit": "5",
        "related_keywords": "true"
    }

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "google-search74.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    st.write("Status Code:", response.status_code)

    data = response.json()
    st.json(data)

    if response.status_code != 200:
        st.error("API call failed.")
        st.stop()

    if "results" not in data:
        st.error("Unexpected response format.")
        st.stop()

    snippet = data["results"][0].get("description", "")

    match = re.search(r'([\d,]+)\s+employees', snippet)

    if match:
        employee_count = int(match.group(1).replace(",", ""))

        st.success(f"LinkedIn Employees: {employee_count}")

        previous_value = employee_count - 50
        delta = employee_count - previous_value

        if delta > 0:
            st.info(f"📈 Hiring Signal: +{delta}")
        elif delta < 0:
            st.warning(f"📉 Contraction Signal: {delta}")
        else:
            st.write("No change detected.")

        st.write("Last Updated:", datetime.now())

    else:
        st.error("Employee count not found in snippet.")
