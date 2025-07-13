from sklearn.cluster import KMeans
import pandas as pd
from sklearn.preprocessing import StandardScaler

def segment_customers(df):
    df = df.copy()
    df["spent_per_night"] = df["total_spent"] / df["nights"]
    features = df[["nights", "total_spent", "spent_per_night"]]
    scaled = StandardScaler().fit_transform(features)
    kmeans = KMeans(n_clusters=3, random_state=42).fit(scaled)
    labels = kmeans.labels_
    # Explain segmentation
    explanation = []
    for i in range(3):
        group = df[labels == i]
        avg_nights = group["nights"].mean()
        avg_spent = group["total_spent"].mean()
        avg_spent_per_night = group["spent_per_night"].mean()
        explanation.append(
            f"Segment {i}: avg nights = {avg_nights:.2f}, avg spent = {avg_spent:.2f}, avg spent/night = {avg_spent_per_night:.2f}, count = {len(group)}"
        )
    print("Segmentation explanation:")
    for exp in explanation:
        print(exp)
    return labels