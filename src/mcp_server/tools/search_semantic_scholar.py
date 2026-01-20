from mcp.server import tool
from src.tools.search_semantic_scholar import search_semantic_scholar


@tool(
    name="search_semantic_scholar",
    description="Search Semantic Scholar for research papers"
)
def search_semantic_scholar_tool(query: str, max_results: int = 10):
    try:
        return search_semantic_scholar(query, max_results)
    except Exception as e:
        # Fail gracefully (rate limits, network issues)
        print(f"[MCP] Semantic Scholar error: {e}")
        return []
