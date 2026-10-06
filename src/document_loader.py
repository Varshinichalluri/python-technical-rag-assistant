from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


def load_documents(data_path="data/raw"):
    """
    Load all PDF documents from data/raw
    and its subfolders.
    """

    data_directory = Path(data_path)

    pdf_files = list(data_directory.rglob("*.pdf"))

    print(f"Found {len(pdf_files)} PDF files.")

    documents = []

    for pdf_file in pdf_files:
        print(f"Loading: {pdf_file.name}")

        loader = PyPDFLoader(str(pdf_file))
        pdf_documents = loader.load()

        documents.extend(pdf_documents)

    print(f"Total pages loaded: {len(documents)}")

    return documents


if __name__ == "__main__":
    documents = load_documents()

    print("\nDocument loading completed successfully!")

    if documents:
        print("\nFirst document preview:")
        print(documents[0].page_content[:1000])