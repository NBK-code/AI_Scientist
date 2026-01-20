from typing import List, Dict
import re
from urllib.parse import urlparse

from src.schemas import DiscoveryRecord


def _normalize_title(title: str) -> str:
    """
    Normalize title for deduplication:
    - lowercase
    - remove punctuation
    - collapse whitespace
    """
    title = title.lower()
    title = re.sub(r"[^\w\s]", "", title)
    title = re.sub(r"\s+", " ", title).strip()
    return title


def _normalize_url(url) -> str:
    """
    Normalize URL for deduplication:
    - Convert HttpUrl to str
    - Remove scheme
    - Remove trailing slashes
    """
    url_str = str(url)
    parsed = urlparse(url_str)
    return f"{parsed.netloc}{parsed.path}".rstrip("/")


def _merge_records(a: DiscoveryRecord, b: DiscoveryRecord) -> DiscoveryRecord:
    """
    Merge two records referring to the same resource.
    Preference rules:
    - Keep citations if available
    - Keep year if available
    - Keep abstract if available
    - Merge authors
    """

    return DiscoveryRecord(
        title=a.title,
        authors=list({*a.authors, *b.authors}),
        year=a.year or b.year,
        type=a.type if a.type != "blog" else b.type,
        source=a.source,  # source is informational; we keep the first
        citations=a.citations if a.citations is not None else b.citations,
        url=a.url,
        abstract_or_snippet=a.abstract_or_snippet or b.abstract_or_snippet,
    )


def deduplicate_records(
    records: List[DiscoveryRecord],
) -> List[DiscoveryRecord]:
    """
    Deduplicate discovery records based on URL and title similarity.

    Args:
        records: List of DiscoveryRecord objects from multiple sources.

    Returns:
        List of deduplicated DiscoveryRecord objects.
    """

    by_url: Dict[str, DiscoveryRecord] = {}
    by_title: Dict[str, DiscoveryRecord] = {}

    for record in records:
        url_key = _normalize_url(record.url)
        title_key = _normalize_title(record.title)

        # First: try URL-based deduplication
        if url_key in by_url:
            by_url[url_key] = _merge_records(by_url[url_key], record)
            continue

        # Second: try title-based deduplication
        if title_key in by_title:
            merged = _merge_records(by_title[title_key], record)
            by_title[title_key] = merged
            by_url[url_key] = merged
            continue

        # New unique record
        by_url[url_key] = record
        by_title[title_key] = record

    return list(by_url.values())
