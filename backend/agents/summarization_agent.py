"""
Summarization Agent
Generates a short summary, key contributions, and major findings.
"""
import json
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from agents.llm_helper import get_llm

SUMMARY_PROMPT = PromptTemplate(
    input_variables=["paper_text", "reader_analysis"],
    template="""You are a Research Summarization Agent. Based on the paper text and extracted analysis, 
generate a clear, structured summary suitable for a researcher.

Return a JSON object with these exact keys:
{{
  "short_summary": "2-3 sentence overview of the entire paper",
  "key_contributions": ["contribution 1", "contribution 2", "contribution 3"],
  "major_findings": ["finding 1", "finding 2", "finding 3"],
  "practical_implications": "How this research can be applied in practice",
  "target_audience": "Who would benefit most from this research"
}}

Return ONLY valid JSON. No markdown, no explanation.

READER ANALYSIS:
{reader_analysis}

PAPER TEXT (excerpt):
{paper_text}
""",
)


class SummarizationAgent:
    def __init__(self):
        self.llm = get_llm(temperature=0.4)
        self.chain = LLMChain(llm=self.llm, prompt=SUMMARY_PROMPT)

    def summarize(self, paper_text: str, reader_analysis: dict) -> dict:
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
                "short_summary": response[:500],
                "key_contributions": [],
                "major_findings": [],
                "practical_implications": "",
                "target_audience": "",
            }
