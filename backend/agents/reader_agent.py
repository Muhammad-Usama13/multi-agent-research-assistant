"""
Reader Agent
Analyzes paper text and extracts: problem, methodology, dataset, results.
"""
import json
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from agents.llm_helper import get_llm

READER_PROMPT = PromptTemplate(
    input_variables=["paper_text"],
    template="""You are a Research Reader Agent. Carefully analyze the following research paper text.

Extract and return a JSON object with these exact keys:
{{
  "research_question": "The main research problem or question addressed",
  "methodology": "The methods, algorithms, or approaches used",
  "dataset": "Datasets or experimental setup used (if mentioned)",
  "results": "Main quantitative or qualitative results achieved",
  "contributions": ["contribution 1", "contribution 2", "contribution 3"],
  "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"]
}}

Return ONLY valid JSON. No markdown, no explanation.

PAPER TEXT:
{paper_text}
""",
)


class ReaderAgent:
    def __init__(self):
        self.llm = get_llm(temperature=0.1)
        self.chain = LLMChain(llm=self.llm, prompt=READER_PROMPT)

    def analyze(self, paper_text: str) -> dict:
        # Truncate to avoid token limits
        truncated = paper_text[:8000]
        try:
            response = self.chain.run(paper_text=truncated)
            # Strip markdown code blocks if present
            clean = response.strip().strip("```json").strip("```").strip()
            return json.loads(clean)
        except json.JSONDecodeError:
            return {
                "research_question": "Could not extract",
                "methodology": "Could not extract",
                "dataset": "Not mentioned",
                "results": "Could not extract",
                "contributions": [],
                "keywords": [],
                "raw_response": response,
            }
