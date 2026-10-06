import streamlit as st

from src.rag_pipeline import create_rag_pipeline


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Python Technical Assistant",
    page_icon="🐍",
    layout="wide"
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🐍 Python Assistant")

    st.markdown(
        """
        ### About

        An AI-powered technical documentation
        assistant built using **RAG**.

        It answers questions using the
        official Python documentation stored
        in the project's knowledge base.
        """
    )

    st.divider()

    st.subheader("🧠 Technology Stack")

    st.markdown(
        """
        - Python
        - LangChain
        - ChromaDB
        - HuggingFace Embeddings
        - Groq LLM
        - Streamlit
        """
    )

    st.divider()

    st.subheader("📚 Knowledge Base")

    st.write(
        "Python 3.11 official documentation"
    )

    st.divider()

    st.subheader("🔄 RAG Workflow")

    st.markdown(
        """
        **Question**
        ↓

        **Query Rewriting**
        ↓

        **Vector Retrieval**
        ↓

        **Relevant Context**
        ↓

        **Groq LLM**
        ↓

        **Grounded Answer**
        """
    )

    st.divider()

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


# =========================================================
# MAIN TITLE
# =========================================================

st.title(
    "🤖 Python Technical Documentation Assistant"
)

st.write(
    "Ask questions about Python using the official "
    "Python documentation stored in the knowledge base."
)


# =========================================================
# LOAD RAG PIPELINE
# =========================================================

@st.cache_resource
def load_rag_pipeline():

    retriever, llm = create_rag_pipeline()

    return retriever, llm


try:

    retriever, llm = load_rag_pipeline()

except Exception:

    st.error(
        "⚠️ The AI system could not be loaded. "
        "Please check the configuration and try again."
    )

    st.stop()


# =========================================================
# INITIALIZE CHAT HISTORY
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# =========================================================
# EXAMPLE QUESTIONS
# =========================================================

if not st.session_state.messages:

    st.markdown("### 💡 Try asking")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            "**What is a Python list?**"
        )

    with col2:

        st.info(
            "**What is the difference "
            "between a list and tuple?**"
        )

    with col3:

        st.info(
            "**What are Python exceptions?**"
        )


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )

        if message["role"] == "assistant":

            sources = message.get(
                "sources",
                []
            )

            if sources:

                with st.expander(
                    "📚 Sources"
                ):

                    for i, source in enumerate(
                        sources,
                        start=1
                    ):

                        st.write(
                            f"{i}. {source}"
                        )


# =========================================================
# CHAT INPUT
# =========================================================

question = st.chat_input(
    "Ask a question about Python..."
)


# =========================================================
# PROCESS QUESTION
# =========================================================

if question:

    # -----------------------------------------------------
    # USER MESSAGE
    # -----------------------------------------------------

    with st.chat_message("user"):

        st.markdown(question)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    # -----------------------------------------------------
    # CONVERSATION HISTORY
    # -----------------------------------------------------

    conversation_history = ""

    for message in st.session_state.messages[:-1]:

        role = message["role"]

        content = message["content"]

        conversation_history += (
            f"{role.upper()}: {content}\n"
        )


    # -----------------------------------------------------
    # HISTORY-AWARE QUERY REWRITING
    # -----------------------------------------------------

    search_query = question


    if conversation_history.strip():

        rewrite_prompt = f"""
You are a query rewriting assistant.

Your task is to rewrite the user's latest
question into a standalone question that
can be searched in a technical documentation
knowledge base.

Use the conversation history only to resolve
references such as:

- it
- they
- this
- that
- the above
- the previous concept

Do not answer the question.

Return ONLY the rewritten standalone question.

Conversation History:
{conversation_history}

Latest User Question:
{question}

Standalone Search Question:
"""

        try:

            rewritten_query_response = llm.invoke(
                rewrite_prompt
            )

            search_query = (
                rewritten_query_response
                .content
                .strip()
            )

        except Exception:

            search_query = question


    # -----------------------------------------------------
    # ASSISTANT RESPONSE
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        try:

            with st.spinner(
                "🔎 Searching the Python documentation..."
            ):

                # -----------------------------------------
                # RETRIEVE DOCUMENTS
                # -----------------------------------------

                documents = retriever.invoke(
                    search_query
                )


                # -----------------------------------------
                # CHECK RETRIEVAL
                # -----------------------------------------

                if not documents:

                    answer = (
                        "I could not find relevant "
                        "information in the provided "
                        "Python documentation."
                    )

                    sources = []


                else:

                    # -------------------------------------
                    # BUILD CONTEXT
                    # -------------------------------------

                    context = "\n\n".join(
                        document.page_content
                        for document in documents
                    )


                    # -------------------------------------
                    # RAG PROMPT
                    # -------------------------------------

                    prompt = f"""
You are a helpful Python technical
documentation assistant.

Use the provided documentation context
to answer the user's question.

You may use the conversation history to
understand what the user is referring to.

Answer using ONLY information supported
by the provided documentation.

Do not invent information.

If the answer cannot be found in the
provided documentation, say:

"I could not find this information in
the provided Python documentation."

Keep the answer clear, accurate and useful.

When comparing concepts, use a markdown
table if it improves clarity.

Conversation History:
{conversation_history}

Documentation Context:
{context}

Current Question:
{question}

Answer:
"""


                    # -------------------------------------
                    # CALL LLM
                    # -------------------------------------

                    response = llm.invoke(
                        prompt
                    )

                    answer = response.content
                    answer = (
    answer
    .replace("<br>", "\n")
    .replace("<br/>", "\n")
    .replace("<br />", "\n")
)

                    # -------------------------------------
                    # HANDLE RESPONSE FORMAT
                    # -------------------------------------

                    if isinstance(
                        answer,
                        list
                    ):

                        text_parts = []

                        for item in answer:

                            if isinstance(
                                item,
                                dict
                            ):

                                text = item.get(
                                    "text",
                                    ""
                                )

                                if text:

                                    text_parts.append(
                                        text
                                    )

                            else:

                                text_parts.append(
                                    str(item)
                                )

                        answer = "\n".join(
                            text_parts
                        )


                    # -------------------------------------
                    # EMPTY RESPONSE CHECK
                    # -------------------------------------

                    if (
                        not answer
                        or not answer.strip()
                    ):

                        answer = (
                            "I could not generate an "
                            "answer from the retrieved "
                            "Python documentation."
                        )


                    # -------------------------------------
                    # COLLECT SOURCES
                    # -------------------------------------

                    sources = []

                    for document in documents:

                        source = document.metadata.get(
                            "source",
                            "Unknown source"
                        )

                        page = document.metadata.get(
                            "page"
                        )


                        if page is not None:

                            page_number = page + 1

                            source_info = (
                                f"{source} — "
                                f"Page {page_number}"
                            )

                        else:

                            source_info = source


                        if source_info not in sources:

                            sources.append(
                                source_info
                            )


            # -------------------------------------------------
            # DISPLAY ANSWER
            # -------------------------------------------------

            st.markdown(answer)


            # -------------------------------------------------
            # DISPLAY SOURCES
            # -------------------------------------------------

            if sources:

                with st.expander(
                    "📚 Sources"
                ):

                    for i, source in enumerate(
                        sources,
                        start=1
                    ):

                        st.write(
                            f"{i}. {source}"
                        )


        except Exception as error:

            answer = (
                "⚠️ Sorry, I couldn't process "
                "your question right now. "
                "Please try again."
            )

            sources = []

            st.error(answer)

            print(
                "Error while processing question:",
                error
            )


    # -----------------------------------------------------
    # SAVE ASSISTANT MESSAGE
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources
        }
    )