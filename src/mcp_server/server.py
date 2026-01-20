from mcp.server import Server
from mcp.server.stdio import stdio_server

# Register tools
from src.mcp_server.tools.search_arxiv import search_arxiv_tool
from src.mcp_server.tools.search_semantic_scholar import search_semantic_scholar_tool
from src.mcp_server.tools.search_duckduckgo import search_duckduckgo_tool
from src.mcp_server.tools.dedup import deduplicate_records_tool
from src.mcp_server.tools.ranking import rank_discovery_records_tool
from src.mcp_server.tools.synthesis import synthesize_from_abstracts_tool
from src.mcp_server.tools.evaluation import evaluate_synthesis_tool


server = Server(name="ai-scientist-mcp")

# Register all tools
server.register_tool(search_arxiv_tool)
server.register_tool(search_semantic_scholar_tool)
server.register_tool(search_duckduckgo_tool)
server.register_tool(deduplicate_records_tool)
server.register_tool(rank_discovery_records_tool)
server.register_tool(synthesize_from_abstracts_tool)
server.register_tool(evaluate_synthesis_tool)


def main():
    stdio_server(server)


if __name__ == "__main__":
    main()
