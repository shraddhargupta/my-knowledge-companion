---
title: "Agentic RAG"
source_type: "personal_note"
topics:
- RAG
- AI agents
  trust_level: "personal"
---

# What is Agentic RAG?

Agentic RAG allows an agent to make decisions
about retrieval instead of following a fixed
retrieve-and-answer workflow.

## Key concepts

- Query rewriting
- Document relevance grading
- Conditional retrieval
- Grounded answer generation

## My understanding

[Add your own explanation here.]

## Questions to revisit

- When should the agent retrieve again?
- How do we evaluate retrieval quality?


## Example

Suppose a user asks, "How do I evaluate an AI agent?"

1. The agent searches the knowledge base.
2. It checks whether the retrieved passages cover agent evaluation.
3. If the evidence is insufficient, it rewrites the query and searches again.
4. It evaluates the new results.
5. It answers using the available evidence or explains what is missing.

## Difference from traditional RAG

Traditional RAG generally follows a predefined retrieval-and-answer pipeline.

Agentic RAG allows an agent to make decisions about retrieval, such as rewriting queries, assessing document relevance, or deciding whether another retrieval step is needed.

## Evaluation questions

- Did retrieval return relevant passages?
- Did the agent retrieve again when evidence was insufficient?
- Was the final answer supported by the retrieved evidence?
- Did the agent acknowledge missing information?
