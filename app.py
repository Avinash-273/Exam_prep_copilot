import os
import time

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

st.set_page_config(
    page_title="Exam Prep Copilot | AI Study Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Read secrets from the hosting platform first, then fall back to local .env.
def get_api_key():
    try:
        secret_value = st.secrets.get("GROQ_API_KEY", "")
        if secret_value:
            return str(secret_value).strip()
    except Exception:
        # Streamlit secrets are optional during local development.
        pass
    return os.getenv("GROQ_API_KEY", "").strip()


API_KEY = get_api_key()

st.markdown(
    """
    <style>
      .block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 1180px;}
      .hero {padding: 1.6rem 1.8rem; border-radius: 18px; background: linear-gradient(120deg,#172554,#1d4ed8); color: white; margin-bottom: 1.2rem;}
      .hero h1 {color: white; margin: 0 0 .35rem 0; font-size: 2.25rem;}
      .hero p {color: #dbeafe; margin: 0; font-size: 1.05rem;}
      .feature-card {border: 1px solid rgba(128,128,128,.25); border-radius: 14px; padding: 1rem; min-height: 112px;}
      .muted {opacity: .75; font-size: .92rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="hero">
      <h1>🎓 Exam Prep Copilot</h1>
      <p>Your AI-powered study companion for clear explanations, revision flashcards, and quick practice quizzes.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

feature_cols = st.columns(3)
for col, icon, heading, detail in zip(
    feature_cols,
    ["📘", "🃏", "📝"],
    ["Understand", "Revise", "Practice"],
    ["Get simple, example-based explanations.", "Create five focused Q&A flashcards.", "Test yourself with a short quiz and answer key."],
):
    with col:
        st.markdown(
            f'<div class="feature-card"><h3>{icon} {heading}</h3><p class="muted">{detail}</p></div>',
            unsafe_allow_html=True,
        )


@st.cache_resource(show_spinner=False)
def get_model(temperature: float, max_tokens: int, api_key: str):
    if not api_key:
        from langchain_core.language_models.fake_chat_models import FakeListChatModel

        return FakeListChatModel(
            responses=[
                "Practice mode is active. Add your Groq API key in the app secrets to generate live AI study material.",
                "Q: What is artificial intelligence?\nA: AI is the field of building computer systems that perform tasks that usually require human intelligence.",
                "1. What is machine learning?\n2. What is deep learning?\n3. What is natural language processing?\n\nAnswer key: 1. Learning patterns from data. 2. ML using multi-layer neural networks. 3. Processing and understanding human language.",
            ]
        )

    from langchain_groq import ChatGroq

    return ChatGroq(
        model="openai/gpt-oss-120b",
        groq_api_key=api_key,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=45,
        max_retries=2,
    )


with st.sidebar:
    st.header("⚙️ Study settings")
    temperature = st.slider(
        "Creativity", min_value=0.0, max_value=1.0, value=0.3, step=0.1,
        help="Lower values produce more focused answers; higher values allow more variety.",
    )
    max_tokens = st.slider("Response length", min_value=200, max_value=1200, value=600, step=100)
    st.divider()
    st.subheader("💡 Suggested topics")
    st.markdown("- Generative AI\n- GANs and VAEs\n- CNNs and Transformers\n- Python fundamentals\n- SQL and DBMS")
    st.divider()
    if API_KEY:
        st.success("AI provider configured")
    else:
        st.info("Practice mode · Add GROQ_API_KEY to enable live AI responses")

SYSTEM_PROMPT = (
    "You are a patient, accurate exam tutor. Explain concepts in simple English, "
    "use short sections, and include practical examples. If uncertain, say so rather than inventing facts."
)


def build_messages(topic: str, task: str):
    if task == "Explanation":
        prompt = (
            f"Explain {topic} to a college student in about 150–250 words. "
            "Use headings and one simple practical example."
        )
    elif task == "Flashcards":
        prompt = (
            f"Create exactly five useful question-and-answer flashcards on {topic}. "
            "Format each as Q: ... followed by A: ..."
        )
    else:
        prompt = (
            f"Create three exam-style quiz questions on {topic}. Include a clear answer key "
            "after the questions and briefly explain each answer."
        )
    return [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=prompt)]


def invoke_with_retry(model, messages, attempts=3):
    for attempt in range(attempts):
        try:
            return model.invoke(messages)
        except Exception as exc:
            if attempt == attempts - 1:
                st.error(f"The AI request failed ({type(exc).__name__}). Check your API configuration and try again.")
                return None
            time.sleep(2 ** attempt)


st.divider()
st.subheader("Build your study material")
with st.form("study_form"):
    topic_col, task_col = st.columns([2, 1])
    with topic_col:
        topic = st.text_input("What topic are you studying?", placeholder="e.g. Retrieval-Augmented Generation (RAG)")
    with task_col:
        task = st.selectbox("Choose a study activity", ["Explanation", "Flashcards", "Quiz"])
    submitted = st.form_submit_button("🚀 Generate study material", type="primary", use_container_width=True)

if submitted:
    if not topic.strip():
        st.warning("Enter a topic to get started.")
    else:
        model = get_model(temperature, max_tokens, API_KEY)
        messages = build_messages(topic.strip(), task)
        with st.spinner("Preparing your study material..."):
            result = invoke_with_retry(model, messages)
        if result is not None:
            heading = {"Explanation": "📘 Topic explanation", "Flashcards": "🃏 Revision flashcards", "Quiz": "📝 Practice quiz"}[task]
            st.subheader(heading)
            st.markdown(result.content)
            st.success("Study material generated.")
            with st.expander("How to use this result"):
                st.write("Review the material, write down key points in your own words, and revisit difficult concepts before your exam.")

with st.expander("About this project"):
    st.write(
        "Exam Prep Copilot is a Python and Streamlit application that uses a Groq-hosted language model "
        "through LangChain to generate topic explanations, flashcards, and practice quizzes. "
        "It also includes a practice mode so the interface can be explored without an API key."
    )
    st.caption("Built with Python · Streamlit · LangChain · Groq")

st.caption("For learning support only. Always verify important facts with your course materials and trusted references.")
