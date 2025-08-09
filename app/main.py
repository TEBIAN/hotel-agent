import streamlit as st
import pandas as pd
from sentiment_model import analyze_sentiments
from clustering import segment_customers
from summarizer import generate_summary
from visualizations import (
    create_metrics_cards,
    create_sentiment_analysis_charts,
    create_customer_segmentation_charts,
    create_revenue_analysis_charts,
    create_booking_patterns_charts,
    create_interactive_filters,
    create_summary_insights,
    apply_custom_css
)
import os

# Page configuration
st.set_page_config(
    page_title="🏨 Hotel Agent - AI Hospitality Analytics",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
apply_custom_css()

# Load data
@st.cache_data
def load_data():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data')
    df_reviews = pd.read_csv(os.path.join(data_path, "reviews.csv"))
    df_bookings = pd.read_csv(os.path.join(data_path, "bookings.csv"))
    return df_reviews, df_bookings

df_reviews, df_bookings = load_data()

# Main header with gradient background
st.markdown("""
<div class="main-header">
    <h1>🏨 Hotel Agent: AI-Powered Hospitality Analytics</h1>
    <p>Transform your hospitality data into actionable insights with AI-driven analytics</p>
</div>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.markdown("## 🧭 Navigation")
page = st.sidebar.selectbox(
    "Choose a Dashboard",
    ["📊 Overview Dashboard", "📝 Sentiment Analysis", "👥 Customer Segmentation", 
     "💰 Revenue Analysis", "📅 Booking Patterns", "🤖 AI Summary", "🔍 Data Explorer"]
)

# Main content area
if page == "📊 Overview Dashboard":
    st.header("📊 Overview Dashboard")
    st.markdown("Get a comprehensive overview of your hospitality business performance")
    
    # Create metrics cards
    create_metrics_cards(df_reviews, df_bookings)
    
    # Create summary insights
    create_summary_insights(df_reviews, df_bookings)
    
    # Quick charts overview
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue trend
        revenue_trend = df_bookings.groupby('nights')['total_spent'].sum()
        st.line_chart(revenue_trend)
        st.caption("Revenue by Number of Nights")
    
    with col2:
        # Nights distribution
        nights_dist = df_bookings['nights'].value_counts().sort_index()
        st.bar_chart(nights_dist)
        st.caption("Distribution of Booking Durations")

elif page == "📝 Sentiment Analysis":
    st.header("📝 Sentiment Analysis Dashboard")
    st.markdown("Understand customer satisfaction through AI-powered sentiment analysis")
    
    # Run sentiment analysis
    with st.spinner("Analyzing customer sentiments..."):
        sentiments = analyze_sentiments(df_reviews["review"])
        df_reviews["sentiment"] = sentiments
    
    # Create sentiment charts
    create_sentiment_analysis_charts(df_reviews)
    
    # Detailed sentiment table
    st.markdown("### 📋 Detailed Sentiment Results")
    st.dataframe(
        df_reviews[['review', 'sentiment']].style.apply(
            lambda x: ['background-color: #e8f5e8' if v == 'POSITIVE' 
                      else 'background-color: #ffe8e8' if v == 'NEGATIVE' 
                      else 'background-color: #fff8e8' for v in x], 
            subset=['sentiment']
        ),
        use_container_width=True
    )

elif page == "👥 Customer Segmentation":
    st.header("👥 Customer Segmentation Analysis")
    st.markdown("Discover customer patterns and create targeted marketing strategies")
    
    # Run customer segmentation
    with st.spinner("Segmenting customers..."):
        segments = segment_customers(df_bookings)
        if isinstance(segments, tuple):
            segments = segments[0]
        df_bookings["segment"] = segments
    
    # Create segmentation charts
    create_customer_segmentation_charts(df_bookings)
    
    # Customer details table
    st.markdown("### 👤 Customer Details by Segment")
    st.dataframe(
        df_bookings.sort_values('segment')[['customer_id', 'nights', 'total_spent', 'segment']],
        use_container_width=True
    )

elif page == "💰 Revenue Analysis":
    st.header("💰 Revenue Analysis Dashboard")
    st.markdown("Deep dive into revenue patterns and financial performance")
    
    # Create revenue analysis charts
    create_revenue_analysis_charts(df_bookings)
    
    # Revenue statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Revenue", f"${df_bookings['total_spent'].sum():,.0f}")
    
    with col2:
        st.metric("Average Revenue per Booking", f"${df_bookings['total_spent'].mean():,.0f}")
    
    with col3:
        st.metric("Revenue per Night", f"${df_bookings['total_spent'].sum() / df_bookings['nights'].sum():,.0f}")

elif page == "📅 Booking Patterns":
    st.header("📅 Booking Patterns & Trends")
    st.markdown("Analyze booking behavior and identify trends")
    
    # Create booking patterns charts
    create_booking_patterns_charts(df_bookings)
    
    # Pattern insights
    st.markdown("### 📈 Pattern Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**Most Popular Duration:** {df_bookings['nights'].mode().iloc[0]} nights")
        st.info(f"**Peak Spending Range:** ${df_bookings['total_spent'].quantile(0.75):.0f} - ${df_bookings['total_spent'].max():.0f}")
    
    with col2:
        st.success(f"**Average Stay:** {df_bookings['nights'].mean():.1f} nights")
        st.success(f"**Revenue Range:** ${df_bookings['total_spent'].min():.0f} - ${df_bookings['total_spent'].max():.0f}")

elif page == "🤖 AI Summary":
    st.header("🤖 AI-Powered Business Summary")
    st.markdown("Get intelligent insights and recommendations from your data")
    
    # Check if sentiment analysis has been performed, if not, run it
    if 'sentiment' not in df_reviews.columns:
        with st.spinner("Running sentiment analysis for comprehensive insights..."):
            from sentiment_model import analyze_sentiments
            sentiments = analyze_sentiments(df_reviews["review"])
            df_reviews["sentiment"] = sentiments
    
    # Generate AI summary
    with st.spinner("Generating AI summary..."):
        summary = generate_summary(df_reviews, df_bookings)
    
    # Display summary in a nice format
    st.markdown("### 📊 AI-Generated Business Insights")
    st.info(summary)
    
    # Key metrics highlight
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Handle sentiment metrics safely
        if 'sentiment' in df_reviews.columns:
            positive_count = len(df_reviews[df_reviews['sentiment'] == 'POSITIVE'])
            total_reviews = len(df_reviews)
            st.metric("Customer Satisfaction", f"{positive_count}/{total_reviews}")
        else:
            st.metric("Customer Satisfaction", f"{len(df_reviews)} reviews")
    
    with col2:
        # Calculate revenue per night safely
        total_spent = df_bookings['total_spent'].sum()
        total_nights = df_bookings['nights'].sum()
        if total_nights > 0:
            revenue_per_night = total_spent / total_nights
            st.metric("Revenue Efficiency", f"${revenue_per_night:.0f}/night")
        else:
            st.metric("Revenue Efficiency", "$0/night")
    
    with col3:
        st.metric("Booking Conversion", f"{len(df_bookings)} bookings")

elif page == "🔍 Data Explorer":
    st.header("🔍 Interactive Data Explorer")
    st.markdown("Explore your data with interactive filters and detailed analysis")
    
    # Create interactive filters
    filtered_bookings = create_interactive_filters(df_reviews, df_bookings)
    
    # Display filtered data
    st.markdown(f"### 📊 Filtered Data ({len(filtered_bookings)} records)")
    st.dataframe(filtered_bookings, use_container_width=True)
    
    # Export functionality
    if st.button("📥 Export Filtered Data"):
        csv = filtered_bookings.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="filtered_hotel_data.csv",
            mime="text/csv"
        )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🏨 Hotel Agent - Powered by AI & Streamlit | Built for Hospitality Excellence</p>
</div>
""", unsafe_allow_html=True)