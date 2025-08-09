import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import calendar

def create_metrics_cards(df_reviews, df_bookings):
    """Create beautiful metric cards with key performance indicators."""
    
    # Calculate metrics
    total_reviews = len(df_reviews)
    total_bookings = len(df_bookings)
    avg_nights = df_bookings['nights'].mean()
    total_revenue = df_bookings['total_spent'].sum()
    avg_spent_per_night = df_bookings['total_spent'].sum() / df_bookings['nights'].sum()
    
    # Create metric columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📊 Total Reviews",
            value=f"{total_reviews:,}",
            delta=f"+{total_reviews//10}" if total_reviews > 0 else "0"
        )
    
    with col2:
        st.metric(
            label="🏨 Total Bookings",
            value=f"{total_bookings:,}",
            delta=f"+{total_bookings//10}" if total_bookings > 0 else "0"
        )
    
    with col3:
        st.metric(
            label="🌙 Avg Nights",
            value=f"{avg_nights:.1f}",
            delta=f"{avg_nights - 3:.1f}" if avg_nights > 3 else f"{avg_nights - 3:.1f}"
        )
    
    with col4:
        st.metric(
            label="💰 Total Revenue",
            value=f"${total_revenue:,.0f}",
            delta=f"${total_revenue//10:,.0f}" if total_revenue > 0 else "$0"
        )

