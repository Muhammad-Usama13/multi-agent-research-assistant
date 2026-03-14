"""
Explanation Agent
Simplifies complex technical concepts, algorithms, and terminology.
"""
import json
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from agents.llm_helper import get_llm

EXPLANATION_PROMPT = PromptTemplate(
    input_variables=["paper_text", "methodology"],
    template="""You are a Research Explanation Agent. Your job is to make complex research accessible.

Analyze the methodology and technical content, then explain it simply.

Return a JSON object with these exact keys:
{{
  "simple_explanation": "Explain what this research does as if explaining to a curious non-expert (3-4 sentences)",
  "methodology_explained": "Explain the methods used in plain language",
  "technical_terms": [
    {{"term": "technical term 1", "definition": "simple definition"}},
    {{"term": "technical term 2", "definition": "simple definition"}},
    {{"term": "technical term 3", "definition": "simple definition"}}
  ],
  "analogy": "A real-world analogy that helps understand this research",
  "why_it_matters": "Why this research is important in simple terms"
}}

Return ONLY valid JSON. No markdown, no explanation.

METHODOLOGY:
{methodology}

PAPER TEXT (excerpt):
{paper_text}
""",
)


class ExplanationAgent:
    def __init__(self):
        self.llm = get_llm(temperature=0.5)
        self.chain = LLMChain(llm=self.llm, prompt=EXPLANATION_PROMPT)

    def explain(self, paper_text: str, methodology: str) -> dict:
        truncated = paper_text[:5000]
        try:
            response = self.chain.run(
                paper_text=truncated,
                methodology=methodology,
            )
            clean = response.strip().strip("```json").strip("```").strip()
            return json.loads(clean)
        except json.JSONDecodeError:
            return {
                "simple_explanation": response[:400],
                "methodology_explained": methodology,
                "technical_terms": [],
                "analogy": "",
                "why_it_matters": "",
            }
