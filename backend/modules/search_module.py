"""
Search Module
Searches ArXiv for research papers relevant to a query.
"""
import arxiv
from typing import Optional


class SearchModule:

    def search(self, query: str, max_results: int = 5) -> list[dict]:
        """Search ArXiv and return a list of paper metadata dicts."""
        client = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance,
        )

        results = []
        for paper in client.results(search):
            results.append({
                "title":     paper.title,
                "authors":   [a.name for a in paper.authors],
                "abstract":  paper.summary,
                "url":       paper.pdf_url,
                "arxiv_id":  paper.entry_id,
                "published": str(paper.published.date()) if paper.published else "",
                "categories": paper.categories,
            })

        return results
