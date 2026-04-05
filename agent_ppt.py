from mcp_servers.ppt_server import PPTServer
from mcp_servers.search_server import search_topic
from utils.planner import plan_slides
from utils.grok_api import generate_grok_content


class PPTAgent:

    def __init__(self):
        self.ppt = PPTServer()

    def generate_content(self, title, topic=None):

        content = generate_grok_content(title, topic)

        if content:
            print(f"✅ Using Grok for: {title}")
            return content

        print("⚠️ Using fallback content...")

        if title.strip().lower() == "conclusion" and topic:
            return search_topic(f"Conclusion of {topic}")

        return search_topic(title)

    def run(self, topic):

        print("Planning slides...")
        slides = plan_slides(topic)

        print("Slide Plan:", slides)

        print("Creating PPT...")
        self.ppt.create_presentation("output.pptx")
        self.ppt.add_title_slide(topic, "Generated using AI Agent")

        for slide in slides:
            print(f"Thought: Create slide '{slide}'")

            content = self.generate_content(slide, topic)

            print(f"Action: add_slide('{slide}')")
            self.ppt.add_slide(slide, content)

        print("Saving file...")
        self.ppt.save()

        print("🎉 PPT Generated Successfully!")