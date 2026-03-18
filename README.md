# 💰 Smart Expense Analyzer PRO

A full-stack fintech web application that analyzes expense CSV files and provides categorized insights, interactive charts, and ML-powered anomaly detection — built for production.

[![Backend](https://img.shields.io/badge/backend-Flask%203-blue?logo=python)](backend/)
[![Frontend](https://img.shields.io/badge/frontend-React%2018%20%2B%20Vite-61DAFB?logo=react)](frontend/)
[![ML](https://img.shields.io/badge/ml-Isolation%20Forest-orange?logo=scikit-learn)](backend/services/anomaly_detector.py)

---

## ✨ Features

| Feature | Details |
|---|---|
| 📤 CSV Upload | Drag-and-drop, flexible column detection, any bank format |
| 🗂 Auto-Categorization | 8 categories — Food, Transport, Shopping, Travel, and more |
| 📊 Visual Charts | Category donut pie + monthly bar chart (Recharts) |
| 📏 Breakdown Bars | Animated percentage bars per category |
| 🤖 Anomaly Detection | Isolation Forest ML — flags unusual transactions |
| 🔔 Alert System | Clear anomaly summary with count and percentage |
| 🔐 JWT Auth | Register, login, secure per-user data |
| 🗄 Persistent DB | SQLite (dev) / PostgreSQL (production-ready) |

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, React Router, Recharts, Axios |
| Backend | Flask 3, Flask-JWT-Extended, Flask-SQLAlchemy |
| Database | SQLite (dev) → PostgreSQL (prod) |
| ML | scikit-learn Isolation Forest |
| Deployment | Render (backend), Vercel (frontend) |

---

## 🚀 Running Locally

### Prerequisites
- Python 3.11+
- Node.js 18+

### Backend
```bash
cd backend

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate        # Windows
source venv/bin/activate       # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Start development server
python app.py
# → http://localhost:5000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# → http://localhost:5173
```

The frontend **Vite proxy** automatically forwards `/auth`, `/upload`, and `/transactions` calls to the Flask backend — no CORS config needed in development.

---

## 📁 Project Structure

```
Smart Expense Analyzer/
├── .gitignore
├── README.md
├── PROJECT_CONTEXT.md           # Living architecture document
│
├── backend/
│   ├── app.py                   # Flask app factory
│   ├── db.py                    # SQLAlchemy setup
│   ├── requirements.txt
│   ├── Procfile                 # Render/Heroku start command
│   ├── render.yaml              # Render deployment config
│   ├── runtime.txt              # Python version
│   ├── .env.example             # Required env vars
│   ├── sample_expenses.csv      # Test CSV file
│   ├── routes/
│   │   ├── auth.py              # /auth/register, /auth/login, /auth/me
│   │   └── upload.py            # POST /upload, GET /transactions
│   ├── models/
│   │   ├── user.py              # bcrypt-hashed passwords
│   │   └── transaction.py       # Expense with batch UUID
│   ├── services/
│   │   └── anomaly_detector.py  # Isolation Forest ML
│   └── utils/
│       ├── csv_parser.py        # Flexible column-alias parser
│       └── categorizer.py       # Rule-based 8-category engine
│
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js           # Dev proxy + build config
    ├── vercel.json              # Vercel SPA rewrites
    ├── .env.example             # VITE_API_URL
    └── src/
        ├── App.jsx              # Router + auth guards
        ├── main.jsx
        ├── index.css            # Design system
        ├── context/AuthContext.jsx
        ├── services/api.js      # Axios + JWT interceptors
        ├── components/
        │   ├── Navbar.jsx
        │   ├── StatCard.jsx
        │   ├── UploadZone.jsx
        │   ├── CategoryChart.jsx
        │   ├── MonthlyChart.jsx
        │   ├── AnomalyTable.jsx
        │   └── CategoryBreakdown.jsx
        └── pages/
            ├── Dashboard.jsx
            ├── Login.jsx
            └── Register.jsx
```

---

## 🌐 Deployment

### Backend → [Render](https://render.com)

1. Push the `backend/` folder to a GitHub repo
2. Create a new **Web Service** on Render
3. Set **Build Command**: `pip install -r requirements.txt`
4. Set **Start Command**: `gunicorn "app:create_app()" --bind 0.0.0.0:$PORT --workers 2`
5. Add environment variables:
   - `JWT_SECRET_KEY` → generate a long random string
   - `DATABASE_URL` → your PostgreSQL URL (optional, defaults to SQLite)
6. Deploy — your API is live at `https://your-service.onrender.com`

### Frontend → [Vercel](https://vercel.com)

1. Push the `frontend/` folder to GitHub
2. Import the project in Vercel
3. Set environment variable:
   - `VITE_API_URL` → your Render backend URL
4. Deploy — Vercel auto-detects Vite and runs `npm run build`

---

## 📋 API Reference

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/auth/register` | ❌ | Create account |
| `POST` | `/auth/login` | ❌ | Get JWT token |
| `GET` | `/auth/me` | ✅ JWT | Current user profile |
| `POST` | `/upload` | ✅ JWT | Upload CSV → full analysis |
| `GET` | `/transactions` | ✅ JWT | Fetch saved transactions |
| `GET` | `/health` | ❌ | Service health check |

### CSV Format
```csv
date,amount,description
2024-01-05,45.50,Starbucks coffee
2024-01-08,120.00,Amazon order
```
Supported column aliases: `date/transaction_date`, `amount/debit/value`, `description/merchant/narration`

---

## 🔒 Security Notes

- Passwords are hashed with **bcrypt** — never stored in plaintext
- JWT tokens expire after **12 hours**
- Login failure messages are deliberately vague to prevent user enumeration
- Set a strong `JWT_SECRET_KEY` in production — never commit `.env`

---

## 📄 License

MIT — free to use, modify, and deploy.
