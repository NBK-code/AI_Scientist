from mcp.server import tool
from src.ranking.ranking import rank_discovery_records
from src.schemas import DiscoveryRecord
from typing import List, Dict


@tool(
    name="rank_discovery_records",
    description="Rank discovery records into multiple ranked views"
)
def rank_discovery_records_tool(records: List[DiscoveryRecord]) -> Dict[str, List[DiscoveryRecord]]:
    return rank_discovery_records(records)
