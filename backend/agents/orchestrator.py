"""
Research Orchestrator
Uses LangGraph to wire all agents into a sequential state machine pipeline.

Pipeline:
  reader_node → summarization_node → explanation_node → critic_node → report_node
"""
from typing import TypedDict, Any
from langgraph.graph import StateGraph, END

from agents.reader_agent import ReaderAgent
from agents.summarization_agent import SummarizationAgent
from agents.explanation_agent import ExplanationAgent
from agents.critic_agent import CriticAgent
from agents.report_generator import ReportGenerator


# ── State definition ───────────────────────────────────────────────────────────
class ResearchState(TypedDict):
    query: str
    paper_text: str
    sections: dict
    mode: str
    reader: dict
    summary: dict
    explanation: dict
    critique: dict
    report: str


# ── Node functions ─────────────────────────────────────────────────────────────
def reader_node(state: ResearchState) -> ResearchState:
    agent = ReaderAgent()
    state["reader"] = agent.analyze(state["paper_text"])
    return state


def summarization_node(state: ResearchState) -> ResearchState:
    agent = SummarizationAgent()
    state["summary"] = agent.summarize(state["paper_text"], state["reader"])
    return state


def explanation_node(state: ResearchState) -> ResearchState:
    agent = ExplanationAgent()
    methodology = state["reader"].get("methodology", "")
    state["explanation"] = agent.explain(state["paper_text"], methodology)
    return state


def critic_node(state: ResearchState) -> ResearchState:
    agent = CriticAgent()
    state["critique"] = agent.critique(state["paper_text"], state["reader"])
    return state


def report_node(state: ResearchState) -> ResearchState:
    generator = ReportGenerator()
    state["report"] = generator.generate(
        query=state["query"],
        reader=state["reader"],
        summary=state["summary"],
        explanation=state["explanation"],
        critique=state["critique"],
    )
    return state


# ── Graph assembly ─────────────────────────────────────────────────────────────
def build_graph() -> StateGraph:
    graph = StateGraph(ResearchState)

    # Node names must NOT match any key in ResearchState.
    # Prefix with "node_" to avoid conflicts.
    graph.add_node("node_reader",        reader_node)
    graph.add_node("node_summarization", summarization_node)
    graph.add_node("node_explanation",   explanation_node)
    graph.add_node("node_critic",        critic_node)
    graph.add_node("node_report",        report_node)

    graph.set_entry_point("node_reader")
    graph.add_edge("node_reader",        "node_summarization")
    graph.add_edge("node_summarization", "node_explanation")
    graph.add_edge("node_explanation",   "node_critic")
    graph.add_edge("node_critic",        "node_report")
    graph.add_edge("node_report",        END)

    return graph.compile()


class ResearchOrchestrator:
    def __init__(self):
        self.graph = build_graph()

    def run(
        self,
        query: str,
        paper_text: str,
        sections: dict,
        mode: str = "full",
    ) -> dict:
        initial_state: ResearchState = {
            "query": query,
            "paper_text": paper_text,
            "sections": sections,
            "mode": mode,
            "reader": {},
            "summary": {},
            "explanation": {},
            "critique": {},
            "report": "",
        }
        final_state = self.graph.invoke(initial_state)
        return {
            "reader":      final_state["reader"],
            "summary":     final_state["summary"],
            "explanation": final_state["explanation"],
            "critique":    final_state["critique"],
            "report":      final_state["report"],
        }