// src/components/QueryInput.jsx
import React, { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { Search, Upload, X, FileText, Loader2 } from "lucide-react";

export default function QueryInput({ onQuery, onPDF, loading }) {
  const [query, setQuery] = useState("");
  const [file, setFile]   = useState(null);
  const [tab, setTab]     = useState("query"); // "query" | "pdf"

  const onDrop = useCallback((accepted) => {
    if (accepted.length) setFile(accepted[0]);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "application/pdf": [".pdf"] },
    maxFiles: 1,
    disabled: loading,
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (tab === "query" && query.trim()) onQuery(query.trim());
    if (tab === "pdf" && file) onPDF(file);
  };

  return (
    <div className="query-card">
      {/* Tabs */}
      <div className="tabs">
        <button
          className={`tab ${tab === "query" ? "active" : ""}`}
          onClick={() => setTab("query")}
        >
          <Search size={15} /> Search Topic
        </button>
        <button
          className={`tab ${tab === "pdf" ? "active" : ""}`}
          onClick={() => setTab("pdf")}
        >
          <Upload size={15} /> Upload PDF
        </button>
      </div>

      <form onSubmit={handleSubmit} className="query-form">
        {tab === "query" ? (
          <div className="input-row">
            <div className="input-wrap">
              <Search size={17} className="input-icon" />
              <input
                className="query-input"
                type="text"
                placeholder='e.g. "video anomaly detection using deep learning"'
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                disabled={loading}
              />
              {query && (
                <button
                  type="button"
                  className="input-clear"
                  onClick={() => setQuery("")}
                >
                  <X size={14} />
                </button>
              )}
            </div>
            <button
              type="submit"
              className="btn-analyze"
              disabled={!query.trim() || loading}
            >
              {loading ? <Loader2 size={17} className="spin" /> : <Search size={17} />}
              {loading ? "Analyzing…" : "Analyze"}
            </button>
          </div>
        ) : (
          <div className="pdf-section">
            <div
              {...getRootProps()}
              className={`dropzone ${isDragActive ? "drag-over" : ""} ${file ? "has-file" : ""}`}
            >
              <input {...getInputProps()} />
              {file ? (
                <div className="file-info">
                  <FileText size={28} />
                  <span className="file-name">{file.name}</span>
                  <span className="file-size">{(file.size / 1024).toFixed(1)} KB</span>
                  <button
                    type="button"
                    className="file-remove"
                    onClick={(e) => { e.stopPropagation(); setFile(null); }}
                  >
                    <X size={14} /> Remove
                  </button>
                </div>
              ) : (
                <div className="drop-hint">
                  <Upload size={28} />
                  <p>Drop your PDF here or <span>browse</span></p>
                  <small>Research papers up to 50MB</small>
                </div>
              )}
            </div>
            <button
              type="submit"
              className="btn-analyze full"
              disabled={!file || loading}
            >
              {loading ? <Loader2 size={17} className="spin" /> : <FileText size={17} />}
              {loading ? "Analyzing…" : "Analyze PDF"}
            </button>
          </div>
        )}
      </form>
    </div>
  );
}
