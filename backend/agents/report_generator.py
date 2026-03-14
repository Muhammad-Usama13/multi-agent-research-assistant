"""
Report Generator
Compiles all agent outputs into a structured markdown research report.
"""
import json
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from agents.llm_helper import get_llm

REPORT_PROMPT = PromptTemplate(
    input_variables=["query", "reader", "summary", "explanation", "critique"],
    template="""You are a Research Report Generator. Compile the following agent outputs into a 
professional, well-structured markdown research analysis report.

The report should have these sections:
# Research Analysis Report: {query}

## Executive Summary
(Use the short_summary)

## Key Contributions
(List the key contributions)

## Methodology Explained
(Use methodology_explained from explanation agent)

## Major Findings
(List major findings)

## Critical Evaluation
(Use strengths, weaknesses, limitations)

## Practical Implications
(Combine practical_implications and why_it_matters)

## Recommendations for Future Work
(Use potential_improvements)

---

READER ANALYSIS:
{reader}

SUMMARY:
{summary}

EXPLANATION:
{explanation}

CRITIQUE:
{critique}

Write the full report in markdown. Be professional, clear, and informative.
""",
)


class ReportGenerator:
    def __init__(self):
        self.llm = get_llm(temperature=0.4)
        self.chain = LLMChain(llm=self.llm, prompt=REPORT_PROMPT)

    def generate(
        self,
        query: str,
        reader: dict,
        summary: dict,
        explanation: dict,
        critique: dict,
    ) -> str:
        try:
            report = self.chain.run(
                query=query,
                reader=json.dumps(reader, indent=2),
                summary=json.dumps(summary, indent=2),
                explanation=json.dumps(explanation, indent=2),
                critique=json.dumps(critique, indent=2),
            )
            return report
        except Exception as e:
            return f"# Research Report\n\nReport generation encountered an error: {str(e)}"
