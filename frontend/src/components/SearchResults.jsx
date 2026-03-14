// src/components/SearchResults.jsx
import React from "react";
import { ExternalLink, User, Calendar, Tag } from "lucide-react";

export default function SearchResults({ results, onSelect }) {
  if (!results || results.length === 0) return null;

  return (
    <div className="search-results">
      <h3 className="sr-title">Papers Found on ArXiv</h3>
      <div className="paper-grid">
        {results.map((p, i) => (
          <div key={i} className="paper-card">
            <div className="paper-card-header">
              <h4 className="paper-title">{p.title}</h4>
              <a
                href={p.url}
                target="_blank"
                rel="noreferrer"
                className="paper-link"
              >
                <ExternalLink size={14} />
              </a>
            </div>

            <div className="paper-meta">
              <span><User size={12} /> {p.authors?.slice(0, 2).join(", ")}{p.authors?.length > 2 ? " et al." : ""}</span>
              {p.published && <span><Calendar size={12} /> {p.published}</span>}
            </div>

            <p className="paper-abstract">
              {p.abstract?.slice(0, 200)}…
            </p>

            {p.categories?.length > 0 && (
              <div className="paper-tags">
                <Tag size={11} />
                {p.categories.slice(0, 3).map((c, j) => (
                  <span key={j} className="tag small">{c}</span>
                ))}
              </div>
            )}

            <button
              className="btn-analyze-paper"
              onClick={() => onSelect(p)}
            >
              Analyze This Paper
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
