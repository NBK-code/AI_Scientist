from mcp.server import tool
from src.synthesis.abstract_synthesis import synthesize_literature_from_abstracts
from src.schemas import DiscoveryRecord
from typing import List


@tool(
    name="synthesize_from_abstracts",
    description="Synthesize a literature review from paper abstracts"
)
def synthesize_from_abstracts_tool(
    topic: str,
    papers: List[DiscoveryRecord]
) -> str:
    return synthesize_literature_from_abstracts(topic, papers)
