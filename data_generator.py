#!/usr/bin/env python3
"""
Data Generator for Hotel Agent
Creates realistic sample data for demonstration purposes.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sample_data():
    """Generate realistic sample data for hotel analytics."""
    
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Generate sample reviews
    positive_reviews = [
        "Excellent service and very clean rooms!",
        "Amazing location and friendly staff.",
        "Great value for money, highly recommended!",
        "Perfect stay, will definitely return.",
        "Outstanding hospitality and beautiful facilities.",
        "Staff went above and beyond expectations.",
        "Clean, comfortable, and convenient location.",
        "Wonderful experience, exceeded all expectations.",
        "Professional service and excellent amenities.",
        "Best hotel experience I've had in years!"
    ]
    
    negative_reviews = [
        "Poor service and dirty rooms.",
        "Staff was rude and unhelpful.",
        "Overpriced for what you get.",
        "Noisy and uncomfortable beds.",
        "Terrible customer service experience.",
        "Room was not clean upon arrival.",
        "Staff ignored our complaints.",
        "Facilities were outdated and broken.",
        "Worst hotel experience ever.",
        "Don't waste your money here."
    ]
    
    neutral_reviews = [
        "Average experience, nothing special.",
        "Room was okay, service was standard.",
        "Met basic expectations, nothing more.",
        "Decent place to stay for the night.",
        "Standard hotel with standard service.",
        "Not bad, but not great either.",
        "Basic amenities, basic experience.",
        "Satisfactory for a business trip.",
        "Mediocre service and facilities.",
        "Acceptable but forgettable stay."
    ]
    
    # Generate 100 reviews with realistic sentiment distribution
    reviews_data = []
    for i in range(100):
        sentiment_choice = np.random.choice(['POSITIVE', 'NEGATIVE', 'NEUTRAL'], p=[0.6, 0.2, 0.2])
        
        if sentiment_choice == 'POSITIVE':
            review = random.choice(positive_reviews)
        elif sentiment_choice == 'NEGATIVE':
            review = random.choice(negative_reviews)
        else:
            review = random.choice(neutral_reviews)
        
        reviews_data.append({
            'review': review,
            'sentiment': sentiment_choice
        })
    
    # Generate 200 bookings with realistic patterns
    bookings_data = []
    
    # Create different customer segments
    segments = ['Budget', 'Standard', 'Premium', 'Luxury']
    
    for i in range(200):
        # Generate realistic nights (1-14 nights, weighted towards shorter stays)
        # Probabilities must sum to 1: 0.3 + 0.25 + 0.15 + 0.1 + 0.08 + 0.05 + 0.03 + 0.02 + 0.01 + 0.004 + 0.004 + 0.004 + 0.004 + 0.003 = 1.0
        nights = np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], 
                                p=[0.3, 0.25, 0.15, 0.1, 0.08, 0.05, 0.03, 0.02, 0.01, 0.004, 0.004, 0.004, 0.004, 0.003])
        
        # Generate realistic spending based on nights and segment
        base_price_per_night = np.random.choice([80, 120, 200, 350], p=[0.4, 0.35, 0.2, 0.05])
        
        # Add some variation
        price_variation = np.random.normal(1, 0.2)
        total_spent = int(base_price_per_night * nights * price_variation)
        
        # Ensure minimum reasonable price
        total_spent = max(total_spent, 50 * nights)
        
        # Assign segment based on spending
        if total_spent / nights < 100:
            segment = 'Budget'
        elif total_spent / nights < 150:
            segment = 'Standard'
        elif total_spent / nights < 250:
            segment = 'Premium'
        else:
            segment = 'Luxury'
        
        bookings_data.append({
            'customer_id': i + 1,
            'nights': nights,
            'total_spent': total_spent,
            'segment': segment,
            'price_per_night': round(total_spent / nights, 2)
        })
    
    # Create DataFrames
    df_reviews = pd.DataFrame(reviews_data)
    df_bookings = pd.DataFrame(bookings_data)
    
    return df_reviews, df_bookings

def save_sample_data():
    """Save generated sample data to CSV files."""
    
    df_reviews, df_bookings = generate_sample_data()
    
    # Save to data directory
    df_reviews.to_csv('data/reviews.csv', index=False)
    df_bookings.to_csv('data/bookings.csv', index=False)
    
    print("✅ Sample data generated successfully!")
    print(f"📝 Reviews: {len(df_reviews)} records")
    print(f"🏨 Bookings: {len(df_bookings)} records")
    print("\n📊 Data Overview:")
    print(f"   - Sentiment Distribution: {df_reviews['sentiment'].value_counts().to_dict()}")
    print(f"   - Customer Segments: {df_bookings['segment'].value_counts().to_dict()}")
    print(f"   - Total Revenue: ${df_bookings['total_spent'].sum():,}")
    print(f"   - Average Nights: {df_bookings['nights'].mean():.1f}")

if __name__ == "__main__":
    save_sample_data()
