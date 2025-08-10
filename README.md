
# 🏨 Hotel Agent: AI Hospitality Analytics

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![GitHub Stars](https://img.shields.io/github/stars/YOUR_USERNAME/advanced-messy-data-generator.svg)
![GitHub Issues](https://img.shields.io/github/issues/YOUR_USERNAME/advanced-messy-data-generator.svg)
![GitHub Forks](https://img.shields.io/github/forks/YOUR_USERNAME/advanced-messy-data-generator.svg)
tags: [AI, Hospitality, Analytics, Streamlit, NLP, Machine Learning, Dashboard, Visualization]
emoji: 🏨📊🤖📝🎨

## Overview
Hotel Agent is an AI-powered analytics dashboard for hospitality businesses. It provides insights into guest reviews, customer segmentation, and booking behavior using machine learning and natural language processing, enhanced with **interactive visualizations** and **professional dashboards**.

## ✨ Enhanced Features 📊

### 🎨 **Advanced Visualizations**
- **Interactive Charts:** Plotly-powered charts with zoom, pan, and hover details
- **Professional Dashboards:** PowerBI-like experience with multiple dashboard views
- **Real-time Metrics:** Beautiful metric cards with delta indicators
- **Custom Styling:** Modern UI with gradient backgrounds and professional aesthetics

### 📝 **Sentiment Analysis Dashboard**
- **Pie Charts:** Visual sentiment distribution with color coding
- **Sentiment Metrics:** Real-time sentiment statistics and percentages
- **Interactive Tables:** Color-coded review results with filtering

### 👥 **Customer Segmentation Analysis**
- **Bar Charts:** Revenue analysis by customer segments
- **Scatter Plots:** Nights vs. Total Spent with segment coloring
- **Statistics Tables:** Highlighted segment performance metrics

### 💰 **Revenue Analysis Dashboard**
- **Multi-panel Charts:** 4-in-1 revenue overview with histograms, bars, and trends
- **Distribution Analysis:** Revenue patterns and cumulative analysis
- **Interactive Filters:** Real-time data filtering and exploration

### 📅 **Booking Patterns & Trends**
- **Histograms:** Booking duration distributions
- **Box Plots:** Spending pattern analysis
- **Correlation Heatmaps:** Nights vs. Total Spent relationships

### 🔍 **Interactive Data Explorer**
- **Dynamic Filters:** Nights, revenue, and segment-based filtering
- **Export Functionality:** Download filtered data as CSV
- **Real-time Updates:** Live dashboard updates based on filter changes

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation Options

#### Option 1: Automatic Installation (Recommended)
Run the installation script:
```bash
# Windows
install.bat

# Or cross-platform
python install.py
```

#### Option 2: Manual Installation
1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd hotel-agent-1
   ```

2. **Install PyTorch first (to avoid wheel building issues):**
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
   ```

3. **Install remaining dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

#### Option 3: Docker Installation
```bash
# Build the Docker image
docker build -t hotel-agent .

# Run the container
docker run -p 8501:8501 hotel-agent
```

### Generate Sample Data
For demonstration purposes, generate realistic sample data:
```bash
python data_generator.py
```

### Running the Application
```bash
streamlit run app/main.py
```

The application will be available at `http://localhost:8501`

## 🎯 Dashboard Navigation

The enhanced application features **7 specialized dashboard views**:

1. **📊 Overview Dashboard** - Key metrics and summary insights
2. **📝 Sentiment Analysis** - Customer satisfaction visualization
3. **👥 Customer Segmentation** - Customer behavior analysis
4. **💰 Revenue Analysis** - Financial performance deep-dive
5. **📅 Booking Patterns** - Trend analysis and correlations
6. **🤖 AI Summary** - AI-generated business insights
7. **🔍 Data Explorer** - Interactive data filtering and export

## 🔧 Troubleshooting

### PyTorch Installation Issues
If you encounter "Failed to build installable wheels for PyTorch" error:

1. **Use the automatic installation script:**
   ```bash
   python install.py
   ```

2. **Or install PyTorch manually:**
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
   ```

3. **Alternative: Use conda (if available):**
   ```bash
   conda install pytorch torchvision torchaudio cpuonly -c pytorch
   ```

### Common Issues
- **Memory issues:** Ensure you have at least 4GB RAM available
- **Python version:** Make sure you're using Python 3.8+
- **Virtual environment:** Consider using a virtual environment for isolation

## 📁 File Structure
- `app/` - Main application code
  - `main.py` - Enhanced Streamlit dashboard with navigation
  - `visualizations.py` - **NEW:** Advanced visualization functions
  - `sentiment_model.py` - Sentiment analysis logic
  - `clustering.py` - Customer segmentation logic
  - `summarizer.py` - AI summary generation
- `data/` - CSV data files (`reviews.csv`, `bookings.csv`)
- `data_generator.py` - **NEW:** Sample data generator
- `requirements.txt` - Python dependencies (including Plotly)
- `install.py` - Automatic installation script
- `install.bat` - Windows installation script
- `Dockerfile` / `docker-compose.yml` - Containerization support

## 🧠 Models Used
- Sentiment: `distilbert/distilbert-base-uncased-finetuned-sst-2-english`
- Summarization: `facebook/bart-large-cnn`

## 🎨 Visualization Technologies
- **Plotly:** Interactive charts and professional visualizations
- **Streamlit:** Modern web application framework
- **Custom CSS:** Professional styling and gradient backgrounds
- **Responsive Design:** Mobile-friendly dashboard layouts

## 🛠️ Customization
- **Add new visualizations** in `visualizations.py`
- **Modify dashboard layouts** in `main.py`
- **Customize styling** in the `apply_custom_css()` function
- **Extend data analysis** in the respective analysis modules

## 📊 Sample Data
The application includes a data generator that creates realistic hotel data:
- **100 customer reviews** with realistic sentiment distribution
- **200 booking records** with customer segmentation
- **Realistic pricing patterns** and booking durations
- **Multiple customer segments** (Budget, Standard, Premium, Luxury)

## 🚀 Performance Features
- **Data caching** for faster loading
- **Lazy loading** of AI models
- **Optimized visualizations** with Plotly
- **Responsive UI** with professional styling

## License 📄
MIT License
