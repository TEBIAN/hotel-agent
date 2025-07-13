# Hotel Agent: AI Hospitality Analytics

## Overview
Hotel Agent is an AI-powered analytics dashboard for hospitality businesses. It provides insights into guest reviews, customer segmentation, and booking behavior using machine learning and natural language processing.

## Features
- **Sentiment Analysis:** Automatically analyzes guest reviews to determine sentiment (positive/negative).
- **Customer Segmentation:** Groups customers based on booking patterns, total spent, and spending per night using KMeans clustering.
- **AI Summarization:** Generates a summary of guest feedback and booking trends using state-of-the-art NLP models.
- **Interactive Dashboard:** Built with Streamlit, featuring charts and tables for easy data exploration.

## How It Works
1. **Data Loading:** Loads reviews and bookings from CSV files in the `data/` folder.
2. **Sentiment Analysis:** Uses Hugging Face Transformers to classify review sentiment.
3. **Segmentation:** Clusters customers and explains segments with average nights, total spent, and spent per night.
4. **Summarization:** Summarizes key trends and metrics using a top-performing summarization model.
5. **Visualization:** Presents results in an interactive dashboard with charts and tables.

## Getting Started
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run app/main.py
   ```

## File Structure
- `app/` - Main application code
  - `main.py` - Streamlit dashboard
  - `sentiment_model.py` - Sentiment analysis logic
  - `clustering.py` - Customer segmentation logic
  - `summarizer.py` - AI summary generation
- `data/` - CSV data files (`reviews.csv`, `bookings.csv`)
- `requirements.txt` - Python dependencies
- `Dockerfile` / `docker-compose.yml` - Containerization support

## Models Used
- Sentiment: `distilbert/distilbert-base-uncased-finetuned-sst-2-english`
- Summarization: `facebook/bart-large-cnn`

## Customization
- Add more features or data columns in `clustering.py` for advanced segmentation.
- Replace or fine-tune models in `sentiment_model.py` and `summarizer.py` as needed.

## License
MIT License
