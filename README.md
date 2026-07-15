# 🌱 VerdiGo AI

> AI-powered Smart Agriculture Platform for Indian Farmers

VerdiGo AI is an intelligent agriculture platform designed to help farmers make data-driven decisions through AI, weather intelligence, farm management, and future crop recommendation systems.

This project is being built as a complete production-ready SaaS platform using modern web technologies.

---

## 🚀 Features

### ✅ Authentication
- Secure JWT Authentication
- Farmer Registration
- Login & Logout
- Protected Routes

### 🌾 Farm Management
- Register Farms
- Manage Farm Details
- Farm Dashboard
- Soil Information
- Farm Area Tracking

### 📊 Smart Dashboard
- Personalized Welcome Section
- Animated Statistics
- Live Weather Widget
- Farm Summary Card
- Quick Actions
- Recent Activity Timeline
- Skeleton Loading States
- Responsive Design

### 🌦 Weather Intelligence
- Live Weather API Integration
- Temperature
- Humidity
- Wind Speed
- Rainfall
- Weather Condition

### 🤖 Upcoming AI Modules
- Crop Recommendation
- Disease Detection
- Fertilizer Recommendation
- AI Chat Assistant
- Yield Prediction
- Farm Analytics

---

# 🛠 Tech Stack

## Frontend

- Next.js 16
- React
- TypeScript
- Tailwind CSS v4
- ShadCN UI
- Lucide Icons

## Backend

- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- JWT Authentication

---

# 📂 Project Structure

```
VerdiGo_AI
│
├── backend
│   ├── app
│   ├── alembic
│   ├── uploads
│   └── requirements.txt
│
├── frontend
│   ├── src
│   ├── public
│   ├── package.json
│   └── next.config.ts
│
└── README.md
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/Vishal10052006/VerdiGo_AI.git
```

---

## 2. Backend

```bash
cd backend

python -m venv .venv

source .venv/bin/activate
```

Install packages

```bash
pip install -r requirements.txt
```

Run server

```bash
uvicorn app.main:app --reload
```

Backend

```
http://127.0.0.1:8000
```

---

## 3. Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend

```
http://localhost:3000
```

---

# 🌐 Environment Variables

Frontend

```
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

Backend

Create a `.env` file.

Example

```
DATABASE_URL=
SECRET_KEY=
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

---

# 📌 Current Development Status

## ✅ Phase 1

- Module 1 – Backend Foundation
- Module 2 – Farmer Registration
- Module 3 – Authentication
- Module 4 – Landing Website
- Module 5 – Dashboard Architecture
- Module 6 – User Dashboard

---

# 🚀 Future Roadmap

- AI Crop Recommendation
- Disease Detection
- Fertilizer Recommendation
- Satellite Integration
- AI Chat Assistant
- IoT Device Support
- Mobile Application
- Government Scheme Integration

---

# 👨‍💻 Developer

**Founder**

**Vishal Singh**

Building AI for Agriculture 🌱

---

# 📄 License

This project is currently under development.

All Rights Reserved © VerdiGo AI
