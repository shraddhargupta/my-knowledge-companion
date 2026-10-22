import streamlit as st
from skill_agent import create_agent

st.set_page_config(
    page_title="My Knowledge Companion",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ---------- Styling ----------
st.markdown("""
<style>
    .stApp {
        background: #F7F6F2;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        max-width: 850px;
        padding-top: 2.5rem;
        padding-bottom: 7rem;
    }

    [data-testid="stSidebar"] {
        background: #ECEFE8;
        border-right: 1px solid #DDE2D9;
    }

    .brand {
        font-size: 1.55rem;
        font-weight: 700;
        color: #294638;
        letter-spacing: -0.5px;
    }

    .subtitle {
        color: #68766B;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    .eyebrow {
        color: #718171;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .hero {
        padding: 2.5rem 0 1.5rem 0;
    }

    .hero h1 {
        color: #24372D;
        font-size: 2.7rem;
        letter-spacing: -1.5px;
        line-height: 1.15;
        margin: 0.7rem 0;
    }

    .hero p {
        color: #68766B;
        font-size: 1.05rem;
        line-height: 1.7;
        max-width: 620px;
    }

    [data-testid="stChatMessage"] {
        background: #FFFFFF;
        border: 1px solid #E5E7E0;
        border-radius: 16px;
        padding: 1rem;
        margin-bottom: 0.8rem;
    }

    [data-testid="stChatInput"] {
        border-color: #D7DED4;
        border-radius: 16px;
    }

    div.stButton > button {
        border-radius: 12px;
        border: 1px solid #DDE2D9;
        background: #FFFFFF;
        color: #294638;
        text-align: left;
        min-height: 3rem;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        border-color: #78917A;
        background: #F0F4EE;
        color: #294638;
    }

    .footer {
        color: #879087;
        font-size: 0.78rem;
        text-align: center;
        padding-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)


# ---------- Agent ----------
@st.cache_resource
def get_agent():
    return create_agent()


# ---------- Session state ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    st.session_state.agent = None


# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("### 📚 My Knowledge Companion")
    st.caption("Your personal learning space")

    st.divider()

    st.markdown("**What you can do here**")
    st.markdown(
        "- Understand technical concepts\n"
        "- Explore your personal notes\n"
        "- Connect ideas across topics\n"
        "- Revisit trusted resources"
    )

    st.divider()

    st.markdown("**Your learning, your sources**")
    st.caption(
        "Answers should draw on your knowledge base. "
        "When relevant, check the retrieved sources to verify the answer."
    )

    if st.button("＋ Start a new conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("Local AI · Python · RAG · Ollama")


# ---------- Main header ----------
st.markdown(
    '<div class="brand">📚 My Knowledge Companion</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">Your knowledge, connected and ready to use.</div>',
    unsafe_allow_html=True,
)

st.divider()


# ---------- Welcome screen ----------
if not st.session_state.messages:
    st.markdown("""
    <div class="hero">
        <div class="eyebrow">YOUR PERSONAL LEARNING SPACE</div>
        <h1>Curiosity starts here.</h1>
        <p>
            Explore technical concepts, revisit what you've learned,
            and build on your knowledge using your own trusted resources.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### What would you like to explore?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "📖  Understand a concept",
            use_container_width=True,
        ):
            st.session_state.suggested_prompt = (
                "Explain a technical concept using my knowledge base."
            )
            st.rerun()

        if st.button(
            "🔎  Explore my notes",
            use_container_width=True,
        ):
            st.session_state.suggested_prompt = (
                "What topics are covered in my knowledge base?"
            )
            st.rerun()

    with col2:
        if st.button(
            "🧩  Connect related ideas",
            use_container_width=True,
        ):
            st.session_state.suggested_prompt = (
                "Find related concepts in my knowledge base and explain how they connect."
            )
            st.rerun()

        if st.button(
            "💡  Test my understanding",
            use_container_width=True,
        ):
            st.session_state.suggested_prompt = (
                "Help me test my understanding of a topic from my notes."
            )
            st.rerun()


# ---------- Chat history ----------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------- Chat input ----------
prompt = st.chat_input(
    "Ask something you want to understand..."
)

if not prompt and "suggested_prompt" in st.session_state:
    prompt = st.session_state.pop("suggested_prompt")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Exploring your knowledge..."):
            try:
                if st.session_state.agent is None:
                    st.session_state.agent = get_agent()

                response = st.session_state.agent.run(prompt)

                if not isinstance(response, str):
                    response = str(response)

                st.markdown(response)

            except Exception as error:
                response = (
                    "I couldn't complete that request. "
                    "Please check that Ollama is running and your "
                    "knowledge base is configured correctly."
                )
                st.error(response)
                st.caption(f"Technical detail: {error}")

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )


st.markdown(
    '<div class="footer">Built around your knowledge. Powered by AI.</div>',
    unsafe_allow_html=True,
)
