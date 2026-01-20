"""
DuckDuckGo web search tool (blogs, tutorials, surveys).

Uses duckduckgo-search library for real web results.

Responsibilities:
- Perform web search
- Extract blog / tutorial resources
- Normalize metadata into DiscoveryRecord

Non-responsibilities:
- Ranking across sources
- Deduplication
- Scraping page content
"""

from typing import List
from ddgs import DDGS

from src.schemas import DiscoveryRecord


def search_duckduckgo(query: str, max_results: int = 20) -> List[DiscoveryRecord]:
    """
    Search DuckDuckGo for blogs and web resources related to the query.
    """

    records: List[DiscoveryRecord] = []

    with DDGS() as ddgs:
        results = ddgs.text(
            query,
            max_results=max_results,
            region="us-en",   # 🔴 IMPORTANT
            safesearch="off",
        )

        for r in results:
            title = r.get("title", "").strip()
            url = r.get("href", "").strip()
            snippet = r.get("body", "").strip()

            if not title or not url:
                continue

            title_lower = title.lower()
            if "survey" in title_lower or "review" in title_lower:
                record_type = "survey"
            else:
                record_type = "blog"

            record = DiscoveryRecord(
                title=title,
                authors=[],
                year=None,
                type=record_type,
                source="duckduckgo",
                citations=None,
                url=url,
                abstract_or_snippet=snippet,
            )

            records.append(record)

            if len(records) >= max_results:
                break

    return records


if __name__ == "__main__":
    results = search_duckduckgo(
        "continual learning machine learning blog",
        max_results=5,
    )
    for r in results:
        print(f"- {r.title}")
