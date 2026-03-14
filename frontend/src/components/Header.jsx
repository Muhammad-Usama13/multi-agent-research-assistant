// src/components/Header.jsx
import React from "react";
import { Cpu, BookOpen } from "lucide-react";

export default function Header() {
  return (
    <header className="header">
      <div className="header-inner">
        <div className="header-brand">
          <div className="brand-icon">
            <Cpu size={22} />
          </div>
          <div>
            <h1 className="brand-title">ResearchMind</h1>
            <span className="brand-sub">Multi-Agent Research Assistant</span>
          </div>
        </div>
        <nav className="header-nav">
          <span className="nav-badge">
            <BookOpen size={13} />
            Powered by Gemini + LangGraph
          </span>
        </nav>
      </div>
    </header>
  );
}
