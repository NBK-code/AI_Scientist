from src.schemas import DiscoveryRecord
from src.ranking.dedup import deduplicate_records


def test_deduplication_merges_duplicates():
    r1 = DiscoveryRecord(
        title="A Survey on Continual Learning",
        authors=["Author A"],
        year=2019,
        type="survey",
        source="arxiv",
        citations=None,
        url="https://arxiv.org/abs/1234.5678",
        abstract_or_snippet="Survey of continual learning.",
    )

    r2 = DiscoveryRecord(
        title="A Survey on Continual Learning",
        authors=["Author B"],
        year=2019,
        type="paper",
        source="semantic_scholar",
        citations=1500,
        url="https://arxiv.org/abs/1234.5678",
        abstract_or_snippet=None,
    )

    deduped = deduplicate_records([r1, r2])

    assert len(deduped) == 1
    record = deduped[0]

    # Metadata merged
    assert set(record.authors) == {"Author A", "Author B"}
    assert record.citations == 1500
    assert record.abstract_or_snippet is not None


def test_deduplication_keeps_unique_records():
    r1 = DiscoveryRecord(
        title="Paper One",
        authors=["A"],
        year=2020,
        type="paper",
        source="arxiv",
        citations=None,
        url="https://arxiv.org/abs/1111.1111",
        abstract_or_snippet="One",
    )

    r2 = DiscoveryRecord(
        title="Paper Two",
        authors=["B"],
        year=2021,
        type="paper",
        source="semantic_scholar",
        citations=50,
        url="https://example.com/paper-two",
        abstract_or_snippet="Two",
    )

    deduped = deduplicate_records([r1, r2])
    assert len(deduped) == 2
