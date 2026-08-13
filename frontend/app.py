import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/ask"


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="F1 Analytics Copilot",
    page_icon="🏎️",
    layout="wide",
)


# ==========================================
# HEADER
# ==========================================

st.title("🏎️ F1 Analytics Copilot")

st.caption(
    "Ask questions about Formula 1 statistics, history, "
    "and current information."
)


# ==========================================
# CHAT HISTORY
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ==========================================
# USER INPUT
# ==========================================

question = st.chat_input(
    "Ask anything about Formula 1..."
)


# ==========================================
# PROCESS QUESTION
# ==========================================

if question:

    # Display user message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # --------------------------------------
    # Call FastAPI
    # --------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = requests.post(
                    API_URL,
                    json={
                        "question": question
                    },
                    timeout=120,
                )

                response.raise_for_status()

                data = response.json()

                answer = data.get(
                    "answer",
                    "No answer was returned.",
                )

                st.markdown(answer)

                # ----------------------------------
                # Route information
                # ----------------------------------

                route = data.get("route")

                intent = data.get("intent")

                if route:

                    st.caption(
                        f"Route: `{route}` · "
                        f"Intent: `{intent}`"
                    )

                # ----------------------------------
                # Sources
                # ----------------------------------

                sources = data.get(
                    "sources",
                    []
                )

                if sources:

                    with st.expander("Sources"):

                        for source in sources:

                            title = source.get(
                                "title",
                                "Source"
                            )

                            url = source.get(
                                "url",
                                ""
                            )

                            snippet = source.get(
                                "snippet",
                                ""
                            )

                            st.markdown(
                                f"**[{title}]({url})**"
                            )

                            if snippet:
                                st.caption(snippet)

                # ----------------------------------
                # SQL
                # ----------------------------------

                sql = data.get("sql")

                if sql:

                    with st.expander(
                        "Generated SQL"
                    ):

                        st.code(
                            sql,
                            language="sql"
                        )

                # ----------------------------------
                # Store assistant response
                # ----------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )

            except requests.exceptions.RequestException as e:

                st.error(
                    f"Unable to connect to the API: {e}"
                )

            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )