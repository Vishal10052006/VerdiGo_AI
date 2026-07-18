# 🌱 VerdiGO AI

**Building the digital backbone for Indian farmers.**

VerdiGO AI is an agri-tech platform designed to give every farmer access to reliable information, personalized guidance, and — eventually — a 24/7 AI agronomist in their own language. This repo contains the backend and frontend for the core platform.

---

## 🚀 Vision

> A farmer opens VerdiGO and simply says: *"What should I do today?"*
> VerdiGO understands their farm, their crop, their weather, and their history — and responds like a trusted agricultural officer, in their own language.

VerdiGO AI's long-term goal is to become a **24×7 AI Agronomist**: a voice and chat assistant that interacts with farmers in their local language, asks intelligent follow-up questions, and analyzes crop images, weather, soil, and farming history to diagnose the real root cause of a problem — then delivers personalized, expert-level recommendations.

---

## ✅ What's Built (Phase 1 — Foundation MVP)

| Module | Status | Details |
|---|---|---|
| **Authentication** | ✅ Live | OTP-based login, JWT access/refresh tokens, logout, session refresh |
| **Farmer Registration** | ✅ Live | Farmer profile & farm information models, full CRUD APIs |
| **Farmer Profile** | ✅ Live | Get/update profile, profile image upload |
| **Dashboard** | ✅ Live | Aggregated farm + weather summary APIs |
| **Weather Advisory** | ✅ Live | Multi-provider weather intelligence (OpenMeteo + WeatherAPI) with automatic fallback, caching, and response normalization |
| **Crop Recommendation** | 🔜 In Progress | AI-driven recommendation engine |
| **AI Chat (Text)** | 🔜 In Progress | Conversational farming assistant |
| **Disease Detection (Image)** | 🔜 In Progress | Computer vision-based crop disease identification |

**Success criteria for Phase 1:** *A farmer can register and get basic advice.*

---

## 🗺️ Roadmap — 8 Phases to a Mature Platform

| Phase | Focus | Goal | Est. Duration |
|---|---|---|---|
| **1 — Foundation MVP** | Auth, Farmer Registration/Profile, Dashboard, Weather, Crop Recommendation, AI Chat, Disease Detection | Build the first usable product | 1–2 months |
| **2 — Voice Companion** | Hindi Speech-to-Text/Text-to-Speech, Voice Chat, Voice Disease/Crop/Weather queries | Farmers talk instead of type | 1 month |
| **3 — Smart Farming Advisor** | Fertilizer & Irrigation Recommendation, Pest Prediction, Crop Calendar, Task Reminders | Provide personalized, proactive recommendations | 2 months |
| **4 — Visual AI Agronomist** | Advanced Disease/Pest Detection, Video Upload Analysis, Soil Image Analysis, Treatment Recommendation | AI understands images and videos | 2 months |
| **5 — Memory & Personalization** | Farm/Crop/Soil/Disease History, Conversation Memory, Farmer Preferences | AI remembers each farmer | 1–2 months |
| **6 — Real-Time AI Companion** | Live Voice Conversation, Multi-turn Memory, Regional Language Support (Haryanvi, Punjabi) | Human-like, context-aware conversations | 2–3 months |
| **7 — Farm Business Platform** | Mandi Prices, Price Prediction, Marketplace, Government Schemes, Insurance Discovery | Increase farmer income | 3 months |
| **8 — AI Operating System for Agriculture** | Live Camera Companion, Satellite Intelligence (NDVI, Crop Monitoring), Predictive Yield/Risk Modeling, Multi-stakeholder Platform (Farmers, FPOs, Experts, Government, Agri Companies), 9+ Indian languages | Become the primary agricultural assistant, nationwide | 6+ months |

**Total estimated timeline:** ~18–24 months to a mature VerdiGO platform (2-person team pace).

---

## 🏗️ Tech Stack

**Backend:** Python, FastAPI, SQLAlchemy, PostgreSQL, Alembic (migrations), JWT Authentication
**Frontend:** Next.js, React, TypeScript, Tailwind CSS
**Weather Integration:** OpenMeteo API, WeatherAPI (multi-provider fallback + caching)
**Deployment:** Vercel, Railway, Render
**Planned AI Stack:** TensorFlow / PyTorch (Disease Detection CV model), LLM integration (AI Farming Assistant), Speech-to-Text/Text-to-Speech (Hindi + regional languages)

---

## 📌 Current Focus

Actively building out **Crop Recommendation**, **Disease Detection**, and the **AI Farming Assistant** — the remaining three modules of Phase 1 — before moving into Phase 2 (Voice Companion).

---

## 🤝 Team

Founded and built by [Vishal Raj](https://github.com/Vishal10052006). Actively looking to bring on a technical or product co-founder to accelerate the roadmap.

---

## 📄 License

TBD
