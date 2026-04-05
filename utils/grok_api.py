import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("GROK_API_KEY"),
    base_url="https://api.x.ai/v1"
)

# -----------------------------
# CONTENT GENERATION (SAFE)
# -----------------------------
def generate_grok_content(title, topic=None):

    prompt = f"""
Create 4 bullet points for a PowerPoint slide.

Slide Title: {title}
Topic: {topic if topic else title}

Rules:
- Each point on new line
- No numbering
- Clear and professional
"""

    try:
        response = client.responses.create(
            model="grok-4.20-reasoning",
            input=prompt,
            max_output_tokens=200
        )

        return response.output[0].content[0].text.strip()

    except Exception as e:
        print("⚠️ Grok not available (no credits or access):", e)
        return None


# -----------------------------
# PLANNING (SAFE)
# -----------------------------
def plan_slides_with_grok(topic):

    prompt = f"""
Create 5 slide titles for a presentation on:
{topic}

Return only a Python list.
"""

    try:
        response = client.responses.create(
            model="grok-4.20-reasoning",
            input=prompt,
            max_output_tokens=200
        )

        return eval(response.output[0].content[0].text)

    except Exception as e:
        print("⚠️ Grok planning failed:", e)
        return None