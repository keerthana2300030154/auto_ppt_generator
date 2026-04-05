import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types
import httpx

app = Server("search-server")

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="search_topic",
            description="Searches DuckDuckGo for facts about a topic. Returns a short text summary.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query string"}
                },
                "required": ["query"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "search_topic":
        query = arguments["query"]
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    "https://api.duckduckgo.com/",
                    params={"q": query, "format": "json", "no_html": 1, "skip_disambig": 1}
                )
                data = resp.json()
                abstract = data.get("AbstractText", "")
                related = " | ".join([r.get("Text", "") for r in data.get("RelatedTopics", [])[:3]])
                result = abstract or related or "No data found — agent should use own knowledge."
                return [types.TextContent(type="text", text=result[:800])]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Search failed: {e}. Use your own knowledge.")]

async def main():
    async with stdio_server() as (r, w):
        await app.run(r, w, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())