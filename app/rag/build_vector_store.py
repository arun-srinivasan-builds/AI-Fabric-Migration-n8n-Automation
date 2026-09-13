from pathlib import Path

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


KNOWLEDGE_DIR = Path("knowledge/processed")
VECTOR_STORE_DIR = Path("knowledge/faiss_index")


def load_documents() -> list[Document]:
    """
    Load all processed knowledge files as LangChain Documents.
    """
    documents = []

    for file_path in KNOWLEDGE_DIR.glob("*.txt"):
        content = file_path.read_text(encoding="utf-8")

        document = Document(
            page_content=content,
            metadata={
                "source_file": file_path.name,
            },
        )

        documents.append(document)

    return documents


def split_documents(documents: list[Document]) -> list[Document]:
    """
    Split documents into smaller overlapping chunks.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )

    chunks = splitter.split_documents(documents)

    return chunks


def build_vector_store(chunks: list[Document]) -> FAISS:
    """
    Convert chunks into embeddings and store them in FAISS.
    """
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )

    return vector_store


def main() -> None:
    load_dotenv()

    print("=" * 70)
    print("Loading processed knowledge documents...")

    documents = load_documents()

    print(f"Documents loaded: {len(documents)}")

    print("=" * 70)
    print("Splitting documents into chunks...")

    chunks = split_documents(documents)

    print(f"Chunks created: {len(chunks)}")

    print("=" * 70)
    print("Creating embeddings and FAISS vector store...")

    vector_store = build_vector_store(chunks)

    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

    vector_store.save_local(str(VECTOR_STORE_DIR))

    print("=" * 70)
    print("FAISS vector store created successfully.")
    print(f"Saved to: {VECTOR_STORE_DIR}")


if __name__ == "__main__":
    main()