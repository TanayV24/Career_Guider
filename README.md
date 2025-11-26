<div align="center">

# 🎓 Career Guider

### AI-Powered Career Recommendation Platform for Students (SSC/HSC)

![React](https://img.shields.io/badge/Frontend-React-61DAFB?style=for-the-badge&logo=react&logoColor=white)
![Flask](https://img.shields.io/badge/Backend-Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)

**An interactive questionnaire-based career guidance system that uses AI/NLP to analyze student responses and generate personalized career recommendations.**

[📖 Documentation](#features) | [🐛 Report Bug](https://github.com/TanayV24/Career_Guider/issues) | [💡 Request Feature](https://github.com/TanayV24/Career_Guider/issues)

</div>

---

## ✨ Features

### 🎓 Student-Focused Features
- 📝 **Interactive Questionnaire** (SSC/HSC level)
- 🤖 **AI/NLP Sentiment Analysis** of student answers  
- 💡 **Personalized Career Suggestions**  
- 📊 **Realtime Score + Progress Tracking**
- 🎨 **Smooth UI Flow** with motivation quotes & themed screens  

### 🔧 Technical Features
- ⚡ **Fast React UI**  
- 📡 **Flask REST API Backend**  
- 🧠 **Custom NLP Engine** (keywords + sentiment)  
- 🔐 **Session Tracking** for user progress  
- 🧹 **Modular Backend Architecture**  
- 🌐 **Fully Cross-Platform**  

---

## 🛠 Tech Stack

<table>
<tr>
<td width="50%" valign="top">

### Frontend (React)
- React 18  
- React Router  
- Axios  
- Custom CSS  
- React Hooks  
- .env API configuration  

</td>
<td width="50%" valign="top">

### Backend (Flask)
- Flask 3.x  
- Flask-CORS  
- Python 3.8+  
- Custom sentiment analyzer  
- RESTful API design  
- Modular service directory  

</td>
</tr>
</table>

---

## 📋 Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| 🐍 Python | 3.8+ | Backend / NLP |
| 🟢 Node.js | 14+ | React frontend |
| 📝 npm | Latest | Package management |
| 💻 Git | Latest | Version control |

---

## ⚙️ Installation & Setup

### 🚀 Quick Setup (5 Minutes)

#### 1️⃣ Clone Project
```bash
git clone https://github.com/TanayV24/Career_Guider.git
cd Career_Guider
````

---

### 🧩 Backend Setup (Flask)

```bash
cd backend
pip install -r requirements.txt
python run.py
```

Backend runs at:

```
http://localhost:5050
```

---

### 🎨 Frontend Setup (React)

Open new terminal:

```bash
cd frontend
npm install
npm start
```

Frontend runs at:

```
http://localhost:3000
```

---

## 🎮 How to Use

1. Select SSC or HSC mode
2. Answer questions interactively
3. NLP analyzes your responses
4. See your final recommended career fields
5. Restart or explore alternate pathways

---

# 📁 **🧩 Detailed Project Structure (Fully Expanded)**

*(Highly requested — now clean, accurate, professional)*

```
Career_Guider/
│
├── backend/                          # Flask Backend
│   ├── app/
│   │   ├── __init__.py               # App initialization + CORS setup
│   │   │
│   │   ├── routes/                   # All API endpoints
│   │   │   ├── api.py                # Main API: login, questions, NLP analysis, recommendations
│   │   │   └── test.py               # Health check / test endpoint
│   │   │
│   │   ├── services/                 # Core business logic
│   │   │   ├── nlp_engine.py         # Sentiment + keyword analyzer
│   │   │   ├── question_bank.py      # SSC/HSC question data
│   │   │   ├── recommender.py        # Career recommendation logic
│   │   │   └── utilities.py          # Helper functions (cleaning, preprocessing)
│   │   │
│   │   ├── models/ (optional)        # Future ML models or persistent structures
│   │   └── data/                     # Static or CSV data for NLP
│   │
│   ├── requirements.txt              # Python dependencies
│   └── run.py                        # Backend entry point
│
│
├── frontend/                         # React Frontend
│   ├── public/
│   │   ├── index.html                # App root HTML
│   │   └── favicon.ico               # Icon
│   │
│   ├── src/
│   │   ├── pages/                    # Page views
│   │   │   ├── LoginPage.jsx
│   │   │   ├── ModeSelection.jsx     # SSC/HSC mode screen
│   │   │   ├── QuestionPage.jsx      # Main questionnaire
│   │   │   ├── ResultsPage.jsx       # Result display
│   │   │   └── MotivationalQuote.jsx
│   │   │
│   │   ├── components/               # Reusable UI components
│   │   │   ├── ProgressBar.jsx
│   │   │   └── QuestionCard.jsx
│   │   │
│   │   ├── services/
│   │   │   └── api.js                # Axios wrapper for backend API
│   │   │
│   │   ├── styles/                   # Styling files
│   │   │   ├── App.css
│   │   │   └── question.css
│   │
│   │   ├── App.js                    # Route mounting
│   │   └── index.js                  # React entry point
│   │
│   ├── package.json                  # Frontend dependencies
│   └── .env                          # API URL config
│
│
├── screenshots/                      # Optional UI previews
├── .gitignore
└── README.md                         # (This file)
```

---

## 🔧 API Endpoints (Backend)

| Method | Endpoint                | Purpose                               |
| ------ | ----------------------- | ------------------------------------- |
| `POST` | `/api/login`            | Register/identify user                |
| `GET`  | `/api/questions/<mode>` | Load SSC or HSC questions             |
| `POST` | `/api/analyze`          | NLP analysis of user answer           |
| `POST` | `/api/recommend`        | Final AI-based career recommendations |
| `GET`  | `/api/test`             | Health check                          |

---

## 🧠 NLP Engine (How It Works)

The custom NLP engine performs:

* 🔤 Tokenization
* 📝 Keyword extraction
* 😊 Sentiment scoring
* 🧩 Pattern matching
* 🎯 Weighted scoring system
* 📚 Final mapping to career paths

---

## 🐛 Troubleshooting

<details>
<summary>Frontend cannot reach backend</summary>

* Check `.env` file in frontend
* Ensure backend running at `5050`
* Enable CORS properly

</details>

<details>
<summary>Blank results page</summary>

* Make sure responses are returned correctly from NLP engine
* Validate payload shape (`answer`, `mode`, etc.)

</details>

---
