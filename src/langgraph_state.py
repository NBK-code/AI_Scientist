from typing import TypedDict, List, Dict, Optional
from src.schemas import DiscoveryRecord


class QueryProposal(TypedDict):
    query: str
    rationale: str


class DiscoveryState(TypedDict):
    # Core topic
    topic: str

    # Accumulated evidence (from ALL searches)
    records: List[DiscoveryRecord]

    # Loop control
    iteration: int
    max_iterations: int
    pending_queries: List[QueryProposal]
    current_query_index: int
    approved_query: Optional[str]

    # Post-loop processing
    deduped_records: List[DiscoveryRecord]
    ranked_views: Dict[str, List[DiscoveryRecord]]

    # Final output
    synthesis_markdown: str
    evaluation_report: dict

