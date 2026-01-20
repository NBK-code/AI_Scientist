from src.tools.search_duckduckgo import search_duckduckgo
from src.schemas import DiscoveryRecord


def test_search_duckduckgo_basic():
    """
    Basic sanity test for DuckDuckGo search.

    This test verifies:
    - The function returns a list
    - Returned items are DiscoveryRecord objects
    - Core fields are populated
    - Schema invariants hold

    It does NOT assume any specific blog titles or URLs.
    """

    results = search_duckduckgo(
        "continual learning machine learning",
        max_results=5,
    )

    assert isinstance(results, list)

    # DuckDuckGo may occasionally return zero results;
    # in that case, we only assert that the function runs.
    if len(results) == 0:
        return

    for record in results:
        assert isinstance(record, DiscoveryRecord)

        # Required fields
        assert record.title
        assert record.url
        assert record.source == "duckduckgo"

        # DuckDuckGo–specific expectations
        assert record.type in {"blog", "survey"}
        assert record.citations is None

        # Optional fields should not break anything
        assert record.year is None or isinstance(record.year, int)
