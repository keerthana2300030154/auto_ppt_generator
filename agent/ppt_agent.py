from mcp_servers.ppt_server import PPTServer
from mcp_servers.search_server import search_topic
from utils.planner import plan_slides

class PPTAgent:

    def __init__(self):
        self.ppt = PPTServer()

    def generate_content(self, title, topic=None):
        if title.strip().lower() == "conclusion" and topic:
            return search_topic(f"Conclusion of {topic}")
        return search_topic(title)

    def run(self, topic):

        print("Planning slides...")

        slides = plan_slides(topic)

        print("Creating PPT...")
        self.ppt.create_presentation("output.pptx")
        self.ppt.add_title_slide(topic, "Professional presentation generated locally")

        for slide in slides:
            print(f"Thought: Create slide '{slide}'")
            content = self.generate_content(slide, topic)

            print(f"Action: add_slide('{slide}')")
            self.ppt.add_slide(slide, content)

        print("Saving file...")
        self.ppt.save()

        print("Done!")
