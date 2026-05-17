import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
# following galing AI, not working and i have no idea kung paano rin gawin yung pie chart, so ignore this for now, baka may time pa ako to fix it later, pero for now, focus muna tayo sa ibang pages
#-PixelatedCorn
st.title("Data Metrics & Visual Summary")

with sqlite3.connect("Residents.db") as conn:
    df = pd.read_sql_query("SELECT * FROM residents", conn)

if df.empty:
    st.info("No processing data metrics profiles saved inside Residents.db source target framework yet.")
else:
    st.metric("Population Overview (Total Residents)", len(df))
    
    # Sex pie distribution plot element
    counts = df["sex"].value_counts()
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90)
    st.pyplot(fig)
