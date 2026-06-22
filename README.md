# SENTINEL - AI-Powered Industrial Safety Intelligence

![SENTINEL Logo](https://img.shields.io/badge/Status-Active-brightgreen) ![License](https://img.shields.io/badge/License-MIT-blue)

**SENTINEL** is an intelligent, multi-agent safety command centre designed to predict, detect, and autonomously respond to industrial hazards. Built for the **ET Gen AI Hackathon 2026**, this project aligns with **Problem Statement #1: AI-Powered Industrial Safety Intelligence for Zero-Harm Operations**.

---

## 📖 Table of Contents
1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Architecture & Tech Stack](#architecture--tech-stack)
4. [The Compound Risk Score (CRS)](#the-compound-risk-score-crs)
5. [Prerequisites](#prerequisites)
6. [Installation & Setup](#installation--setup)
7. [Running the Application](#running-the-application)
8. [Demo Simulation Workflow](#demo-simulation-workflow)

---

## 🌍 Project Overview
Heavy industrial sectors rely on reactive safety systems (e.g., a gas alarm sounds *after* a leak reaches a critical limit). SENTINEL transforms this paradigm by using AI to analyze contextual overlaps. It tracks workers, environmental sensors, and active work permits simultaneously to predict accidents before they occur.

If a worker is performing *Hot Work* (welding) in Zone 1, and an adjacent sensor detects a mild *Flammable Gas* anomaly, SENTINEL's Compound Risk Score will spike, triggering automated emergency protocols.

---

## ✨ Key Features
*   **Multi-Agent AI Pipeline:** A team of 6 specialized LangGraph agents (Watcher, Auditor, Analyst, Oracle, Scribe, Guardian) working in milliseconds.
*   **Real-Time Data Streaming:** Uses Server-Sent Events (SSE) to push live risk metrics and AI decisions from the backend to the UI with zero latency.
*   **Compound Risk Scoring (CRS):** A proprietary algorithm that weights base hazards, cascading environmental factors, and regulatory compliance to calculate true risk.
*   **Geospatial Plant Heatmap:** A live SVG map tracking workers, active permits, and hazardous zones in real-time.
*   **Automated Emergency Protocols:** The Guardian Agent can autonomously issue evacuation orders and shutdown commands if the CRS exceeds critical thresholds.

---

## 🏗 Architecture & Tech Stack

### Frontend (`sentinel-frontend`)
*   **Framework:** Next.js 15 (React)
*   **Styling:** Pure Vanilla CSS (Dark Mode, Neon Design System, Glassmorphism)
*   **Data Fetching:** Native `EventSource` for Server-Sent Events (SSE) streaming.

### Backend (`sentinel-backend`)
*   **Framework:** FastAPI (Python)
*   **AI Orchestration:** LangGraph & Langchain
*   **LLM Provider:** Google Gemini 2.0 (via `google-generativeai`)
*   **Database:** Async SQLite (`aiosqlite`)
*   **Real-time Protocol:** `sse-starlette`

---

## 🧮 The Compound Risk Score (CRS)
The CRS is the heart of the predictive engine. It is calculated as follows:
1.  **Base Score:** Extracted from raw IoT sensor data (e.g., Gas, Temp, Pressure).
2.  **Cascade Multiplier:** Applied if contextual factors overlap (e.g., Hot Work Permit + Flammable Gas).
3.  **Regulatory Penalty:** Applied if workers lack required certifications for their current task.

**Formula:** `CRS = (Base_Hazard) * (1 + Cascade_Multiplier) * (Regulatory_Penalty)`
*Scale: 0.00 to 1.00 (Normal < 0.3 | Medium < 0.6 | High < 0.85 | Critical >= 0.85)*

---

## 🛠 Prerequisites
Before you begin, ensure you have the following installed:
*   **Node.js** (v18.0.0 or higher)
*   **Python** (v3.10 or higher)
*   **Git**

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-org/sentinel.git
cd SENTINEL
```

### 2. Backend Setup
```bash
cd sentinel-backend
python -m venv venv

# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```
*Note: Ensure you create a `.env` file in the `sentinel-backend` directory and add your `GEMINI_API_KEY=your_key_here`.*

### 3. Frontend Setup
```bash
cd ../sentinel-frontend
npm install --legacy-peer-deps
```

---

## ⚡ Running the Application

You need to run both the Backend and Frontend servers concurrently.

### Terminal 1: Backend Server
```bash
cd sentinel-backend
.\venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

### Terminal 2: Frontend Server
```bash
cd sentinel-frontend
npm run dev
```

Once both are running, open your browser and navigate to: **[http://localhost:3000](http://localhost:3000)**

---

## 🎯 Demo Simulation Workflow
To test the core capabilities of SENTINEL during a pitch or demonstration:

1.  Load the dashboard at `http://localhost:3000`. Observe the initial "Normal" state.
2.  Click the **"INITIATE CRS SIMULATION"** button in the top right corner.
3.  Watch the **LangGraph Agent Pipeline** section on the left. You will see the Watcher, Auditor, Analyst, Oracle, Scribe, and Guardian agents execute sequentially.
4.  Observe the **Compound Risk Score** spike to Critical (>0.85).
5.  Watch the **Geospatial Plant Heatmap**. "Zone 1" (Coke Oven Battery) will turn red, indicating an active hazard.
6.  Look at the **Emergency Panel** (bottom right). The Guardian Agent will issue a live evacuation order.

---
*Built with ❤️ for ET Gen AI Hackathon 2026*
