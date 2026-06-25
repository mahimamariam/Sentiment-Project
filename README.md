# 🤖 AI Feedback Analytics

An AI-powered Sentiment Analysis Web Application built using **Python**, **Flask**, **Machine Learning**, and **SQLite**. This application analyzes customer feedback and predicts whether the sentiment is **Positive**, **Negative**, or **Neutral**.

---

## 📌 Project Overview

AI Feedback Analytics is a web application that allows users to enter customer reviews or feedback. The application uses a trained Machine Learning model to analyze the text and predict its sentiment. All predictions are stored in a SQLite database and can be viewed through a history page and analytics dashboard.

---

## ✨ Features

- 🔍 Analyze customer feedback
- 😊 Predict Positive, Negative, or Neutral sentiment
- 🤖 AI explanation for each prediction
- 📊 Analytics Dashboard
- 📈 Pie Chart & Bar Chart visualization
- 📝 Prediction History
- 🔎 Search previous predictions
- 🗑 Delete individual records
- 🧹 Clear all history
- 📥 Export prediction history to CSV
- 💾 SQLite database integration
- 🎨 Modern and responsive user interface

---

## 🛠 Technologies Used

- Python 3
- Flask
- Scikit-learn
- SQLite
- HTML5
- CSS3
- JavaScript
- Chart.js
- Joblib

---

## 📂 Project Structure

```
Sentiment-Project/
│
├── dataset/
│   └── sentiment_dataset.csv
│
├── static/
│   ├── style.css
│   └── script.js
│
├── templates/
│   ├── index.html
│   ├── history.html
│   └── analytics.html
│
├── app.py
├── train_model.py
├── sentiment_model.pkl
├── vectorizer.pkl
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/mahimamariam/Sentiment-Project.git
```

### 2. Open the project folder

```bash
cd Sentiment-Project
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

### 5. Open your browser

```
http://127.0.0.1:5001
```

---

## 📊 Application Pages

### 🏠 Home
- Enter customer feedback
- Predict sentiment
- View AI explanation
- Display confidence score

### 📜 History
- View all predictions
- Search feedback
- Delete records
- Clear history

### 📈 Analytics
- Total analyses
- Positive percentage
- Negative percentage
- Neutral percentage
- Pie Chart
- Bar Chart

---

## 📷 Sample Predictions

| Input | Prediction |
|-------|------------|
| I love this product! | Positive |
| The service was terrible. | Negative |
| The meeting starts at 10 AM. | Neutral |

---

## 👩‍💻 Developed By

**Mahima Mariam Sam**

B.Tech Computer Science Engineering

---

## 📧 Internship Project

**Project Title:**

AI Feedback Analytics – Sentiment Analysis Web Application using Flask and Machine Learning

---

## 📜 License

This project was developed for learning and internship purposes.
