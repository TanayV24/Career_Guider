<div align="center">

# 🎯 Career Guider

### AI-Powered Career Counseling Platform for Indian Students

[![React](https://img.shields.io/badge/React-18.2.0-61DAFB?style=for-the-badge&logo=react&logoColor=white)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**A modern web application that helps SSC and HSC students discover their perfect career path through interactive questionnaires and real-time NLP sentiment analysis.**

[🚀 Live Demo](#) | [📖 Documentation](#features) | [🐛 Report Bug](https://github.com/Tanayv24/career-guider/issues) | [💡 Request Feature](https://github.com/Tanayv24/career-guider/issues)

</div>

---

## ✨ Features

### 🎓 **For Students**
- 📝 **Interactive Questionnaire** - Engaging questions tailored for SSC/HSC students
- 🤖 **AI-Powered Analysis** - Real-time sentiment analysis using custom NLP engine
- 💡 **Personalized Recommendations** - Career suggestions based on responses
- 📊 **Progress Tracking** - Visual progress indicators and score tracking
- 🎨 **Beautiful UI** - Modern, responsive design that works on all devices

### 🔧 **Technical Features**
- ⚡ **Fast & Responsive** - Built with React for smooth user experience
- 🔐 **Session Management** - Secure user session handling
- 📡 **RESTful API** - Clean Flask backend architecture
- 🧠 **Custom NLP Engine** - Sentiment analysis and keyword extraction
- 🌐 **Cross-Platform** - Works on desktop, tablet, and mobile

---

## 🛠️ Tech Stack

<table>
<tr>
<td width="50%" valign="top">

### Frontend
- **Framework:** React 18.2.0
- **Routing:** React Router DOM 6.x
- **HTTP Client:** Axios
- **Styling:** Custom CSS3
- **State Management:** React Hooks

</td>
<td width="50%" valign="top">

### Backend
- **Framework:** Flask 3.0.0
- **CORS:** Flask-CORS 4.0.0
- **NLP:** Custom sentiment analysis engine
- **Data Processing:** Python 3.8+
- **API Architecture:** RESTful design

</td>
</tr>
</table>

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

| Tool | Version | Download Link |
|------|---------|---------------|
| 🐍 Python | 3.8 or higher | [Download Python](https://www.python.org/downloads/) |
| 📦 Node.js | 14.0 or higher | [Download Node.js](https://nodejs.org/) |
| 📝 npm | 6.0 or higher | Comes with Node.js |
| 💻 Git | Latest | [Download Git](https://git-scm.com/) (optional) |

**Verify installations:**

python --version # Should show 3.8+
node --version # Should show 14.0+
npm --version # Should show 6.0+


---

## ⚙️ Installation & Setup

### 🚀 Quick Start (5 Minutes)

1. Clone the repository
git clone https://github.com/Tanayv24/career-guider.git
cd career-guider

2. Setup Backend
cd backend
pip install -r requirements.txt
python run.py

3. Setup Frontend (in a new terminal)
cd frontend
npm install
npm start


### 📖 Detailed Instructions

<details>
<summary>Click to expand detailed setup instructions</summary>

#### Step 1: Clone/Download the Project

**Option A: Using Git**

git clone https://github.com/Tanayv24/career-guider.git
cd career-guider


**Option B: Download ZIP**
1. Click the green "Code" button above
2. Select "Download ZIP"
3. Extract the ZIP file
4. Open terminal in the extracted folder

#### Step 2: Backend Setup

Navigate to backend directory
cd backend

Install Python dependencies
pip install -r requirements.txt

Start the Flask server
python run.py


✅ Backend will start at: `http://localhost:5050`

You should see:

Running on http://127.0.0.1:5050

Running on http://192.168.X.X:5050


#### Step 3: Frontend Setup

Open a **NEW terminal window** and run:

Navigate to frontend directory
cd frontend

Install Node.js dependencies (first time only, takes 2-3 minutes)
npm install

Start the React development server
npm start

✅ Frontend will automatically open at: `http://localhost:3001`

You should see:
Compiled successfully!
Local: http://localhost:3001
On Your Network: http://192.168.X.X:3001

</details>

---

## 🎮 How to Use

1. **Start Both Servers** (backend on port 5050, frontend on port 3001)
2. **Open Browser** to `http://localhost:3001`
3. **Login** with your name and email
4. **Select Your Path** - Choose SSC or HSC
5. **Answer Questions** - NLP analyzes each response in real-time
6. **View Results** - Get personalized career recommendations!

---

## 📁 Project Structure

career-guider/
│
├── backend/ # Flask Backend
│ ├── app/
│ │ ├── init.py # Flask app initialization
│ │ ├── routes/
│ │ │ └── api.py # API endpoints
│ │ └── services/
│ │ ├── nlp_engine.py # Sentiment analysis engine
│ │ ├── question_bank.py # Question database
│ │ └── stream_analyzer.py # Career analyzer
│ ├── requirements.txt # Python dependencies
│ └── run.py # Backend entry point
│
├── frontend/ # React Frontend
│ ├── public/
│ │ ├── index.html
│ │ └── favicon.ico
│ ├── src/
│ │ ├── pages/ # Page components
│ │ │ ├── LoginPage.jsx
│ │ │ ├── ModeSelection.jsx
│ │ │ ├── MotivationalQuote.jsx
│ │ │ ├── QuestionPage.jsx
│ │ │ └── ResultsPage.jsx
│ │ ├── services/
│ │ │ └── api.js # API service layer
│ │ ├── App.jsx # Main app component
│ │ └── App.css # Global styles
│ ├── package.json # Node.js dependencies
│ └── .env # Environment variables
│
├── screenshots/ # Project screenshots
├── .gitignore # Git ignore rules
└── README.md # This file

---

## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/login` | User login/registration |
| `GET` | `/api/questions/<mode>` | Get questions (ssc/hsc) |
| `POST` | `/api/analyze` | Analyze answer with NLP |
| `POST` | `/api/submit-answer` | Submit user answer |
| `POST` | `/api/recommend` | Get career recommendations |
| `GET` | `/api/test` | Health check endpoint |

### Example API Call

// Analyze user answer
const response = await axios.post('http://localhost:5050/api/analyze', {
answer: "I love coding and building apps"
});

// Response:
{
sentiment: 0.75,
keywords: ["love", "coding", "building", "apps"],
confidence: 0.75
}

---

## 🧠 NLP Engine

Our custom NLP engine performs:

- **✅ Sentiment Analysis** - Measures positivity/negativity of responses
- **✅ Keyword Extraction** - Identifies important terms
- **✅ Confidence Scoring** - Calculates response certainty
- **✅ Pattern Recognition** - Detects interests and strengths

### Example Analysis

**Input:** "I really enjoy mathematics and solving complex problems"

**Output:**
{
"sentiment": 0.8,
"keywords": ["enjoy", "mathematics", "solving", "complex", "problems"],
"confidence": 0.8
}

---

## 🐛 Troubleshooting

<details>
<summary>Backend won't start</summary>

**Problem:** `ModuleNotFoundError` or import errors

**Solution:**
cd backend
pip install -r requirements.txt --upgrade
python run.py

**Check:** Make sure Python 3.8+ is installed: `python --version`
</details>

<details>
<summary>Frontend won't start</summary>

**Problem:** `'react-scripts' is not recognized`

**Solution:**
cd frontend
rm -rf node_modules
npm install
npm start

**Check:** Make sure Node.js is installed: `node --version`
</details>

<details>
<summary>Port already in use</summary>

**Problem:** `Port 5050 already in use` or `Port 3001 already in use`

**Solution (Windows):**
Find and kill process on port 5050
netstat -ano | findstr :5050
taskkill /PID <PID> /F

Find and kill process on port 3001
netstat -ano | findstr :3001
taskkill /PID <PID> /F

**Solution (Mac/Linux):**
Kill process on port 5050
lsof -ti:5050 | xargs kill -9

Kill process on port 3001
lsof -ti:3001 | xargs kill -9

</details>

<details>
<summary>Network Error / CORS Error</summary>

**Problem:** Frontend can't connect to backend

**Solution:**
1. Check backend is running on port 5050
2. Verify `.env` file in frontend:
REACT_APP_API_URL=http://localhost:5050/api

3. Restart both servers
4. Clear browser cache (Ctrl+Shift+Delete)
</details>

<details>
<summary>Page redirects to wrong route</summary>

**Problem:** Goes to mode-selection instead of login

**Solution:**
Clear browser localStorage:
1. Press F12 (DevTools)
2. Go to Application → Local Storage
3. Delete all entries
4. Refresh page
</details>

---

## 🚀 Future Enhancements

- [ ] 📱 Mobile app version (React Native)
- [ ] 🔐 User authentication with JWT
- [ ] 💾 Database integration (PostgreSQL)
- [ ] 📊 Advanced analytics dashboard
- [ ] 🌍 Multi-language support
- [ ] 📧 Email notifications
- [ ] 🎓 College/course recommendations
- [ ] 📈 Career path visualization
- [ ] 🤝 Mentor matching system
- [ ] 💬 Chat support integration

---