def create_sentiment_analysis_charts(df_reviews):
    """Create comprehensive sentiment analysis visualizations."""
    
    st.subheader("📝 Sentiment Analysis Dashboard")
    
    # Sentiment distribution pie chart
    sentiment_counts = df_reviews['sentiment'].value_counts()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Create pie chart
        fig_pie = px.pie(
            values=sentiment_counts.values,
            names=sentiment_counts.index,
            title="Sentiment Distribution",
            color_discrete_map={
                'POSITIVE': '#00FF88',
                'NEGATIVE': '#FF6B6B',
                'NEUTRAL': '#4ECDC4'
            }
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Sentiment metrics
        st.markdown("### Sentiment Metrics")
        for sentiment, count in sentiment_counts.items():
            percentage = (count / len(df_reviews)) * 100
            color = "🟢" if sentiment == "POSITIVE" else "🔴" if sentiment == "NEGATIVE" else "🟡"
            st.metric(
                label=f"{color} {sentiment}",
                value=f"{count:,}",
                delta=f"{percentage:.1f}%"
            )

def create_customer_segmentation_charts(df_bookings):
    """Create comprehensive customer segmentation visualizations."""
    
    st.subheader("👥 Customer Segmentation Analysis")
    
    # Ensure segment column exists
    if "segment" not in df_bookings.columns:
        from clustering import segment_customers
        segments = segment_customers(df_bookings)
        if isinstance(segments, tuple):
            segments = segments[0]
        df_bookings["segment"] = segments
    
    # Segment analysis
    segment_stats = df_bookings.groupby('segment').agg({
        'nights': ['mean', 'count'],
        'total_spent': ['mean', 'sum']
    }).round(2)
    
    segment_stats.columns = ['Avg Nights', 'Count', 'Avg Spent', 'Total Revenue']
    segment_stats = segment_stats.reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue by segment bar chart
        fig_bar = px.bar(
            segment_stats,
            x='segment',
            y='Total Revenue',
            title="Total Revenue by Customer Segment",
            color='segment',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_bar.update_layout(height=400, xaxis_title="Customer Segment", yaxis_title="Total Revenue ($)")
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        # Nights vs Total Spent scatter plot
        fig_scatter = px.scatter(
            df_bookings,
            x='nights',
            y='total_spent',
            color='segment',
            title="Nights vs Total Spent by Segment",
            color_discrete_sequence=px.colors.qualitative.Set3,
            size='total_spent',
            hover_data=['customer_id']
        )
        fig_scatter.update_layout(height=400, xaxis_title="Number of Nights", yaxis_title="Total Spent ($)")
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Segment statistics table
    st.markdown("### 📊 Segment Statistics")
    st.dataframe(
        segment_stats.style.highlight_max(axis=0, color='lightgreen').highlight_min(axis=0, color='lightcoral'),
        use_container_width=True
    )

def create_revenue_analysis_charts(df_bookings):
    """Create comprehensive revenue analysis visualizations."""
    
    st.subheader("💰 Revenue Analysis Dashboard")
    
    # Create subplots for different revenue metrics
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Revenue Distribution', 'Revenue by Nights', 'Cumulative Revenue', 'Revenue Trends'),
        specs=[[{"type": "histogram"}, {"type": "bar"}],
               [{"type": "scatter"}, {"type": "line"}]]
    )
    
    # Revenue distribution histogram
    fig.add_trace(
        go.Histogram(x=df_bookings['total_spent'], name='Revenue Distribution', nbinsx=20),
        row=1, col=1
    )
    
    # Revenue by nights
    nights_revenue = df_bookings.groupby('nights')['total_spent'].sum().reset_index()
    fig.add_trace(
        go.Bar(x=nights_revenue['nights'], y=nights_revenue['total_spent'], name='Revenue by Nights'),
        row=1, col=2
    )
    
    # Cumulative revenue
    sorted_bookings = df_bookings.sort_values('total_spent')
    cumulative_revenue = sorted_bookings['total_spent'].cumsum()
    fig.add_trace(
        go.Scatter(x=sorted_bookings['total_spent'], y=cumulative_revenue, name='Cumulative Revenue'),
        row=2, col=1
    )
    
    # Revenue trends (assuming customer_id represents time order)
    fig.add_trace(
        go.Scatter(x=df_bookings['customer_id'], y=df_bookings['total_spent'], name='Revenue Trends'),
        row=2, col=2
    )
    
    fig.update_layout(height=600, title_text="Revenue Analysis Overview")
    st.plotly_chart(fig, use_container_width=True)

def create_booking_patterns_charts(df_bookings):
    """Create booking patterns and trends visualizations."""
    
    st.subheader("📅 Booking Patterns & Trends")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Nights distribution
        fig_nights = px.histogram(
            df_bookings,
            x='nights',
            title="Distribution of Booking Durations",
            nbins=10,
            color_discrete_sequence=['#636EFA']
        )
        fig_nights.update_layout(height=400, xaxis_title="Number of Nights", yaxis_title="Frequency")
        st.plotly_chart(fig_nights, use_container_width=True)
    
    with col2:
        # Spending patterns
        fig_spending = px.box(
            df_bookings,
            y='total_spent',
            title="Spending Distribution",
            color_discrete_sequence=['#00CC96']
        )
        fig_spending.update_layout(height=400, yaxis_title="Total Spent ($)")
        st.plotly_chart(fig_spending, use_container_width=True)
    
    # Advanced patterns
    st.markdown("### 🔍 Advanced Patterns")
    
    # Create correlation heatmap
    correlation_matrix = df_bookings[['nights', 'total_spent']].corr()
    
    fig_heatmap = px.imshow(
        correlation_matrix,
        title="Correlation Matrix: Nights vs Total Spent",
        color_continuous_scale='RdBu',
        aspect='auto'
    )
    fig_heatmap.update_layout(height=400)
    st.plotly_chart(fig_heatmap, use_container_width=True)

def create_interactive_filters(df_reviews, df_bookings):
    """Create interactive filters for the dashboard."""
    
    st.sidebar.markdown("## 🔍 Dashboard Filters")
    
    # Date range filter (if date columns exist)
    if 'date' in df_bookings.columns:
        min_date = df_bookings['date'].min()
        max_date = df_bookings['date'].max()
        date_range = st.sidebar.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
    
    # Nights filter
    min_nights = int(df_bookings['nights'].min())
    max_nights = int(df_bookings['nights'].max())
    nights_range = st.sidebar.slider(
        "Number of Nights",
        min_value=min_nights,
        max_value=max_nights,
        value=(min_nights, max_nights)
    )
    
    # Revenue filter
    min_revenue = int(df_bookings['total_spent'].min())
    max_revenue = int(df_bookings['total_spent'].max())
    revenue_range = st.sidebar.slider(
        "Revenue Range ($)",
        min_value=min_revenue,
        max_value=max_revenue,
        value=(min_revenue, max_revenue)
    )
    
    # Segment filter
    if "segment" in df_bookings.columns:
        segments = df_bookings['segment'].unique()
        selected_segments = st.sidebar.multiselect(
            "Customer Segments",
            options=segments,
            default=segments.tolist()
        )
    
    # Apply filters
    filtered_bookings = df_bookings[
        (df_bookings['nights'] >= nights_range[0]) &
        (df_bookings['nights'] <= nights_range[1]) &
        (df_bookings['total_spent'] >= revenue_range[0]) &
        (df_bookings['total_spent'] <= revenue_range[1])
    ]
    
    if 'selected_segments' in locals():
        filtered_bookings = filtered_bookings[filtered_bookings['segment'].isin(selected_segments)]
    
    return filtered_bookings

def create_summary_insights(df_reviews, df_bookings):
    """Create summary insights and key takeaways."""
    
    st.subheader("💡 Key Insights & Takeaways")
    
    # Calculate insights
    total_revenue = df_bookings['total_spent'].sum()
    avg_nights = df_bookings['nights'].mean()
    avg_spent_per_night = df_bookings['total_spent'].sum() / df_bookings['nights'].sum()
    
    # Sentiment insights
    if 'sentiment' in df_reviews.columns:
        positive_reviews = len(df_reviews[df_reviews['sentiment'] == 'POSITIVE'])
        negative_reviews = len(df_reviews[df_reviews['sentiment'] == 'NEGATIVE'])
        satisfaction_rate = (positive_reviews / len(df_reviews)) * 100 if len(df_reviews) > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"**Revenue Insights**\n\n💰 Total Revenue: ${total_revenue:,.0f}\n🌙 Avg Nights: {avg_nights:.1f}\n💸 Avg per Night: ${avg_spent_per_night:.0f}")
    
    with col2:
        if 'sentiment' in df_reviews.columns:
            st.success(f"**Customer Satisfaction**\n\n😊 Positive: {positive_reviews}\n😞 Negative: {negative_reviews}\n📈 Rate: {satisfaction_rate:.1f}%")
    
    with col3:
        # Top performing metrics
        top_revenue_booking = df_bookings.loc[df_bookings['total_spent'].idxmax()]
        st.warning(f"**Top Performance**\n\n🏆 Highest Revenue: ${top_revenue_booking['total_spent']:,.0f}\n👤 Customer ID: {top_revenue_booking['customer_id']}\n🌙 Nights: {top_revenue_booking['nights']}")

def apply_custom_css():
    """Apply custom CSS styling to improve the dashboard appearance."""
    
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    
    .stMetric {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stPlotlyChart {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stDataFrame {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
