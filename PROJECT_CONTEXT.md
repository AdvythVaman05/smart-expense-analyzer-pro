# 🧠 PROJECT CONTEXT: Smart Expense Analyzer PRO

## 📌 Objective

Build a production-quality fintech-style web application that analyzes user expenses from CSV uploads and provides insights, anomaly detection, and visual dashboards.

---

## 🏗️ Architecture

* Frontend: React (Vite) — ✅ Running at http://localhost:5173
* Backend: Flask API — ✅ Running at http://localhost:5000
* Database: SQLite — ✅ Auto-created at `backend/expense_analyzer.db`
* ML: Isolation Forest — ✅ Anomaly detection working
* Charts: Recharts (Pie + Bar) — ✅ Rendering correctly

---

## 🔑 Feature Status

| Feature | Status |
|---|---|
| CSV Upload (drag-and-drop) | ✅ Done |
| Expense Categorization (8 categories) | ✅ Done |
| Monthly & Category Charts | ✅ Done |
| ML Anomaly Detection (Isolation Forest) | ✅ Done |
| Alert Banner | ✅ Done |
| JWT Authentication (register/login) | ✅ Done |
| Persistent Storage (SQLite) | ✅ Done |
| Glassmorphism Dashboard UI | ✅ Done |
| Deployment | 🔲 Phase 5 |

---

## 📁 Project Structure

```
Smart Expense Analyzer/
├── PROJECT_CONTEXT.md
├── backend/
│   ├── app.py                 # Flask factory
│   ├── db.py                  # SQLAlchemy
│   ├── requirements.txt
│   ├── expense_analyzer.db    # SQLite DB
│   ├── sample_expenses.csv    # Test data
│   ├── routes/
│   │   ├── auth.py            # POST /auth/register, /login, GET /me
│   │   └── upload.py          # POST /upload, GET /transactions
│   ├── models/
│   │   ├── user.py            # bcrypt hashed passwords
│   │   └── transaction.py     # batch UUID tracking
│   ├── services/
│   │   └── anomaly_detector.py # Isolation Forest
│   └── utils/
│       ├── csv_parser.py       # Flexible column alias parser
│       └── categorizer.py      # 8-category rule engine
└── frontend/
    ├── package.json
    ├── index.html
    ├── vite.config.js          # Proxies API to Flask
    └── src/
        ├── main.jsx
        ├── App.jsx             # Routes + Auth guards
        ├── index.css           # Full design system
        ├── context/AuthContext.jsx
        ├── services/api.js     # Axios + JWT interceptors
        ├── components/
        │   ├── Navbar.jsx/css
        │   ├── StatCard.jsx/css
        │   ├── UploadZone.jsx/css
        │   ├── AnomalyTable.jsx/css
        │   ├── CategoryChart.jsx
        │   └── MonthlyChart.jsx
        └── pages/
            ├── Dashboard.jsx/css
            ├── Login.jsx
            ├── Register.jsx
            └── Auth.css
```

---

## 🔌 API Summary

| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| POST | /auth/register | None | Create account |
| POST | /auth/login | None | Get JWT |
| GET | /auth/me | JWT | My profile |
| POST | /upload | JWT | Upload CSV, get analysis |
| GET | /transactions | JWT | Fetch saved transactions |

---

## 🧠 Current Progress

- ✅ Phase 1: Backend core (Flask, CSV parser, categorizer, ML)
- ✅ Phase 2: Database + Auth (SQLite, User model, JWT)
- ✅ Phase 3: React frontend (Dashboard, charts, upload, auth pages)
- ✅ E2E verified: register → login → upload → dashboard renders correctly

---

## 📝 Next Tasks (Optional)

- Phase 4: UI polish (if needed — already well-designed)
- Phase 5: Deployment — Backend → Render, Frontend → Vercel
