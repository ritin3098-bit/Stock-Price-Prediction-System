📈 Stock Price Prediction System

A Django-based Stock Price Prediction System that combines web development and machine learning to provide stock-related predictions through a user-friendly web interface.

🚀 Project Overview

This project is built using Python, Django, Pandas, NumPy, and Machine Learning. It provides a web application where users can work with stock data and generate predictions through the Django interface.

The project is designed as a practical demonstration of integrating a machine-learning workflow into a Django web application.

Disclaimer: This project is for educational and demonstration purposes only. Stock-market predictions are inherently uncertain and should not be considered financial advice.

✨ Features

📊 Stock data processing and analysis

🤖 Machine-learning based stock prediction

🌐 Django web application

🔐 User registration and login

📜 Prediction/history functionality

📁 Stock data stored in CSV files

🧩 Django management command for loading stock data

🎨 HTML/CSS/JavaScript based interface

📱 Web-based prediction workflow

🛠️ Technologies Used

Backend

Python

Django

Machine Learning & Data Science

Pandas

NumPy

Scikit-learn

Frontend

HTML5

CSS3

JavaScript

Database

SQLite3 for local development

Data

stock_data_complete.csv

Tickers.csv

📂 Project Structure

Stock_prediction/
│
├── predictor/
│   ├── management/
│   │   └── commands/
│   │       └── load_stock_data.py
│   ├── migrations/
│   ├── static/
│   │   ├── css/
│   │   │   ├── auth.css
│   │   │   ├── history.css
│   │   │   └── style.css
│   │   └── js/
│   │       └── script.js
│   ├── templates/
│   │   ├── registration/
│   │   │   ├── login.html
│   │   │   └── signup.html
│   │   └── stock_predictor/
│   │       ├── history.html
│   │       └── index.html
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── tests.py
│
├── Stock_prediction/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
├── stock_data_complete.csv
├── Tickers.csv
├── db.sqlite3
└── README.md

💻 Installation

1. Clone the repository

git clone https://github.com/ritin3098-bit/Stock-Price-Prediction-Sysytem.git
cd Stock-Price-Prediction-Sysytem

2. Create a virtual environment

Windows:

python -m venv venv

Activate it:

venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Apply migrations

python manage.py migrate

5. Load stock data

If your project uses the included management command:

python manage.py load_stock_data

6. Create an admin user

python manage.py createsuperuser

Follow the prompts to create your Django administrator account.

7. Start the development server

python manage.py runserver

Open:

http://127.0.0.1:8000/

🔄 Application Workflow

User
  ↓
Django Web Interface
  ↓
Select / Enter Stock Information
  ↓
Stock Data Processing
  ↓
Machine Learning Model
  ↓
Prediction
  ↓
Display Result
  ↓
Save / View Prediction History

📊 Dataset

The project includes stock-market data in:

stock_data_complete.csv

Ticker information is stored in:

Tickers.csv

The dataset can be processed and loaded into the Django application using the included management command.

🤖 Machine Learning

The machine-learning component is integrated into the Django application to process stock information and generate predictions.

The general workflow is:

Load stock data

Clean and preprocess the data

Select relevant features

Train/use the machine-learning model

Generate predictions

Display predictions through Django

The exact prediction performance depends on the dataset, model, features, and market conditions.

🔐 Security Notes

Before deploying this application publicly:

Set DEBUG = False

Use a secure Django SECRET_KEY

Configure ALLOWED_HOSTS

Do not commit .env files or API keys

Use environment variables for secrets

Configure production static files

Use a production database instead of SQLite where appropriate

🌐 Deployment

This project can be deployed using platforms such as:

Render

Railway

PythonAnywhere

Other Django-compatible cloud platforms

For production deployment, use a production WSGI/ASGI server such as Gunicorn rather than Django's development server.

🧪 Testing

Run Django's test suite with:

python manage.py test

You can also check the project configuration with:

python manage.py check

Before production deployment, use Django's deployment checks where appropriate.

🔮 Future Improvements

Possible improvements include:

📈 Interactive stock charts

📅 Historical price visualization

🔄 Automated market-data updates

🧠 More advanced ML/deep-learning models

📊 Model performance comparison

☁️ Cloud database integration

🔔 Price/prediction alerts

📱 Improved responsive design

🔑 API-based stock data integration

🚀 Production deployment with PostgreSQL

👨‍💻 Author

Ritin Setia

GitHub:
https://github.com/ritin3098-bit

📄 License

This project is intended for educational and portfolio purposes.

⚠️ Disclaimer

Stock-market prediction is a complex problem and no machine-learning model can guarantee future prices. Predictions generated by this application should not be interpreted as financial, investment, or trading advice.
