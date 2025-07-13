from transformers import pipeline
def analyze_sentiments(reviews):
    # Specify model and revision explicitly for production use
    classifier = pipeline(
        "sentiment-analysis",
        model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
        revision="714eb0f",
        device=-1  # Use CPU
    )
    return [result["label"] for result in classifier(reviews.tolist())]