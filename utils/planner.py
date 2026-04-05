from utils.grok_api import plan_slides_with_grok

def plan_slides(topic):
    slides = plan_slides_with_grok(topic)

    if slides:
        return slides

    print("⚠️ Using fallback planning...")

    return [
        f"Introduction to {topic}",
        f"Key Concepts of {topic}",
        f"Process or Working of {topic}",
        f"Applications of {topic}",
        "Conclusion"
    ]