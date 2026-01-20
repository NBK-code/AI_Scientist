"""
arXiv search tool.

Responsibilities:
- Query the arXiv API
- Parse results
- Normalize metadata into DiscoveryRecord
- Return a list of DiscoveryRecord objects

Non-responsibilities:
- Ranking
- Deduplication
- Summarization
- Reasoning
"""

from typing import List
import requests
import xml.etree.ElementTree as ET

from src.schemas import DiscoveryRecord


ARXIV_API_URL = "http://export.arxiv.org/api/query"


def search_arxiv(query: str, max_results: int = 20) -> List[DiscoveryRecord]:
    """
    Search arXiv for papers matching the query.

    Args:
        query: Search query string.
        max_results: Maximum number of results to return.

    Returns:
        List of DiscoveryRecord objects normalized from arXiv results.
    """

    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending",
    }

    response = requests.get(ARXIV_API_URL, params=params, timeout=15)
    response.raise_for_status()

    root = ET.fromstring(response.text)

    # arXiv Atom namespace
    ns = {"atom": "http://www.w3.org/2005/Atom"}

    records: List[DiscoveryRecord] = []

    for entry in root.findall("atom:entry", ns):
        title = entry.findtext("atom:title", default="", namespaces=ns).strip()
        summary = entry.findtext("atom:summary", default="", namespaces=ns).strip()

        published = entry.findtext("atom:published", default=None, namespaces=ns)
        year = None
        if published:
            try:
                year = int(published[:4])
            except ValueError:
                year = None

        authors = [
            author.findtext("atom:name", default="", namespaces=ns).strip()
            for author in entry.findall("atom:author", ns)
        ]

        url = entry.findtext("atom:id", default="", namespaces=ns).strip()

        # Determine type (simple heuristic)
        title_lower = title.lower()
        if "survey" in title_lower or "review" in title_lower:
            record_type = "survey"
        else:
            record_type = "paper"

        record = DiscoveryRecord(
            title=title,
            authors=authors,
            year=year,
            type=record_type,
            source="arxiv",
            citations=None,  # arXiv does not provide citation counts
            url=url,
            abstract_or_snippet=summary,
        )

        records.append(record)

    return records


if __name__ == "__main__":
    # Simple manual test
    results = search_arxiv("Neural scaling laws", max_results=10)
    for r in results:
        print(f"- {r.title} ({r.year})")
