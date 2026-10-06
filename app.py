import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(
    page_title="Multi-Source Web Scraping",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Multi-Source Web Scraping & Data Consolidation")
st.write(
    "Realisieren Technologies Assignment — "
    "Books to Scrape + Quotes to Scrape"
)

csv_path = "output/final_dataset.csv"
json_path = "output/summary_report.json"

if os.path.exists(json_path):
    with open(json_path, "r", encoding="utf-8") as file:
        summary = json.load(file)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Books",
        summary["final_records"]["Books to Scrape"]
    )

    col2.metric(
        "Quotes",
        summary["final_records"]["Quotes to Scrape"]
    )

    col3.metric(
        "Final Records",
        summary["final_records"]["total"]
    )

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)

    st.subheader("Final Consolidated Dataset")

    st.dataframe(
        df,
        use_container_width=True,
        height=500
    )

    st.download_button(
        "⬇️ Download CSV",
        data=df.to_csv(index=False),
        file_name="final_dataset.csv",
        mime="text/csv"
    )
else:
    st.error("Final dataset not found.")