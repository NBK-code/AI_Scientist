from mcp.server import tool
from src.ranking.dedup import deduplicate_records
from src.schemas import DiscoveryRecord
from typing import List


@tool(
    name="deduplicate_records",
    description="Deduplicate discovery records from multiple sources"
)
def deduplicate_records_tool(records: List[DiscoveryRecord]):
    return deduplicate_records(records)
