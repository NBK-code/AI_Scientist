from mcp.client import Client


class MCPClient:
    def __init__(self):
        self.client = Client(
            command=[
                "python",
                "-m",
                "src.mcp_server.server",
            ]
        )

    def call_tool(self, tool_name: str, args: dict):
        return self.client.call_tool(tool_name, args)


# Singleton-style client
mcp = MCPClient()
