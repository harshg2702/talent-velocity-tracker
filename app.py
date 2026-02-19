import streamlit as st
import requests
from openai import OpenAI
import json

st.title("🚀 Workforce Intelligence Engine")

PDL_API_KEY = st.secrets["PDL_API_KEY"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]


company = st.text_input("Enter Company Name")

if company:

    st.write("🔎 Pulling structured workforce data from People Data Labs...")

    url = "https://api.peopledatalabs.com/v5/company/search"

    elastic_query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"name": company}}
                ]
            }
        }
    }

    params = {
        "api_key": PDL_API_KEY,
        "query": json.dumps(elastic_query),
        "size": 1
    }

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200 and data.get("data"):

        company_data = data["data"][0]

        employee_count = company_data.get("employee_count", "Not Available")
        industry = company_data.get("industry", "Not Available")
        website = company_data.get("website", "Not Available")

        st.subheader("📊 Structured Workforce Data (PDL)")
        st.write(f"**Employee Count:** {employee_count}")
        st.write(f"**Industry:** {industry}")
        st.write(f"**Website:** {website}")

        prompt = f"""
        Company: {company}
        Employee Count: {employee_count}
        Industry: {industry}

        Provide a concise VC-style analysis of workforce scale and likely growth stage.
        """

      from openai import OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

ai_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a VC workforce intelligence analyst."},
        {"role": "user", "content": prompt}
    ]
)

insight = ai_response.choices[0].message.content


        st.subheader("🤖 AI Workforce Insight")
        st.write(insight)

    else:
        st.error("No structured company match found in People Data Labs.")
        st.json(data)
