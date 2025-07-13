import streamlit as st
import pandas as pd
from sentiment_model import analyze_sentiments
from clustering import segment_customers
from summarizer import generate_summary
import os

# Load data
data_path = os.path.join(os.path.dirname(__file__), '..', 'data')
df_reviews = pd.read_csv(os.path.join(data_path, "reviews.csv"))
df_bookings = pd.read_csv(os.path.join(data_path, "bookings.csv"))
print("Data loaded successfully.")
# Streamlit UI
st.set_page_config(page_title="AI Insight Engine", layout="wide")
st.title("AI Hospitality Analytics")

# Toggle for views
view = st.session_state.get("view", "main")

if view == "dashboard" or st.button("📊 Show Full Analysis Dashboard"):
    st.session_state.view = "dashboard"
    # Ensure segment column exists before plotting
    if "segment" not in df_bookings.columns:
        segments = segment_customers(df_bookings)
        if isinstance(segments, tuple):
            segments = segments[0]
        df_bookings["segment"] = segments
    st.markdown("""
    ## Full PowerBI-like Dashboard (Streamlit Embedded)
    - Key Metrics:
        - Total Reviews: **{}**
        - Avg Nights: **{:.1f}**
        - Total Revenue: **${}**
    - Segment Breakdown:
    """.format(
        len(df_reviews),
        df_bookings["nights"].mean(),
        df_bookings["total_spent"].sum()
    ))
    st.bar_chart(df_bookings.groupby("segment")["total_spent"].mean())
    st.line_chart(df_bookings["total_spent"])
    st.dataframe(df_bookings)
    if st.button("🔙 Return to Main View"):
        st.session_state.view = "main"
        st.rerun()
else:
    st.session_state.view = "main"
    st.subheader("1. Sentiment Analysis")
    sentiments = analyze_sentiments(df_reviews["review"])
    df_reviews["sentiment"] = sentiments
    st.write(df_reviews.head())

    st.subheader("2. Customer Segmentation")
    segments = segment_customers(df_bookings)
    df_bookings["segment"] = segments
    st.write(df_bookings.head())

    st.subheader("3. AI Summary")
    st.text(generate_summary(df_reviews, df_bookings))