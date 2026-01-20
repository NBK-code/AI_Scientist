from typing import List, Dict
from datetime import datetime

from src.schemas import DiscoveryRecord


def rank_discovery_records(
    records: List[DiscoveryRecord],
    *,
    top_k: int = 10,
    recent_cited_years: int = 4,
    recent_relevant_years: int = 2,
) -> Dict[str, List[DiscoveryRecord]]:
    """
    Rank and slice discovery records into multiple research views.

    This function is PURE:
    - No API calls
    - No LLM usage
    - No side effects

    Args:
        records: List of DiscoveryRecord objects (already discovered).
        top_k: Number of records to return per category.
        recent_cited_years: Time window for recent cited papers.
        recent_relevant_years: Time window for recent relevant papers.

    Returns:
        Dictionary of ranked research views.
    """

    current_year = datetime.now().year

    # ---- Helper filters ----
    def has_citations(r: DiscoveryRecord) -> bool:
        return r.citations is not None

    def has_year(r: DiscoveryRecord) -> bool:
        return r.year is not None

    # ---- 1. Top all-time cited ----
    top_all_time_cited = sorted(
        (r for r in records if has_citations(r)),
        key=lambda r: r.citations or 0,
        reverse=True,
    )[:top_k]

    # ---- 2. Top cited in recent years ----
    top_recent_cited = sorted(
        (
            r for r in records
            if has_citations(r)
            and has_year(r)
            and r.year >= current_year - recent_cited_years
        ),
        key=lambda r: r.citations or 0,
        reverse=True,
    )[:top_k]

    # ---- 3. Most relevant in recent years ----
    # IMPORTANT:
    # We preserve original ordering (assumed relevance ordering from search)
    top_recent_relevant = [
        r for r in records
        if has_year(r)
        and r.year >= current_year - recent_relevant_years
    ][:top_k]

    # ---- 4. Emerging work (new + low citation) ----
    emerging_work = [
        r for r in records
        if has_year(r)
        and r.year >= current_year - 1
        and (r.citations is None or r.citations < 10)
    ][:top_k]

    return {
        "top_all_time_cited": top_all_time_cited,
        "top_recent_cited": top_recent_cited,
        "top_recent_relevant": top_recent_relevant,
        "emerging_work": emerging_work,
    }
