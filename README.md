# 📈 Stock Price Prediction System

A full-stack **Django web application** that integrates a **machine learning pipeline** to generate stock price predictions, complete with user authentication and prediction history tracking.

> ⚠️ **Disclaimer:** Built for educational and portfolio purposes. Predictions are not financial advice.

**[▶ Demo Video](https://drive.google.com/file/d/1yiLLWwpyOZGYzGjnm9g21GjmnuKuI_g3/view?usp=drive_link)**

---

## 🚀 Overview

This project demonstrates end-to-end ML integration into a production-style web app — from data ingestion and model training to serving predictions through a secured Django interface. It covers the full stack: backend architecture, data processing, model evaluation, and frontend delivery.

## ✨ Key Features

- 🤖 ML-based stock price prediction (multiple models benchmarked)
- 🌐 Django web application with a clean HTML/CSS/JS interface
- 🔐 User registration, login, and session-based access
- 📜 Prediction history tracking per user
- 📁 CSV-based data pipeline with a custom Django management command for data loading

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| **Backend** | Python, Django |
| **ML / Data** | Pandas, NumPy, Scikit-learn |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Database** | SQLite3 (dev) |

## 📊 Results

Two model families were benchmarked across multiple tickers (AAPL, MSFT, GOOGL) on held-out test data to compare predictive accuracy against computational cost:

| Model | Avg. R² | Avg. MAPE | Avg. Train Time | Avg. Inference Time |
|---|---|---|---|---|
| **Linear Regression** | **0.976** | **0.75%** | ~83 ms | ~0.001 ms/pred |
| LSTM | 0.553 | 3.47% | ~13.6 s | ~2.76 ms/pred |

**Key finding:** the Linear Regression baseline outperformed the LSTM model on this dataset — achieving higher R² and lower error across all three tickers, while training over 150x faster. This highlights a core ML engineering lesson: model complexity doesn't guarantee better performance, especially on limited or non-stationary financial time-series data. The evaluation pipeline (`evaluation_results.csv`) is included for full reproducibility across per-ticker metrics (RMSE, MAE, MAPE, R², latency).

## 📂 Project Structure

```
Stock_prediction/
├── predictor/
│   ├── management/commands/load_stock_data.py
│   ├── static/{css,js}/
│   ├── templates/{registration,stock_predictor}/
│   ├── models.py, views.py, urls.py, admin.py, tests.py
├── Stock_prediction/          # Django project settings
├── stock_data_complete.csv
├── Tickers.csv
├── requirements.txt
└── manage.py
```

## 💻 Quick Start

```bash
# Clone & enter the repo
git clone https://github.com/ritin3098-bit/Stock-Price-Prediction-Sysytem.git
cd Stock-Price-Prediction-Sysytem

# Set up environment
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt

# Initialize the app
python manage.py migrate
python manage.py load_stock_data
python manage.py createsuperuser
python manage.py runserver
```

Visit **http://127.0.0.1:8000/**

## 🔄 Application Workflow

```
User → Django Interface → Stock Selection → Data Processing
     → ML Model Inference → Prediction Display → History Log
```

## 🧪 Testing

```bash
python manage.py test    # Run test suite
python manage.py check   # Validate project config
```

## 🔮 Roadmap

- Interactive & historical price charts
- Automated market-data refresh via API
- Additional models + systematic performance comparison
- Cloud DB (PostgreSQL) + production deployment (Gunicorn)
- Prediction/price alerts

## 🔐 Production Checklist

`DEBUG=False` · secure `SECRET_KEY` · configured `ALLOWED_HOSTS` · env-based secrets · production static files & database

## 👨‍💻 Author

**Ritin Setia** — [GitHub](https://github.com/ritin3098-bit)

---
*Educational/portfolio project. Not financial advice.*should not be interpreted as financial, investment, or trading advice.
