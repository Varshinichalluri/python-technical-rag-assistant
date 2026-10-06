from langchain_huggingface import HuggingFaceEmbeddings


def create_embeddings():
    """
    Create the Hugging Face embedding model.
    """

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Embedding model loaded successfully!")

    return embeddings


if __name__ == "__main__":
    embeddings = create_embeddings()

    test_text = "Python is a programming language."

    vector = embeddings.embed_query(test_text)

    print(f"Embedding vector length: {len(vector)}")
    print("Embedding test completed successfully!")