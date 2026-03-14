// src/components/AgentPipeline.jsx
import React from "react";
import { Search, BookOpen, FileText, Lightbulb, MessageSquare, BarChart2 } from "lucide-react";

const AGENTS = [
  { icon: Search,        label: "Search Agent",        desc: "Finds relevant papers" },
  { icon: BookOpen,      label: "Reader Agent",         desc: "Extracts key info" },
  { icon: FileText,      label: "Summarization Agent",  desc: "Creates summaries" },
  { icon: Lightbulb,     label: "Explanation Agent",    desc: "Simplifies concepts" },
  { icon: MessageSquare, label: "Critic Agent",         desc: "Evaluates quality" },
  { icon: BarChart2,     label: "Report Generator",     desc: "Compiles final report" },
];

export default function AgentPipeline() {
  return (
    <div className="pipeline-section">
      <h3 className="pipeline-title">How It Works</h3>
      <div className="pipeline">
        {AGENTS.map(({ icon: Icon, label, desc }, i) => (
          <React.Fragment key={label}>
            <div className="agent-node">
              <div className="agent-icon-wrap">
                <Icon size={20} />
              </div>
              <span className="agent-label">{label}</span>
              <span className="agent-desc">{desc}</span>
            </div>
            {i < AGENTS.length - 1 && (
              <div className="pipeline-arrow">→</div>
            )}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
}
