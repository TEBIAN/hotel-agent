from transformers import pipeline

def generate_summary(df_reviews, df_bookings):
    # Use a top summarization model from Hugging Face
    summary_pipe = pipeline("summarization", model="facebook/bart-large-cnn")
    # Prepare summary prompt with average revenue and segment explanation
    avg_revenue = df_bookings["total_spent"].mean()
    segment_counts = df_bookings["segment"].value_counts().to_dict() if "segment" in df_bookings.columns else {}
    spent_per_night = df_bookings.groupby("segment")["spent_per_night"].mean().to_dict() if "spent_per_night" in df_bookings.columns else {}
    prompt = (
        f"Summarize guest feedback and booking behavior. "
        f"Average revenue per booking: {avg_revenue:.2f}. "
        f"Segment counts: {segment_counts}. "
        f"Average spent per night by segment: {spent_per_night}. "
        f"Explain the main trends shown in the graphs. "
        f"Reviews: {'. '.join(df_reviews['review'].astype(str).tolist()[:5])}"
    )
    summary = summary_pipe(prompt, max_length=150, min_length=50, do_sample=False)[0]['summary_text']
    return summary