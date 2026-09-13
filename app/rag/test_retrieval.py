from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings


VECTOR_STORE_DIR = "knowledge/faiss_index"


def main() -> None:
    load_dotenv()

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vector_store = FAISS.load_local(
        VECTOR_STORE_DIR,
        embeddings,
        allow_dangerous_deserialization=True,
    )

    query = (
        "What should be considered when migrating "
        "Azure Data Factory workloads to Microsoft Fabric?"
    )

    print("=" * 70)
    print(f"Query: {query}")
    print("=" * 70)

    results = vector_store.similarity_search(
        query,
        k=3,
    )

    for index, document in enumerate(results, start=1):
        print(f"\nRESULT {index}")
        print("-" * 70)
        print(f"Source: {document.metadata.get('source_file')}")
        print()
        print(document.page_content[:1000])


if __name__ == "__main__":
    main()