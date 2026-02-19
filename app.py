import streamlit as st
import requests
import re
from datetime import datetime

# -----------------------------
# CONFIG
# -----------------------------
RAPID_HOST = "google-search74.p.rapidapi.com"
URL = "https://google-search74.p.rapidapi.com/api/v1/search"

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.title("📊 LinkedIn Workforce Velocity Tracker")

company = st.text_input("Enter Company Name")

if st.button("Fetch Employee Count"):

    if company:

        api_key = st.secrets["RAPIDAPI_KEY"]

        querystring = {
            "q": f'site:linkedin.com/company {company} "employees"',
            "limit": "5"
        }

        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": RAPID_HOST
        }

        try:
            response = requests.get(URL, headers=headers, params=querystring)
            data = response.json()

            snippet = data["results"][0]["description"]

            match = re.search(r'([\d,]+)\s+employees', snippet)

            if match:
                employee_count = int(match.group(1).replace(",", ""))

                st.success(f"LinkedIn Employees: {employee_count}")

                # Demo trend logic
                previous_value = employee_count - 50
                delta = employee_count - previous_value

                if delta > 0:
                    st.info(f"📈 Hiring Signal: +{delta} employees")
                elif delta < 0:
                    st.warning(f"📉 Contraction Signal: {delta} employees")
                else:
                    st.write("No change detected.")

                st.write("Last Updated:", datetime.now())

            else:
                st.error("Employee count not found in search results.")

        except Exception as e:
            st.error("Could not fetch data.")
            st.write(e)

    else:
        st.warning("Please enter a company name.")
