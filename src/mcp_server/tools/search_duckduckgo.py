from mcp.server import tool
from src.tools.search_duckduckgo import search_duckduckgo


@tool(
    name="search_duckduckgo",
    description="Search DuckDuckGo for blogs and web articles"
)
def search_duckduckgo_tool(query: str, max_results: int = 10):
    return search_duckduckgo(query, max_results)
