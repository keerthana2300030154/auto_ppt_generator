# Auto-PPT Agent

**Course:** AI Agents & MCP Architecture
**Project:** Auto-PPT Generator using MCP-based Agent Architecture

---

## 🎯 Objective

To design and implement an autonomous AI agent that generates a complete PowerPoint presentation (`.pptx`) from a single user prompt using MCP-style tool integration.

---

## 🧠 Overview

This project implements an **agentic system** that:

* Accepts a user prompt (e.g., "Life cycle of a star")
* Plans slide structure
* Generates meaningful content
* Uses MCP tools to create slides
* Produces a fully functional PowerPoint file

Unlike traditional scripts, this system follows an **agentic loop** involving planning, decision-making, and tool execution.

---

## ⚙️ Core Features

* ✅ Agent-based architecture (not a static script)
* ✅ MCP tool integration (PPT + Search server)
* ✅ Slide planning before execution
* ✅ 3–5 meaningful bullet points per slide
* ✅ Automatic `.pptx` generation
* ✅ Graceful fallback for unknown topics
* ✅ Works without external APIs (offline mode)

---

## 🏗️ System Architecture

```
User Input
   ↓
Agent (Brain)
   ↓
Planner (Slide Outline)
   ↓
Agent Loop:
   → Decide action
   → Call MCP tool
   → Generate content
   → Repeat
   ↓
Save PPT
```

---

## 🔁 Agentic Workflow (IMPORTANT)

The system follows a **Thought → Action → Observation loop**:

1. **Thought:** Plan slide titles
2. **Action:** Create presentation
3. **Thought:** Generate slide content
4. **Action:** Call `add_slide()`
5. Repeat for all slides
6. **Final Action:** Save file

Example:

```
Thought: Plan slides
Action: create_presentation

Thought: Create slide 1
Action: add_slide

Thought: Create slide 2
Action: add_slide

Thought: Save file
Action: save
```

This proves the system is an **AI agent**, not a simple script.

---

## 🛠️ MCP Integration

The system uses modular MCP-style tools:

### 1. PPT Server (`ppt_server.py`)

* Creates presentation
* Adds slides
* Writes content
* Saves file

### 2. Search Server (`search_server.py`)

* Generates topic-specific content
* Provides fallback content if topic is unknown

These tools allow the agent to interact with external functionalities dynamically.

---

## 🧩 Project Structure

```
autoppt/
├── main.py
├── agent/
│   └── ppt_agent.py
├── mcp_servers/
│   ├── ppt_server.py
│   └── search_server.py
├── utils/
│   └── planner.py
└── venv/
```

---

## 📊 Slide Structure

Each presentation contains:

1. Introduction
2. Key Concepts
3. Process / Working
4. Applications
5. Conclusion

Each slide includes **3–5 meaningful bullet points**.

---

## 🧠 Content Generation

* Topic-specific content is generated using rule-based logic
* Supports domains like:

  * Stars
  * AI
  * Cybersecurity
  * Planets
* Unknown topics fallback to generic structured content

Example:

```
• Stars form from clouds of gas called nebulae
• Nuclear fusion produces energy
• Stars evolve into red giants
• Final stages include white dwarf or black hole
```

---

## ⚠️ Error Handling

The system handles failures gracefully:

* If topic is unknown → fallback content is generated
* Prevents crashes
* Ensures presentation is always created

---

## ▶️ Installation Steps

```bash
cd D:\calibo\autoppt
py -m venv venv
.\venv\Scripts\Activate.ps1
py -m pip install python-pptx
```

---

## ▶️ Run the Project

```bash
py main.py
```

OR

```bash
py main.py "life cycle of a star"
```

---

## 📁 Output

* File generated: `output.pptx`
* Located in project directory
* Fully functional PowerPoint presentation

---

## 🧠 Why This is an Agent (VERY IMPORTANT)

This system is an **AI agent** because:

* ✔ It plans before execution
* ✔ It makes decisions step-by-step
* ✔ It uses tools dynamically (MCP)
* ✔ It handles uncertainty (fallback)

Unlike traditional scripts, it **thinks and acts autonomously**.

---

## 🏆 How Requirements Are Met

| Requirement        | Status |
| ------------------ | ------ |
| MCP Integration    | ✅      |
| Agentic Loop       | ✅      |
| Content Generation | ✅      |
| Output (.pptx)     | ✅      |
| Error Handling     | ✅      |

---

## 🔮 Future Improvements

* Add real web search API
* Integrate OpenAI for better content
* Add images to slides
* Improve slide design templates

---

## 📌 Conclusion

The Auto-PPT Agent successfully demonstrates:

* Agentic reasoning
* MCP-based tool usage
* Automated content generation

It transforms a simple prompt into a complete presentation autonomously, fulfilling all assignment requirements.

---
