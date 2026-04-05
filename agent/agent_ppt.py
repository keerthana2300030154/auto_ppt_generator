import asyncio
import json
import os
import re
import sys
from datetime import datetime
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import OpenAI

load_dotenv()

# ── Groq client ───────────────────────────────────────────────────────────────
grok = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

GROK_MODEL = "llama-3.3-70b-versatile"

# ── Helpers ──────────────────────────────────────────────────────────────────

def call_grok(messages: list[dict], json_mode: bool = False) -> str:
    """Single call to Groq. Returns text content."""
    kwargs = {"model": GROK_MODEL, "messages": messages, "max_tokens": 2000}
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    response = grok.chat.completions.create(**kwargs)
    return response.choices[0].message.content.strip()


def extract_json(text: str) -> dict | list:
    """Safely extract JSON even if wrapped in markdown fences."""
    text = re.sub(r"```json|```", "", text).strip()
    return json.loads(text)


# ── Step 1: Planning ──────────────────────────────────────────────────────────

def plan_presentation(user_request: str) -> dict:
    """Ask Groq to produce a full slide plan as JSON."""
    print("\n🧠 [AGENT] Planning slide structure...")
    messages = [
        {
            "role": "system",
            "content": (
                "You are a presentation planning expert. "
                "Given a user's presentation request, output ONLY valid JSON with this schema:\n"
                "{\n"
                '  "title": "Presentation title",\n'
                '  "audience": "Target audience",\n'
                '  "slides": [\n'
                '    {"slide_number": 1, "title": "...", "bullets": ["...", "...", "..."], "is_title_slide": true},\n'
                '    {"slide_number": 2, "title": "...", "bullets": ["...", "...", "...", "..."], "is_title_slide": false}\n'
                '  ]\n'
                "}\n"
                "Rules: 1st slide is always title/cover. Last slide is 'Summary' or 'Key Takeaways'. "
                "Each non-title slide has 3-5 bullets. Output ONLY JSON, no commentary."
            )
        },
        {"role": "user", "content": user_request}
    ]
    raw = call_grok(messages, json_mode=True)
    plan = extract_json(raw)
    print(f"   ✅ Plan ready: {len(plan['slides'])} slides — '{plan['title']}'")
    return plan


# ── Step 2: Enrich with search data ──────────────────────────────────────────

async def enrich_slide(session: ClientSession, slide: dict, context_text: str) -> dict:
    """Optionally enrich a slide's bullets using web search + Groq refinement."""
    title = slide["title"]
    print(f"   🔍 Enriching: '{title}'")

    # Call search MCP tool
    search_result = await session.call_tool("search_topic", {"query": title})
    search_text = search_result.content[0].text if search_result.content else ""

    if "No data" in search_text or "failed" in search_text.lower():
        return slide  # Keep Groq's original bullets

    # Ask Groq to refine bullets using search data
    messages = [
        {
            "role": "system",
            "content": (
                "You improve slide bullet points using web search data. "
                "Output ONLY a JSON array of 3-5 improved bullet strings. "
                "Keep bullets short (max 12 words each). Audience: " + context_text
            )
        },
        {
            "role": "user",
            "content": (
                f"Slide title: {title}\n"
                f"Current bullets: {json.dumps(slide['bullets'])}\n"
                f"Search data: {search_text}\n"
                "Output improved bullets as a JSON array."
            )
        }
    ]
    raw = call_grok(messages, json_mode=False)
    try:
        improved = extract_json(raw)
        if isinstance(improved, list) and improved:
            slide["bullets"] = improved[:5]
    except Exception:
        pass  # gracefully fall back to original bullets

    return slide


# ── Step 3: Agentic loop ──────────────────────────────────────────────────────

async def run_agent(user_request: str):
    print(f"\n🚀 Auto-PPT Agent started")
    print(f"   Request: {user_request}\n")

    # ── Phase 1: Plan ────────────────────────────────────────────────────────
    try:
        plan = plan_presentation(user_request)
    except Exception as e:
        print(f"❌ Planning failed: {e}")
        sys.exit(1)

    output_filename = f"output/presentation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx"

    # ── Phase 2: Connect to MCP servers ─────────────────────────────────────
    pptx_params = StdioServerParameters(
        command="python",
        args=["mcp_servers/pptx_server.py"]
    )
    search_params = StdioServerParameters(
        command="python",
        args=["mcp_servers/search_server.py"]
    )

    async with stdio_client(pptx_params) as (pr, pw):
        async with ClientSession(pr, pw) as pptx_session:
            await pptx_session.initialize()

            async with stdio_client(search_params) as (sr, sw):
                async with ClientSession(sr, sw) as search_session:
                    await search_session.initialize()

                    # ── Phase 3: Create presentation file ────────────────────
                    print("\n📂 [TOOL] create_presentation")
                    await pptx_session.call_tool(
                        "create_presentation",
                        {"output_path": output_filename}
                    )

                    # ── Phase 4: Enrich & add each slide ─────────────────────
                    audience = plan.get("audience", "general audience")
                    for slide_data in plan["slides"]:
                        snum = slide_data["slide_number"]

                        # Skip search enrichment for title/summary slides
                        if not slide_data.get("is_title_slide") and snum < len(plan["slides"]):
                            slide_data = await enrich_slide(
                                search_session, slide_data, audience
                            )

                        print(f"\n📊 [TOOL] add_slide #{snum}: '{slide_data['title']}'")
                        result = await pptx_session.call_tool("add_slide", {
                            "title": slide_data["title"],
                            "bullets": slide_data.get("bullets", []),
                            "slide_number": snum,
                            "is_title_slide": slide_data.get("is_title_slide", False)
                        })
                        print(f"   → {result.content[0].text}")

                    # ── Phase 5: Save ─────────────────────────────────────────
                    print("\n💾 [TOOL] save_presentation")
                    save_result = await pptx_session.call_tool("save_presentation", {})
                    print(f"   → {save_result.content[0].text}")

    print(f"\n✅ Done! File saved: {output_filename}")
    return output_filename


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python agent/agent_ppt.py \"Your presentation prompt here\"")
        sys.exit(1)

    user_input = " ".join(sys.argv[1:])
    asyncio.run(run_agent(user_input))