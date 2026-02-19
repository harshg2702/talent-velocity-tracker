import streamlit as st
import requests
import openai
import pandas as pd

SERP_API_KEY = st.secrets["SERP_API_KEY"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

openai.api_key = OPENAI_API_KEY

st.title("🚀 Talent Velocity Tracker")

company = st.text_input("Enter Company Name")

if company:

    params = {
        "engine": "google_jobs",
        "q": f"{company} jobs",
        "api_key": SERP_API_KEY
    }

    response = requests.get("https://serpapi.com/search", params=params)
    jobs_data = response.json()

    job_titles = []
    if "jobs_results" in jobs_data:
        for job in jobs_data["jobs_results"][:10]:
            job_titles.append(job["title"])

    if job_titles:
        st.subheader("Recent Job Titles")
        st.write(job_titles)

        prompt = f"""
        Classify these job titles into:
        - GTM
        - Engineering/Product
        - Operations
        - Leadership

        Return only a list in format:
        Job Title - Category

        {job_titles}
        """

        ai_response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        result = ai_response["choices"][0]["message"]["content"]

        st.subheader("AI Role Classification")
        st.write(result)

        interpretation_prompt = f"""
        Based on these job titles:
        {job_titles}

        Write a short VC-style insight about what this hiring mix suggests.
        """

        interpretation = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": interpretation_prompt}]
        )

        st.subheader("AI Strategic Interpretation")
        st.write(interpretation["choices"][0]["message"]["content"])
