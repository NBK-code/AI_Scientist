from datetime import datetime
from src.schemas import DiscoveryRecord
from src.ranking.ranking import rank_discovery_records


def test_ranking_views():
    current_year = datetime.now().year

    records = [
        DiscoveryRecord(
            title="Old Influential Paper",
            authors=["A"],
            year=current_year - 10,
            type="paper",
            source="semantic_scholar",
            citations=5000,
            url="https://example.com/old",
            abstract_or_snippet="Old but gold",
        ),
        DiscoveryRecord(
            title="Recent Cited Paper",
            authors=["B"],
            year=current_year - 2,
            type="paper",
            source="semantic_scholar",
            citations=800,
            url="https://example.com/recent-cited",
            abstract_or_snippet="Recent and cited",
        ),
        DiscoveryRecord(
            title="Brand New Paper",
            authors=["C"],
            year=current_year,
            type="paper",
            source="arxiv",
            citations=None,
            url="https://example.com/new",
            abstract_or_snippet="New idea",
        ),
    ]

    ranked = rank_discovery_records(records, top_k=2)

    # Top all-time cited
    assert ranked["top_all_time_cited"][0].title == "Old Influential Paper"

    # Top recent cited
    assert ranked["top_recent_cited"][0].title == "Recent Cited Paper"

    # Recent relevant
    assert any(
        r.title == "Brand New Paper"
        for r in ranked["top_recent_relevant"]
    )

    # Emerging work
    assert any(
        r.title == "Brand New Paper"
        for r in ranked["emerging_work"]
    )
