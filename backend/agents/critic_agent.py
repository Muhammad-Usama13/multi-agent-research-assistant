"""
Critic Agent
Evaluates the research paper — strengths, weaknesses, limitations, improvements.
"""
import json
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from agents.llm_helper import get_llm

CRITIC_PROMPT = PromptTemplate(
    input_variables=["paper_text", "reader_analysis"],
    template="""You are a Critical Research Evaluation Agent. Provide a rigorous, balanced critique.

Return a JSON object with these exact keys:
{{
  "overall_rating": 7,
  "strengths": [
    "strength 1",
    "strength 2",
    "strength 3"
  ],
  "weaknesses": [
    "weakness 1",
    "weakness 2"
  ],
  "limitations": [
    "limitation 1",
    "limitation 2"
  ],
  "potential_improvements": [
    "improvement suggestion 1",
    "improvement suggestion 2",
    "improvement suggestion 3"
  ],
  "novelty_assessment": "Assessment of how novel/original this work is",
  "reproducibility": "Assessment of whether the work can be reproduced"
}}

overall_rating must be an integer 1-10.
Return ONLY valid JSON. No markdown, no explanation.

READER ANALYSIS:
{reader_analysis}

PAPER TEXT (excerpt):
{paper_text}
""",
)


class CriticAgent:
    def __init__(self):
        self.llm = get_llm(temperature=0.3)
        self.chain = LLMChain(llm=self.llm, prompt=CRITIC_PROMPT)

    def critique(self, paper_text: str, reader_analysis: dict) -> dict:
        truncated = paper_text[:6000]
        try:
            response = self.chain.run(
                paper_text=truncated,
                reader_analysis=json.dumps(reader_analysis, indent=2),
            )
            clean = response.strip().strip("```json").strip("```").strip()
            return json.loads(clean)
        except json.JSONDecodeError:
            return {
                "overall_rating": 0,
                "strengths": [],
                "weaknesses": [],
                "limitations": [],
                "potential_improvements": [],
                "novelty_assessment": "",
                "reproducibility": "",
            }
