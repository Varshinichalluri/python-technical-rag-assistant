import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from src.retriever import create_retriever


# Load environment variables from .env
load_dotenv()


def create_rag_pipeline():
    """
    Create the RAG pipeline using
    the retriever and Groq LLM.
    """

    # Get Groq API key from .env
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found. "
            "Please check your .env file."
        )

    # Create retriever
    retriever = create_retriever()

    # Create Groq LLM
    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0
    )

    print("RAG pipeline created successfully!")

    return retriever, llm


if __name__ == "__main__":

    # Create retriever and LLM
    retriever, llm = create_rag_pipeline()

    # User question
    query = "What is Python?"

    # Retrieve relevant documents
    documents = retriever.invoke(query)

    # Combine retrieved documents into context
    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    # Create RAG prompt
    prompt = f"""
You are a helpful technical documentation assistant.

Answer the user's question using ONLY the
provided context.

If the answer is not available in the context,
say that you could not find the answer in the
provided documentation.

Do not use outside knowledge.

Context:
{context}

Question:
{query}

Answer:
"""

    # Generate answer using the LLM
    response = llm.invoke(prompt)

    # Display question
    print("\nQuestion:")
    print(query)

    # Display answer
    print("\nAnswer:")
    print(response.content)

    # Display sources
    print("\nSources:")

    for i, document in enumerate(documents, start=1):

        source = document.metadata.get(
            "source",
            "Unknown"
        )

        page = document.metadata.get("page")

        # PDF page numbers in metadata are zero-indexed,
        # so add 1 for the user-facing page number.
        if page is not None:
            page = page + 1

        print(
            f"{i}. {source} | Page: {page}"
        )