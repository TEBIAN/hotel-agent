from transformers import pipeline
import pandas as pd
import streamlit as st

def generate_summary(df_reviews, df_bookings):
    """
    Generate an AI-powered summary of the hotel data.
    Includes error handling and fallback options.
    """
    try:
        # Check if sentiment analysis has been performed
        if 'sentiment' not in df_reviews.columns:
            # If sentiment analysis hasn't been done, create a basic sentiment count
            sentiment_counts = {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0}
        else:
            sentiment_counts = df_reviews['sentiment'].value_counts().to_dict()
        
        # Calculate key metrics
        total_revenue = df_bookings["total_spent"].sum()
        avg_revenue = df_bookings["total_spent"].mean()
        avg_nights = df_bookings["nights"].mean()
        total_bookings = len(df_bookings)
        
        # Handle segment information if available
        segment_info = ""
        if "segment" in df_bookings.columns:
            segment_counts = df_bookings["segment"].value_counts().to_dict()
            segment_info = f"Customer segments: {segment_counts}. "
        
        # Calculate spent per night if the column exists, otherwise calculate it
        spent_per_night_info = ""
        if "spent_per_night" in df_bookings.columns:
            avg_spent_per_night = df_bookings["spent_per_night"].mean()
            spent_per_night_info = f"Average spent per night: ${avg_spent_per_night:.2f}. "
        else:
            # Calculate spent per night manually
            total_nights = df_bookings["nights"].sum()
            if total_nights > 0:
                avg_spent_per_night = total_revenue / total_nights
                spent_per_night_info = f"Average spent per night: ${avg_spent_per_night:.2f}. "
        
        # Prepare review summary
        review_summary = ""
        if len(df_reviews) > 0:
            # Take first 3 reviews for summary
            sample_reviews = df_reviews['review'].astype(str).tolist()[:3]
            review_summary = f"Sample reviews: {' | '.join(sample_reviews)}. "
        
        # Create a comprehensive prompt
        prompt = (
            f"Hotel Analytics Summary: "
            f"Total bookings: {total_bookings}. "
            f"Total revenue: ${total_revenue:,.0f}. "
            f"Average revenue per booking: ${avg_revenue:.2f}. "
            f"Average nights per stay: {avg_nights:.1f}. "
            f"{spent_per_night_info}"
            f"{segment_info}"
            f"Review sentiment distribution: {sentiment_counts}. "
            f"{review_summary}"
            f"Provide key insights and recommendations for hotel management."
        )
        
        # Truncate prompt if it's too long (transformers have limits)
        if len(prompt) > 1000:
            prompt = prompt[:1000] + "..."
        
        # Try to use the AI model for summarization
        try:
            # Check if transformers is available and model can be loaded
            summary_pipe = pipeline("summarization", model="facebook/bart-large-cnn")
            summary_result = summary_pipe(prompt, max_length=150, min_length=50, do_sample=False)
            summary = summary_result[0]['summary_text']
            
            # Ensure the summary is not empty
            if not summary or len(summary.strip()) < 10:
                raise Exception("Generated summary is too short or empty")
                
        except Exception as e:
            # Fallback to manual summary if AI model fails
            st.warning(f"AI model unavailable, using manual summary. Error: {str(e)}")
            summary = _generate_manual_summary(df_reviews, df_bookings, sentiment_counts, total_revenue, avg_revenue, avg_nights)
        
        return summary
        
    except Exception as e:
        # Ultimate fallback
        st.error(f"Summary generation failed: {str(e)}")
        return _generate_manual_summary(df_reviews, df_bookings, {}, 0, 0, 0)

def _generate_manual_summary(df_reviews, df_bookings, sentiment_counts, total_revenue, avg_revenue, avg_nights):
    """
    Generate a manual summary when AI model is unavailable.
    """
    summary_parts = []
    
    # Basic metrics
    summary_parts.append(f"📊 **Business Overview**: {len(df_bookings)} total bookings with ${total_revenue:,.0f} total revenue.")
    summary_parts.append(f"💰 **Average Performance**: ${avg_revenue:.0f} per booking, {avg_nights:.1f} nights average stay.")
    
    # Sentiment analysis
    if sentiment_counts and sum(sentiment_counts.values()) > 0:
        positive_count = sentiment_counts.get('POSITIVE', 0)
        negative_count = sentiment_counts.get('NEGATIVE', 0)
        total_reviews = sum(sentiment_counts.values())
        
        if total_reviews > 0:
            satisfaction_rate = (positive_count / total_reviews) * 100
            summary_parts.append(f"😊 **Customer Satisfaction**: {satisfaction_rate:.1f}% positive reviews ({positive_count}/{total_reviews}).")
    elif 'sentiment' in df_reviews.columns:
        # If sentiment analysis was done but not passed to this function
        positive_count = len(df_reviews[df_reviews['sentiment'] == 'POSITIVE'])
        total_reviews = len(df_reviews)
        if total_reviews > 0:
            satisfaction_rate = (positive_count / total_reviews) * 100
            summary_parts.append(f"😊 **Customer Satisfaction**: {satisfaction_rate:.1f}% positive reviews ({positive_count}/{total_reviews}).")
    
    # Segment information
    if "segment" in df_bookings.columns and len(df_bookings) > 0:
        segment_counts = df_bookings["segment"].value_counts()
        if len(segment_counts) > 0:
            top_segment = segment_counts.index[0]
            top_segment_count = segment_counts.iloc[0]
            summary_parts.append(f"👥 **Customer Segments**: Top segment is {top_segment} with {top_segment_count} customers.")
    
    # Recommendations based on data
    if len(df_bookings) > 0:
        if avg_revenue < 300:
            summary_parts.append("💡 **Recommendation**: Consider premium pricing strategies to increase average revenue.")
        elif avg_nights < 2:
            summary_parts.append("💡 **Recommendation**: Focus on extending guest stays with attractive packages.")
        else:
            summary_parts.append("💡 **Recommendation**: Continue monitoring key metrics and customer feedback.")
    
    return " ".join(summary_parts)