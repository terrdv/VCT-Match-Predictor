# VCT Outcome Predictor Website

The **VCT Outcome Predictor** is a full-stack web application that predicts match outcomes for the Valorant Champions Tour (VCT). It combines machine learning, a Flask API backend, and a modern React frontend to deliver live predictions based on historical performance data and team metrics.

## 🌐 Live Demo

🔗 [https://main.dxzmyy40dxhqi.amplifyapp.com/]() (coming soon)

## 📦 Tech Stack

### Frontend
- **React**
- **Recharts** (for visualization)
- **Vite**

### Backend
- **Flask (Python)**
- **Pandas + Scikit-learn**
- **CSV-based storage**

---

## 🚀 Features

- 📊 Predicts VCT match winners based on team statistics
- 🔍 Clean UI with dynamic charts and probability displays
- 🌐 RESTful API serving prediction results
- 🧠 Machine learning model (e.g. Random Forest Classifier)
- 🔐 Deployment with proper environment & security configs

---

## 🛠️ Getting Started (Git Bash Terminal)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/VCT-Outcome-Predictor-Website.git
cd VCT-Outcome-Predictor-Website
```

### 2. Set-up backend
```
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements
python app.py
```

### 3. Install and run frontend

```
cd frontend
npm install
npm run dev
```







