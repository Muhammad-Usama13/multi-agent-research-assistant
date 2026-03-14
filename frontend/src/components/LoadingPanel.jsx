// src/components/LoadingPanel.jsx
import React from "react";
import { Loader2 } from "lucide-react";

const ALL_STAGES = [
  "📄 Processing document...",
  "🔍 Reader Agent analyzing...",
  "📝 Summarization Agent working...",
  "💡 Explanation Agent simplifying...",
  "🔬 Critic Agent evaluating...",
  "📊 Generating final report...",
];

export default function LoadingPanel({ stage }) {
  const currentIndex = ALL_STAGES.indexOf(stage);

  return (
    <div className="loading-panel">
      <div className="loading-header">
        <Loader2 size={24} className="spin" />
        <h3>Agents Working…</h3>
      </div>

      <div className="stage-list">
        {ALL_STAGES.map((s, i) => {
          const done    = i < currentIndex;
          const active  = i === currentIndex;
          const pending = i > currentIndex;
          return (
            <div
              key={s}
              className={`stage-item ${done ? "done" : ""} ${active ? "active" : ""} ${pending ? "pending" : ""}`}
            >
              <div className="stage-dot">
                {done ? "✓" : active ? <Loader2 size={12} className="spin" /> : "○"}
              </div>
              <span>{s}</span>
            </div>
          );
        })}
      </div>

      <p className="loading-note">
        Multiple AI agents are collaborating on your research…
      </p>
    </div>
  );
}
