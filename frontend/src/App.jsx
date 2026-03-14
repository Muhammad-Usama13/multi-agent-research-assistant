// src/App.jsx
import React from "react";
import { Toaster } from "react-hot-toast";

import Header        from "./components/Header";
import QueryInput    from "./components/QueryInput";
import LoadingPanel  from "./components/LoadingPanel";
import ResultsPanel  from "./components/ResultsPanel";
import AgentPipeline from "./components/AgentPipeline";
import { useAnalysis } from "./hooks/useAnalysis";

import "./styles.css";

export default function App() {
  const {
    loading, stage, results,
    analyzeByQuery, analyzeByPDF, clearResults,
  } = useAnalysis();

  return (
    <>
      <Toaster position="top-right" toastOptions={{ duration: 3500 }} />
      <div className="app">
        <Header />

        <main className="main">
          {/* Hero */}
          {!results && !loading && (
            <div className="hero">
              <div className="hero-badge">AI-Powered · Multi-Agent</div>
              <h2 className="hero-title">
                Understand Research Papers<br />
                <span className="accent">in Minutes, Not Hours</span>
              </h2>
              <p className="hero-sub">
                Enter a research topic or upload a PDF. Six specialized AI agents will
                analyze, summarize, explain, and critique it for you.
              </p>
            </div>
          )}

          {/* Input always visible when not showing results */}
          {!results && (
            <QueryInput
              onQuery={analyzeByQuery}
              onPDF={analyzeByPDF}
              loading={loading}
            />
          )}

          {/* Loading */}
          {loading && <LoadingPanel stage={stage} />}

          {/* Results */}
          {results && !loading && (
            <ResultsPanel results={results} onClear={clearResults} />
          )}

          {/* Pipeline explainer (only on home) */}
          {!results && !loading && <AgentPipeline />}
        </main>

        <footer className="footer">
          <p>Multi-Agent Research Assistant · Built with LangGraph + Google Gemini + FastAPI</p>
        </footer>
      </div>
    </>
  );
}
