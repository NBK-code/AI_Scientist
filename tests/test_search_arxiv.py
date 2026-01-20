import pytest

from src.tools.search_arxiv import search_arxiv
from src.schemas import DiscoveryRecord


def test_search_arxiv_basic():
    """
    Basic sanity test for arXiv search.

    This test verifies that:
    - The function returns a list
    - Returned items are DiscoveryRecord objects
    - Core fields are populated correctly

    It does NOT assume any specific paper titles.
    """

    results = search_arxiv("continual learning", max_results=3)

    # Basic type checks
    assert isinstance(results, list)
    assert len(results) > 0

    for record in results:
        assert isinstance(record, DiscoveryRecord)

        # Required fields
        assert record.title
        assert record.url
        assert record.source == "arxiv"

        # arXiv-specific expectations
        assert record.type in {"paper", "survey"}
        assert record.citations is None  # arXiv does not provide citations

        # Year is optional but if present must be reasonable
        if record.year is not None:
            assert 1900 <= record.year <= 2100
