"""
Shared LLM instance using Google Gemini via LangChain.
"""
import os
from langchain_google_genai import ChatGoogleGenerativeAI


def get_llm(temperature: float = 0.3) -> ChatGoogleGenerativeAI:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not set. Add it to backend/.env"
        )
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=temperature,
    )
