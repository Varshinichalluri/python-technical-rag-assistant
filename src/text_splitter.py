from document_loader import load_documents
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents):
    """
    Split loaded documents into smaller chunks.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(documents)

    print(f"Total chunks created: {len(chunks)}")

    return chunks


if __name__ == "__main__":
    documents = load_documents()

    chunks = split_documents(documents)

    print("\nText splitting completed successfully!")

    if chunks:
        print("\nFirst chunk preview:")
        print(chunks[0].page_content[:1000])

        print("\nFirst chunk metadata:")
        print(chunks[0].metadata)