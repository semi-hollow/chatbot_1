"""最小 MCP Client 模块（mcp）。主 Agent 通过该模块访问 tool/resource/prompt。"""
from typing import Any

from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


class MCPClient:
    def __init__(self, command: str) -> None:
        parts = command.split()
        self.params = StdioServerParameters(command=parts[0], args=parts[1:])

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        async with stdio_client(self.params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(name, arguments)
                if hasattr(result, "content") and result.content:
                    return result.content[0].text
                return str(result)

    async def read_resource(self, uri: str) -> str:
        async with stdio_client(self.params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.read_resource(uri)
                return result.contents[0].text

    async def get_prompt(self, name: str, arguments: dict[str, Any]) -> str:
        async with stdio_client(self.params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.get_prompt(name, arguments)
                return result.messages[0].content.text
