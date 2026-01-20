from mcp.server import tool
from src.tools.search_arxiv import search_arxiv


@tool(
    name="search_arxiv",
    description="Search arXiv for research papers"
)
def search_arxiv_tool(query: str, max_results: int = 10):
    return search_arxiv(query, max_results)
