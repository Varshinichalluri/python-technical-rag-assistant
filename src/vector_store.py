from document_loader import load_documents
from text_splitter import split_documents
from embeddings import create_embeddings
from langchain_chroma import Chroma


def create_vector_store():
    """
    Create and persist the ChromaDB vector store.
    """

    print("Loading documents...")

    documents = load_documents()

    print("\nSplitting documents into chunks...")

    chunks = split_documents(documents)

    print(f"\nTotal chunks: {len(chunks)}")

    print("\nCreating embedding model...")

    embeddings = create_embeddings()

    print("\nCreating ChromaDB vector store...")

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="chroma_db"
    )

    print("\nVector store created successfully!")
    print("ChromaDB location: chroma_db")

    return vector_store


if __name__ == "__main__":
    create_vector_store()