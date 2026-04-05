from agent_ppt import PPTAgent

if __name__ == "__main__":
    topic = input("Enter your topic: ")
    agent = PPTAgent()
    agent.run(topic)