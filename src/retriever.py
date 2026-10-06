from langchain_chroma import Chroma

from src.embeddings import create_embeddings


def create_retriever():
    """
    Load the existing ChromaDB vector store
    and create an MMR-based retriever.
    """

    embeddings = create_embeddings()

    vector_store = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )

    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 8,
            "fetch_k": 30,
            "lambda_mult": 0.6
        }
    )

    print("MMR retriever created successfully!")

    return retriever


if __name__ == "__main__":

    retriever = create_retriever()

    query = "What are the differences between a Python list and a tuple?"

    results = retriever.invoke(query)

    print(f"\nQuery: {query}")
    print(f"Retrieved documents: {len(results)}")

    for i, doc in enumerate(results, start=1):

        print(f"\n--- Result {i} ---")

        print(doc.page_content[:700])

        print("Source:", doc.metadata.get("source"))

        print("Page:", doc.metadata.get("page"))