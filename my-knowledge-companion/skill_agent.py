from smolagents import CodeAgent, OpenAIModel
from retriever import KnowledgeBaseSearchTool
def create_agent():
    knowledge_tool = KnowledgeBaseSearchTool()

    model = OpenAIModel(
        model_id="qwen2.5-coder:3b",
        api_base="http://localhost:11434/v1",
        api_key="ollama",
    )

    agent = CodeAgent(
        tools=[knowledge_tool],
        model=model,
        max_steps=4,
        verbosity_level=0,
        instructions="""
        You are SkillPilot, a personal technical learning assistant.

        Use knowledge_base_search for relevant technical questions.
        Use retrieved passages as evidence.
        If the notes lack sufficient evidence, say so clearly.
        Do not invent unavailable tools or pretend a search succeeded.
        """,
    )

    return agent
