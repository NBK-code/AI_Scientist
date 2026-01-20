import pytest
import requests

from src.tools.search_semantic_scholar import search_semantic_scholar
from src.schemas import DiscoveryRecord


def test_search_semantic_scholar_basic():
    """
    Basic sanity test for Semantic Scholar search.

    This test verifies our integration and schema normalization.
    It must NOT fail due to external rate limits (HTTP 429).
    """

    try:
        results = search_semantic_scholar("continual learning", max_results=3)
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code == 429:
            pytest.skip("Semantic Scholar rate limited (HTTP 429)")
        raise

    assert isinstance(results, list)

    if len(results) == 0:
        return

    for record in results:
        assert isinstance(record, DiscoveryRecord)
        assert record.title
        assert record.url
        assert record.source == "semantic_scholar"
        assert record.type in {"paper", "survey"}
        assert record.citations is None or isinstance(record.citations, int)
