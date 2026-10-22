
import re
from difflib import SequenceMatcher
from pathlib import Path

from langchain_core.documents import Document
from langchain_community.retrievers import BM25Retriever
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)
from smolagents import Tool


DATA_DIR = Path(__file__).parent / "data" / "notes"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
TOP_K = 3
MIN_QUERY_COVERAGE = 0.20
NEAR_DUPLICATE_THRESHOLD = 0.90




def normalize(text: str) -> str:
    """Normalize text for comparison."""
    return re.sub(r"\s+", " ", text.lower()).strip()


def tokenize(text: str) -> set[str]:
    """Extract simple word tokens, excluding common stop words."""
    stop_words = {
        "a", "an", "and", "are", "as", "at", "be", "by",
        "for", "from", "how", "i", "in", "is", "it", "of",
        "on", "or", "the", "to", "what", "when", "where",
        "which", "why", "with", "do", "does", "my",
    }

    words = set(re.findall(r"\b[a-zA-Z0-9_+#.-]+\b", text.lower()))
    return {word for word in words if word not in stop_words}




def load_documents() -> list[Document]:
    documents = []

    for file_path in DATA_DIR.glob("*.md"):
        content = file_path.read_text(encoding="utf-8")

        if not content.strip():
            continue

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "source": str(file_path),
                    "title": file_path.stem,
                    "source_type": "personal_note",
                },
            )
        )

    if not documents:
        raise ValueError(f"No Markdown files found in {DATA_DIR}")

    return documents


def split_documents(
    documents: list[Document],
) -> list[Document]:
    # First split by Markdown headings to preserve section boundaries.
    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "h1"),
            ("##", "h2"),
            ("###", "h3"),
        ],
        strip_headers=False,
    )

    # Then split long sections into manageable chunks.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        add_start_index=True,
    )

    chunks = []

    for document in documents:
        sections = header_splitter.split_text(
            document.page_content
        )

        for section in sections:
            # Preserve the original document metadata.
            section.metadata.update(document.metadata)

            for chunk in text_splitter.split_documents([section]):
                content = chunk.page_content.strip()

               

                chunk.page_content = content
                chunks.append(chunk)

    return chunks


def deduplicate_documents(
    documents: list[Document],
) -> list[Document]:
    """Remove exact and highly similar duplicate passages."""
    unique = []

    for document in documents:
        current = normalize(document.page_content)

        if not current:
            continue

        duplicate = False

        for existing in unique:
            previous = normalize(existing.page_content)

            # Exact duplicate.
            if current == previous:
                duplicate = True
                break

            # Near duplicate; compare only chunks from the same source.
            same_source = (
                document.metadata.get("source")
                == existing.metadata.get("source")
            )

            if same_source and SequenceMatcher(
                None, current, previous
            ).ratio() >= NEAR_DUPLICATE_THRESHOLD:
                duplicate = True
                break

        if not duplicate:
            unique.append(document)

    return unique


def build_retriever(
    chunks: list[Document],
) -> BM25Retriever:
    if not chunks:
        raise ValueError("No usable chunks found in the notes.")

    return BM25Retriever.from_documents(chunks, k=TOP_K)


def search_documents(
    retriever: BM25Retriever,
    query: str,
    top_k: int = TOP_K,
) -> list[tuple[Document, float, float]]:
    """Rank chunks, filter weak matches, and remove duplicate results."""
    

    query_tokens = set(retriever.preprocess_func(query))
    if not query_tokens:
        return []

    # Use the same tokenizer as the BM25 retriever.
    query_terms = retriever.preprocess_func(query)
    scores = retriever.vectorizer.get_scores(query_terms)

    ranked = sorted(
        zip(retriever.docs, scores),
        key=lambda item: item[1],
        reverse=True,
    )

    results = []

    for document, score in ranked:
        document_tokens = tokenize(document.page_content)

        coverage = (
            len(query_tokens & document_tokens) / len(query_tokens)
        )

        # These are initial heuristics, not calibrated confidence scores.
        if score <= 0 or coverage < MIN_QUERY_COVERAGE:
            continue

        # Avoid returning multiple near-identical passages.
        duplicate = any(
            normalize(document.page_content)
            == normalize(existing.page_content)
            or SequenceMatcher(
                None,
                normalize(document.page_content),
                normalize(existing.page_content),
            ).ratio() >= NEAR_DUPLICATE_THRESHOLD
            for existing, _, _ in results
            if document.metadata.get("source")
            == existing.metadata.get("source")
        )

        if duplicate:
            continue

        results.append((document, float(score), coverage))

        if len(results) >= top_k:
            break

    return results


class KnowledgeBaseSearchTool(Tool):
    name = "knowledge_base_search"

    description = (
        "Search curated technical notes. Returns relevant passages "
        "with retrieval scores. If no relevant passages are found, "
        "reports that the knowledge base lacks sufficient evidence."
    )

    inputs = {
        "query": {
            "type": "string",
            "description": "Question or topic to search for.",
        }
    }

    output_type = "string"

    def __init__(self):
        super().__init__()

        documents = load_documents()
        chunks = split_documents(documents)
        chunks = deduplicate_documents(chunks)

        self.retriever = build_retriever(chunks)
        self.is_initialized = True

    def forward(self, query: str) -> str:
        results = search_documents(self.retriever, query)

        if not results:
            return (
                "No sufficiently relevant passages were found. "
                "Try a more specific query or add supporting notes."
            )

        passages = []

        for index, (doc, score, coverage) in enumerate(
            results, start=1
        ):
            passages.append(
                f"Passage {index}\n"
                f"Source: {doc.metadata.get('source', 'Unknown')}\n"
                f"Title: {doc.metadata.get('title', 'Unknown')}\n"
                f"BM25 score: {score:.3f}\n"
                f"Query-term coverage: {coverage:.0%}\n"
                f"Content:\n{doc.page_content}"
            )

        return "\n\n---\n\n".join(passages)


if __name__ == "__main__":
    documents = load_documents()
    chunks = split_documents(documents)
    chunks = deduplicate_documents(chunks)

    print(f"Notes loaded: {len(documents)}")
    print(f"Chunks after filtering: {len(chunks)}")

    retriever = build_retriever(chunks)
    query = input("\nWhat do you want to learn? ")

    results = search_documents(retriever, query)

    if not results:
        print("\nNo sufficiently relevant passages found.")
    else:
        for index, (doc, score, coverage) in enumerate(
            results, start=1
        ):
            print(f"\n--- Result {index} ---")
            print(f"BM25 score: {score:.3f}")
            print(f"Query-term coverage: {coverage:.0%}")
            print(f"Source: {doc.metadata['source']}")
            print(doc.page_content)
