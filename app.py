import streamlit as st
import requests
import re
from datetime import datetime

# -----------------------------
# CONFIG
# -----------------------------
RAPID_API_KEY = "YOUR_RAPID_API_KEY"
RAPID_HOST = "google-search74.p.rapidapi.com"
URL = "https://google-search74.p.rapidapi.com/api/v1/search"

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.title("📊 LinkedIn Workforce Velocity Tracker")

company = st.text_input("Enter Company Name")

if st.button("Fetch Employee Count"):

    if company:

        querystring = {
            "q": f'site:linkedin.com/company {company} "employees"',
            "limit": "5"
        }

        headers = {
            "X-RapidAPI-Key": RAPID_API_KEY,
            "X-RapidAPI-Host": RAPID_HOST
        }

        response = requests.get(URL, headers=headers, params=querystring)
        data = response.json()

        try:
            snippet = data["results"][0]["description"]

            match = re.search(r'([\d,]+)\s+employees', snippet)

            if match:
                employee_count = int(match.group(1).replace(",", ""))

                st.success(f"LinkedIn Employees: {employee_count}")

                # Simple demo trend logic (fake previous value)
                previous_value = employee_count - 50  # simulate last snapshot

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

        except:
            st.error("Could not fetch data. Try another company.")

    else:
        st.warning("Please enter a company name.")
