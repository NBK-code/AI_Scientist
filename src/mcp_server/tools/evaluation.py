from mcp.server import tool
from src.agents.evaluator import evaluate_synthesis
from src.schemas import DiscoveryRecord
from typing import List, Dict


@tool(
    name="evaluate_synthesis",
    description="Evaluate the quality of a synthesized literature review"
)
def evaluate_synthesis_tool(
    topic: str,
    synthesis_markdown: str,
    papers: List[DiscoveryRecord]
) -> Dict:
    return evaluate_synthesis(topic, synthesis_markdown, papers)
