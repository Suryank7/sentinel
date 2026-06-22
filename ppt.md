---
title: "SENTINEL: AI-Powered Industrial Safety Intelligence"
subtitle: "ET Gen AI Hackathon 2026 - Problem Statement #1"
author: "Team [Your Team Name]"
theme: "Dark / Neon Green"
---

# Slide 1: Title Slide
**SENTINEL**
AI-Powered Industrial Safety Intelligence for Zero-Harm Operations
*Transforming reactive safety into proactive prevention using Multi-Agent AI.*

**Track:** PS 1 (Industrial Intelligence / Worker Safety / Geospatial Safety Analytics)
**Team:** [Your Team Name]

---

# Slide 2: The Problem - The Cost of Reactive Safety
Heavy industrial sectors face devastating human and financial costs due to outdated safety protocols.

*   **The Statistic:** Over 6,500 fatal workplace accidents recorded in FY2023 (DGFASLI).
*   **The Flaw:** Current systems are **siloed and reactive**. Gas sensors, permit systems, and worker tracking do not talk to each other.
*   **The Result:** A worker might be performing hot work (welding) near a slow, undetected flammable gas leak. The alarm only sounds *after* the explosion.

---

# Slide 3: The Solution - Meet SENTINEL
**SENTINEL** is a real-time, AI-driven Command Centre that connects the dots before disaster strikes.

Instead of waiting for a single sensor to breach a critical limit, SENTINEL uses a multi-agent AI pipeline to continuously analyze compounding risks across the entire plant.

**Core Mission:** Achieve Zero-Harm Operations through predictive intelligence.

---

# Slide 4: How It Works (The CRS Engine)
At the heart of SENTINEL is the **Compound Risk Score (CRS)**.

The CRS doesn't just look at one metric; it evaluates contextual overlap:
1.  **Proximity Hazard:** Are workers near a high-risk zone?
2.  **Cascade Hazard:** Is there a *Hot Work* permit active near a *Flammable Gas* (H₂S) anomaly?
3.  **Regulatory Penalty:** Are safety compliances being violated in real-time?

*Formula: Base Risk × (1 + Cascade Multiplier) × Regulatory Penalty*

---

# Slide 5: The LangGraph Multi-Agent Pipeline
We didn't just build an app; we built a team of specialized AI agents working in milliseconds.

1.  **Watcher Agent:** Monitors raw IoT streams (Temperature, Gas, Pressure).
2.  **Auditor Agent:** Cross-references active Work Permits and regulatory compliance.
3.  **Analyst Agent:** Calculates the live Compound Risk Score.
4.  **Oracle Agent:** Projects future risk using predictive logic.
5.  **Guardian Agent:** The enforcer. Automatically triggers **Emergency Protocols** and shuts down machinery if CRS > 0.85.

---

# Slide 6: Key Features & The Command Centre
**The SENTINEL Dashboard (Live Demo):**
*   **Geospatial Plant Heatmap:** Live SVG tracking of zones (Coke Oven, Blast Furnace) turning from green to red as risks compound.
*   **Live Event Streaming:** Server-Sent Events (SSE) push agent decisions to the UI instantly—no refreshing required.
*   **Automated Emergency Protocols:** Automated evacuation orders and machinery shutdown commands issued the second thresholds are breached.

---

# Slide 7: The Technology Stack
Built for speed, scalability, and extreme reliability.

*   **Frontend:** Next.js 15, React, Custom CSS (Dark Mode/Neon Design System)
*   **Backend:** FastAPI (Python), Server-Sent Events (SSE) for sub-second latency
*   **AI Orchestration:** LangGraph (Stateful Multi-Agent System)
*   **LLM Engine:** Google Gemini 2.0 (for complex scenario reasoning)
*   **Database:** Async SQLite (easily swappable to PostgreSQL)

---

# Slide 8: Business Impact & ROI
Safety isn't just a moral imperative; it's a financial necessity.

*   **Eliminate Fatalities:** Achieve the ultimate goal of Zero-Harm operations.
*   **Reduce Downtime:** Prevent catastrophic failures that halt production for weeks.
*   **Regulatory Compliance:** Automated auditing avoids heavy fines and legal liabilities.
*   **Insurance Premiums:** Verifiable, proactive safety systems drastically lower insurance costs.

---

# Slide 9: Future Roadmap
Where we take SENTINEL next:

1.  **Computer Vision Integration:** Hooking CCTV feeds into a new 'Vision Agent' to detect PPE compliance (Hardhat/Vest detection).
2.  **Wearable Tech Sync:** Biometric monitoring (heart rate, heat stress) for workers in extreme environments.
3.  **Drone Dispatch:** Automated drone deployment to inspect hazardous zones before humans enter.

---

# Slide 10: Thank You
**SENTINEL: Because every worker deserves to go home safe.**

*Questions & Demo*
