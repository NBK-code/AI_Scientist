"""
Semantic Scholar search tool.

Responsibilities:
- Query the Semantic Scholar API
- Parse results
- Normalize metadata into DiscoveryRecord
- Return a list of DiscoveryRecord objects

Non-responsibilities:
- Ranking across sources
- Deduplication
- Reasoning or summarization
"""

from typing import List
import time
import requests

from src.schemas import DiscoveryRecord


SEMANTIC_SCHOLAR_API_URL = "https://api.semanticscholar.org/graph/v1/paper/search"


def search_semantic_scholar(
    query: str,
    max_results: int = 20,
    max_retries: int = 3,
    backoff_seconds: float = 1.0,
) -> List[DiscoveryRecord]:
    """
    Search Semantic Scholar for papers matching the query.

    Includes retry logic with exponential backoff to handle rate limits (HTTP 429).
    """

    params = {
        "query": query,
        "limit": max_results,
        "fields": "title,authors,year,citationCount,abstract,url,venue",
    }

    for attempt in range(max_retries):
        try:
            response = requests.get(
                SEMANTIC_SCHOLAR_API_URL,
                params=params,
                timeout=15,
            )
            response.raise_for_status()
            break
        except requests.HTTPError as e:
            # Retry only on rate limit
            if response.status_code == 429 and attempt < max_retries - 1:
                sleep_time = backoff_seconds * (2 ** attempt)
                time.sleep(sleep_time)
                continue
            raise

    data = response.json()
    papers = data.get("data", [])

    records: List[DiscoveryRecord] = []

    for paper in papers:
        title = paper.get("title", "").strip()
        url = paper.get("url")

        if not title or not url:
            continue

        authors = [
            a.get("name", "").strip()
            for a in paper.get("authors", [])
            if "name" in a
        ]

        year = paper.get("year")
        citations = paper.get("citationCount")
        abstract = paper.get("abstract")

        title_lower = title.lower()
        record_type = "survey" if ("survey" in title_lower or "review" in title_lower) else "paper"

        records.append(
            DiscoveryRecord(
                title=title,
                authors=authors,
                year=year,
                type=record_type,
                source="semantic_scholar",
                citations=citations,
                url=url,
                abstract_or_snippet=abstract,
            )
        )

    return records


if __name__ == "__main__":
    # Simple manual test
    results = search_semantic_scholar("neural scaling laws", max_results=10)
    for r in results:
        print(f"- {r.title} ({r.year}) | citations={r.citations}")
