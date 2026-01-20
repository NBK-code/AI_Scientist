from typing import Dict, List

from src.schemas import DiscoveryRecord
from src.tools.search_arxiv import search_arxiv
from src.tools.search_semantic_scholar import search_semantic_scholar
from src.tools.search_duckduckgo import search_duckduckgo
from src.ranking.dedup import deduplicate_records
from src.ranking.ranking import rank_discovery_records


def run_discovery_pipeline(
    topic: str,
    *,
    arxiv_max_results: int = 20,
    semantic_scholar_max_results: int = 50,
    duckduckgo_max_results: int = 20,
    top_k: int = 10,
) -> Dict[str, List[DiscoveryRecord]]:
    """
    Run the full discovery → deduplication → ranking pipeline.

    Args:
        topic: Research topic (e.g., "continual learning").
        arxiv_max_results: Number of arXiv results to fetch.
        semantic_scholar_max_results: Number of Semantic Scholar results to fetch.
        duckduckgo_max_results: Number of DuckDuckGo blog results to fetch.
        top_k: Number of items per ranking category.

    Returns:
        Dictionary of ranked research views.
    """

    # ---- 1. Search phase ----
    arxiv_results = search_arxiv(topic, max_results=arxiv_max_results)
    semantic_results = search_semantic_scholar(
        topic, max_results=semantic_scholar_max_results
    )
    duckduckgo_results = search_duckduckgo(
        f"{topic} machine learning", max_results=duckduckgo_max_results
    )

    # ---- 2. Merge ----
    all_results: List[DiscoveryRecord] = (
        arxiv_results
        + semantic_results
        + duckduckgo_results
    )

    # ---- 3. Deduplicate ----
    unique_results = deduplicate_records(all_results)

    # ---- 4. Rank ----
    ranked_views = rank_discovery_records(
        unique_results,
        top_k=top_k,
    )

    return ranked_views


if __name__ == "__main__":
    views = run_discovery_pipeline("continual learning")

    for category, records in views.items():
        print(f"\n=== {category.upper()} ===")
        for r in records:
            print(f"- {r.title} ({r.year}) [{r.source}]")
