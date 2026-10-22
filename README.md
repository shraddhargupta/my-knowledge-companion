# My Knowledge Companion

**Your knowledge, connected and ready to use.**

My Knowledge Companion is a personal AI-powered learning assistant designed to make the technical knowledge we collect over time easier to revisit, explore, and apply.

Over the years, we accumulate notes, documentation, tutorials, and useful reference links across different places. This project brings that knowledge closer together, allowing me to ask questions and explore technical concepts using my own resources.

The goal is simple: **spend less time searching for information and more time understanding it.**

## Why I Built This

I wanted to build something useful for my own learning rather than just follow another AI tutorial.

While organizing years of technical notes and reference material, I realized how much useful information gets scattered across folders, documents, and bookmarks.

That became the starting point for My Knowledge Companion: a hands-on project to explore retrieval-augmented generation (RAG), local LLMs, and eventually agentic workflows.

## What It Does

- **Learn from personal resources** — ask questions about technical concepts using your own knowledge base.
- **Retrieve relevant information** — use keyword-based retrieval to find useful passages from local Markdown notes.
- **Explore ideas conversationally** — interact through a Streamlit chat interface.
- **Run a local LLM** — use Ollama to connect to a locally running language model.
- **Build incrementally** — extend the project as new learning needs and AI capabilities emerge.

The quality of answers depends on the content available in the knowledge base and whether relevant information is retrieved.

## How It Works

The current implementation follows a basic retrieval-augmented workflow:

1. **Knowledge sources:** Technical notes are stored locally in Markdown files.
2. **Retrieval:** LangChain's BM25 retriever searches the notes for relevant content.
3. **Agent and model interaction:** The application connects the user's question to the configured agent workflow and local language model.
4. **Response:** The application presents the generated response in a Streamlit interface.

```text
Your Question
     |
     v
Streamlit Chat Interface
     |
     v
Agent / Retrieval Workflow
     |
     v
BM25 Search over Local Notes
     |
     v
Relevant Context + Language Model
     |
     v
Generated Response
```

The retrieval and agent implementation determine how retrieved context is passed to the model. Grounded answers depend on that context being used correctly.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | User interface |
| LangChain | Retrieval components |
| BM25 | Keyword-based document retrieval |
| Ollama | Local language model inference |
| Markdown | Personal knowledge storage |

## Getting Started

### Prerequisites

- Python installed on your machine
- [Ollama](https://ollama.com/) installed and running
- A language model downloaded through Ollama
- Git and a terminal

### 1. Clone the repository

```bash
git clone https://github.com/shraddhargupta/interview-prep-helper.git
cd interview-prep-helper
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Ollama

Download a model suitable for your machine and start Ollama. For example, if you have already downloaded `qwen2.5-coder:3b`:

```bash
ollama run qwen2.5-coder:3b
```

Make sure the model name matches the one configured in your application.

### 5. Configure the Streamlit theme

Create `.streamlit/config.toml` in the project root:

```toml
[theme]
primaryColor = "#58765F"
backgroundColor = "#F7F6F2"
secondaryBackgroundColor = "#ECEFE8"
textColor = "#24372D"
font = "sans serif"
```

### 6. Run the application

```bash
streamlit run app.py
```

Streamlit will display a local URL in your terminal. Open it in your browser to start exploring.

## Adding Your Own Knowledge

Add technical notes and learning material to the local knowledge directory configured by the application.

Markdown files are a practical starting point because they are easy to create, edit, organize, and version-control.

For useful results:

- Keep notes focused on specific topics.
- Include definitions, examples, explanations, and links to trusted sources.
- Organize related concepts into separate files.
- Test questions against the actual content of your knowledge base.

External URLs recorded in notes or source lists are not automatically fetched unless URL ingestion has been implemented.

## Current Scope

This is an evolving personal project. The current focus is understanding the fundamentals of retrieval, local model integration, and the relationship between retrieved context and generated answers.

It should not be assumed that every response is fully grounded in personal sources; retrieval quality and context usage need to be tested.

## What's Next

Planned directions include:

- Improving retrieval quality and answer grounding.
- Making source references visible so answers can be verified.
- Expanding the knowledge base to support additional trusted resources.
- Exploring agentic RAG, where an agent can decide how to retrieve information and what steps to take.
- Evaluating answer relevance, faithfulness, and reliability.
- Exploring learning workflows that connect technical concepts and support continuous upskilling.

These are directions for further development, not claims about features already completed.

## The Bigger Idea

My Knowledge Companion is more than a chatbot. It is a practical way to experiment with AI while building something useful for everyday learning.

The longer-term vision is to turn accumulated knowledge into something searchable, connected, and actionable — a personal resource that grows alongside what I learn.

---

**Built as a hands-on exploration of Python, RAG, local LLMs, and AI application development.**
