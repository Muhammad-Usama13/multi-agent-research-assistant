// src/components/ResultsPanel.jsx
import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import {
  BookOpen, Brain, Lightbulb, MessageSquare,
  FileText, ChevronDown, ChevronUp, Star, X
} from "lucide-react";

const TABS = [
  { id: "summary",     label: "Summary",     icon: BookOpen },
  { id: "reader",      label: "Analysis",    icon: Brain },
  { id: "explanation", label: "Explanation", icon: Lightbulb },
  { id: "critique",    label: "Critique",    icon: MessageSquare },
  { id: "report",      label: "Full Report", icon: FileText },
];

// ── Small reusable pieces ──────────────────────────────────────────────────────
const TagList = ({ items = [] }) => (
  <div className="tag-list">
    {items.map((t, i) => <span key={i} className="tag">{t}</span>)}
  </div>
);

const BulletList = ({ items = [], color = "accent" }) => (
  <ul className="bullet-list">
    {items.map((item, i) => (
      <li key={i} className={`bullet-item ${color}`}>{item}</li>
    ))}
  </ul>
);

const RatingBar = ({ value = 0 }) => (
  <div className="rating-row">
    <span className="rating-label">Overall Rating</span>
    <div className="rating-bar-wrap">
      <div className="rating-bar" style={{ width: `${value * 10}%` }} />
    </div>
    <span className="rating-num">{value}/10</span>
    {[...Array(10)].map((_, i) => (
      <Star
        key={i}
        size={13}
        className={i < value ? "star filled" : "star empty"}
      />
    ))}
  </div>
);

// ── Tab panes ─────────────────────────────────────────────────────────────────
function SummaryPane({ data }) {
  return (
    <div className="pane">
      <div className="pane-section highlight-box">
        <h4>Overview</h4>
        <p>{data.short_summary}</p>
      </div>
      <div className="two-col">
        <div className="pane-section">
          <h4>Key Contributions</h4>
          <BulletList items={data.key_contributions} color="green" />
        </div>
        <div className="pane-section">
          <h4>Major Findings</h4>
          <BulletList items={data.major_findings} color="blue" />
        </div>
      </div>
      <div className="pane-section">
        <h4>Practical Implications</h4>
        <p>{data.practical_implications}</p>
      </div>
      <div className="pane-section">
        <h4>Target Audience</h4>
        <p className="muted">{data.target_audience}</p>
      </div>
    </div>
  );
}

function ReaderPane({ data }) {
  return (
    <div className="pane">
      <div className="pane-section highlight-box">
        <h4>Research Question</h4>
        <p>{data.research_question}</p>
      </div>
      <div className="pane-section">
        <h4>Methodology</h4>
        <p>{data.methodology}</p>
      </div>
      <div className="two-col">
        <div className="pane-section">
          <h4>Dataset / Experiment</h4>
          <p>{data.dataset}</p>
        </div>
        <div className="pane-section">
          <h4>Results</h4>
          <p>{data.results}</p>
        </div>
      </div>
      <div className="pane-section">
        <h4>Contributions</h4>
        <BulletList items={data.contributions} color="green" />
      </div>
      <div className="pane-section">
        <h4>Keywords</h4>
        <TagList items={data.keywords} />
      </div>
    </div>
  );
}

function ExplanationPane({ data }) {
  return (
    <div className="pane">
      <div className="pane-section highlight-box analogy">
        <h4>Simple Explanation</h4>
        <p>{data.simple_explanation}</p>
      </div>
      <div className="pane-section">
        <h4>Methodology in Plain Language</h4>
        <p>{data.methodology_explained}</p>
      </div>
      {data.analogy && (
        <div className="pane-section analogy-box">
          <h4>💡 Real-World Analogy</h4>
          <p>{data.analogy}</p>
        </div>
      )}
      <div className="pane-section">
        <h4>Technical Terms Glossary</h4>
        <div className="glossary">
          {(data.technical_terms || []).map((t, i) => (
            <div key={i} className="glossary-item">
              <span className="term">{t.term}</span>
              <span className="definition">{t.definition}</span>
            </div>
          ))}
        </div>
      </div>
      <div className="pane-section">
        <h4>Why It Matters</h4>
        <p>{data.why_it_matters}</p>
      </div>
    </div>
  );
}

function CritiquePane({ data }) {
  return (
    <div className="pane">
      <RatingBar value={data.overall_rating || 0} />
      <div className="two-col">
        <div className="pane-section">
          <h4 className="green-head">✅ Strengths</h4>
          <BulletList items={data.strengths} color="green" />
        </div>
        <div className="pane-section">
          <h4 className="red-head">⚠️ Weaknesses</h4>
          <BulletList items={data.weaknesses} color="red" />
        </div>
      </div>
      <div className="pane-section">
        <h4>Limitations</h4>
        <BulletList items={data.limitations} color="orange" />
      </div>
      <div className="pane-section">
        <h4>Potential Improvements</h4>
        <BulletList items={data.potential_improvements} color="blue" />
      </div>
      <div className="two-col">
        <div className="pane-section">
          <h4>Novelty Assessment</h4>
          <p>{data.novelty_assessment}</p>
        </div>
        <div className="pane-section">
          <h4>Reproducibility</h4>
          <p>{data.reproducibility}</p>
        </div>
      </div>
    </div>
  );
}

function ReportPane({ report }) {
  const [copied, setCopied] = useState(false);
  const copy = () => {
    navigator.clipboard.writeText(report);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  return (
    <div className="pane">
      <div className="report-toolbar">
        <span className="muted">Full markdown report generated by all agents</span>
        <button className="btn-copy" onClick={copy}>
          {copied ? "✓ Copied!" : "Copy Markdown"}
        </button>
      </div>
      <div className="markdown-body">
        <ReactMarkdown>{report}</ReactMarkdown>
      </div>
    </div>
  );
}

// ── Main component ─────────────────────────────────────────────────────────────
export default function ResultsPanel({ results, onClear }) {
  const [activeTab, setActiveTab] = useState("summary");

  const renderPane = () => {
    switch (activeTab) {
      case "summary":     return <SummaryPane     data={results.summary} />;
      case "reader":      return <ReaderPane       data={results.reader_analysis} />;
      case "explanation": return <ExplanationPane  data={results.explanation} />;
      case "critique":    return <CritiquePane     data={results.critique} />;
      case "report":      return <ReportPane       report={results.report} />;
      default:            return null;
    }
  };

  return (
    <div className="results-panel">
      {/* Header */}
      <div className="results-header">
        <div>
          <h2 className="results-title">Research Analysis</h2>
          <p className="results-query">"{results.query}"</p>
        </div>
        <button className="btn-clear" onClick={onClear}>
          <X size={14} /> New Analysis
        </button>
      </div>

      {/* Tab bar */}
      <div className="result-tabs">
        {TABS.map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            className={`result-tab ${activeTab === id ? "active" : ""}`}
            onClick={() => setActiveTab(id)}
          >
            <Icon size={15} /> {label}
          </button>
        ))}
      </div>

      {/* Pane */}
      <div className="pane-container">{renderPane()}</div>
    </div>
  );
}
