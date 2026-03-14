"""
Document Processor Module
Handles PDF parsing, text extraction, and section detection.
"""
import re
from typing import Optional

try:
    import pdfplumber
    PDF_BACKEND = "pdfplumber"
except ImportError:
    try:
        import PyPDF2
        PDF_BACKEND = "pypdf2"
    except ImportError:
        PDF_BACKEND = None


SECTION_PATTERNS = [
    r"\babstract\b",
    r"\b(1\.?\s*)?introduction\b",
    r"\b(2\.?\s*)?related\s+work\b",
    r"\b(3\.?\s*)?methodology\b",
    r"\b(3\.?\s*)?method(s)?\b",
    r"\b(3\.?\s*)?approach\b",
    r"\b(4\.?\s*)?experiment(s|al\s+results)?\b",
    r"\b(4\.?\s*)?results?\b",
    r"\b(5\.?\s*)?discussion\b",
    r"\b(6\.?\s*)?conclusion(s)?\b",
    r"\breferences\b",
    r"\backnowledg(e?ment)?s?\b",
]


class DocumentProcessor:

    def process_pdf(self, pdf_path: str) -> dict:
        if PDF_BACKEND == "pdfplumber":
            return self._process_pdfplumber(pdf_path)
        elif PDF_BACKEND == "pypdf2":
            return self._process_pypdf2(pdf_path)
        else:
            raise RuntimeError("No PDF library installed. Run: pip install pdfplumber")

    # ── pdfplumber ─────────────────────────────────────────────────────────────
    def _process_pdfplumber(self, pdf_path: str) -> dict:
        import pdfplumber
        pages_text = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    pages_text.append(text)

        full_text = "\n".join(pages_text)
        return {
            "full_text": full_text,
            "pages": len(pages_text),
            "sections": self._extract_sections(full_text),
        }

    # ── PyPDF2 fallback ────────────────────────────────────────────────────────
    def _process_pypdf2(self, pdf_path: str) -> dict:
        import PyPDF2
        pages_text = []
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    pages_text.append(text)

        full_text = "\n".join(pages_text)
        return {
            "full_text": full_text,
            "pages": len(pages_text),
            "sections": self._extract_sections(full_text),
        }

    # ── Section detection ──────────────────────────────────────────────────────
    def _extract_sections(self, text: str) -> dict:
        sections: dict[str, str] = {}
        lines = text.split("\n")
        current_section: Optional[str] = None
        current_content: list[str] = []

        for line in lines:
            line_lower = line.strip().lower()
            matched_section = None

            for pattern in SECTION_PATTERNS:
                if re.match(pattern, line_lower, re.IGNORECASE):
                    # Only treat short lines as section headers
                    if len(line.strip()) < 60:
                        matched_section = line.strip().lower()
                        break

            if matched_section:
                # Save previous section
                if current_section and current_content:
                    sections[current_section] = "\n".join(current_content).strip()
                current_section = matched_section
                current_content = []
            elif current_section is not None:
                current_content.append(line)

        # Save last section
        if current_section and current_content:
            sections[current_section] = "\n".join(current_content).strip()

        # Fallback: if no sections found, store everything as "full text"
        if not sections:
            sections["full text"] = text[:10000]

        return sections
