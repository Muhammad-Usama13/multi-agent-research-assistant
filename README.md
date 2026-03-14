# 🔬 Multi-Agent Research Assistant

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-0.3-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Gemini](https://img.shields.io/badge/Gemini_2.5_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)

**An intelligent Agentic AI system that automates research paper discovery, analysis, summarization, explanation, and critique — powered by 6 specialized AI agents collaborating through LangGraph.**

[Features](#-features) • [Architecture](#-architecture) • [Setup](#-setup) • [Usage](#-usage) • [API](#-api-endpoints)

</div>

---

## 🌟 What It Does

Instead of spending **hours** reading complex research papers, this system deploys **6 specialized AI agents** that work together in a pipeline — each agent handling a different task — and delivers a complete structured analysis in minutes.

| Without This Tool | With This Tool |
|---|---|
| Read 20+ page paper manually | Instant structured summary |
| Struggle with technical jargon | Plain-language explanation + glossary |
| Miss key contributions | Auto-extracted insights |
| No critical evaluation | AI critique with 1–10 rating |
| Hours of work | Minutes |

---

## ✨ Features

- 🔍 **ArXiv Search** — search any research topic, get real papers instantly
- 📄 **PDF Upload** — upload your own research paper for analysis
- 🤖 **6 AI Agents** — each specialized for a different task
- 📊 **5-Tab Results UI** — Summary, Analysis, Explanation, Critique, Full Report
- 📝 **Copyable Markdown Report** — export-ready research report
- ⚡ **Real-time Stage Tracking** — watch each agent work live

---

## 🏗️ Architecture

```
User Input (Topic Query  /  PDF Upload)
                │
                ▼
         FastAPI Backend
                │
                ▼
      ┌─── LangGraph Pipeline ────────────────────────────┐
      │                                                    │
      │  [Reader] → [Summarizer] → [Explainer]            │
      │              → [Critic] → [Report Generator]      │
      │                                                    │
      └────────────────────────────────────────────────────┘
                │
                ▼
        Structured JSON Response
                │
                ▼
       React Frontend (Dark UI)
```

### The 6 Agents

| Agent | Role |
|-------|------|
| 🔍 **Search Agent** | Finds relevant papers from ArXiv |
| 📖 **Reader Agent** | Extracts research question, methodology, results |
| 📝 **Summarization Agent** | Creates short summary, key contributions, findings |
| 💡 **Explanation Agent** | Simplifies concepts, builds glossary, gives analogy |
| 🔬 **Critic Agent** | Evaluates strengths, weaknesses, gives 1–10 rating |
| 📊 **Report Generator** | Compiles everything into a markdown report |

---

## 📁 Project Structure

```
research-assistant/
├── backend/
│   ├── main.py                     # FastAPI entry point
│   ├── requirements.txt
│   ├── .env.example
│   ├── agents/
│   │   ├── orchestrator.py         # LangGraph state machine
│   │   ├── reader_agent.py
│   │   ├── summarization_agent.py
│   │   ├── explanation_agent.py
│   │   ├── critic_agent.py
│   │   ├── report_generator.py
│   │   └── llm_helper.py           # Shared Gemini 2.5 Flash LLM
│   ├── modules/
│   │   ├── document_processor.py   # PDF parsing + section detection
│   │   └── search_module.py        # ArXiv search
│   └── routers/
│       ├── analysis.py
│       ├── upload.py
│       └── health.py
│
└── frontend/
    └── src/
        ├── App.jsx
        ├── styles.css
        ├── components/
        │   ├── Header.jsx
        │   ├── QueryInput.jsx
        │   ├── LoadingPanel.jsx
        │   ├── ResultsPanel.jsx
        │   ├── SearchResults.jsx
        │   └── AgentPipeline.jsx
        ├── hooks/useAnalysis.js
        └── utils/api.js
```

---

## ⚙️ Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- Google Gemini API key — get free at https://aistudio.google.com

### 1️⃣ Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your GOOGLE_API_KEY to .env

# Start server
uvicorn main:app --reload
```

API runs at http://localhost:8000 — interactive docs at /docs

### 2️⃣ Frontend

```bash
cd frontend
npm install
npm start
```

UI runs at http://localhost:3000

---

## 🚀 Usage

### Search by Topic
1. Type any research topic — "video anomaly detection", "transformer attention", etc.
2. Hit **Analyze** — the system fetches a real ArXiv paper and runs all agents

### Upload a PDF
1. Switch to the **Upload PDF** tab
2. Drag and drop your PDF or browse for it
3. Hit **Analyze PDF**

### Results Tabs

| Tab | What You Get |
|-----|-------------|
| **Summary** | 2–3 sentence overview, contributions, findings |
| **Analysis** | Research question, methodology, dataset, results |
| **Explanation** | Plain English explanation, glossary, real-world analogy |
| **Critique** | Strengths, weaknesses, limitations, 1–10 rating |
| **Full Report** | Complete copyable markdown report |

---

## 🔌 API Endpoints

```
GET  /api/health                    → Health check
POST /api/upload/pdf                → Upload PDF
POST /api/analysis/run              → Run full agent pipeline
GET  /api/analysis/search?q=topic   → Search ArXiv
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/analysis/run \
  -H "Content-Type: application/json" \
  -d '{"query": "attention is all you need transformer", "mode": "full"}'
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | Google Gemini 2.5 Flash |
| Agent Orchestration | LangGraph |
| LLM Framework | LangChain |
| Backend | FastAPI + Uvicorn |
| PDF Processing | pdfplumber |
| Paper Search | ArXiv API (free) |
| Frontend | React 18 |
| Styling | Custom CSS — dark theme |

---

## 🔮 Roadmap

- [ ] Multi-paper side-by-side comparison
- [ ] Automatic literature review generation
- [ ] Citation network graph visualization
- [ ] Export to PDF / Word
- [ ] Semantic Scholar + PubMed integration
- [ ] User accounts + analysis history
- [ ] Research trend detection

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

1. Fork the repo
2. Create your branch `git checkout -b feature/AmazingFeature`
3. Commit changes `git commit -m 'Add AmazingFeature'`
4. Push to branch `git push origin feature/AmazingFeature`
5. Open a Pull Request

---

## 📄 License

MIT License

---

<div align="center">
Built with ❤️ using LangGraph + Google Gemini + FastAPI + React
</div>
