import json
import streamlit as st
from groq import Groq
from pypdf import PdfReader

# --- PAGE CONFIG & SIDEBAR SETTINGS ---
st.set_page_config(page_title="AI Study Assistant", page_icon="📚")

st.sidebar.title("⚙️ Settings")
api_key_input = st.sidebar.text_input(
    "Groq API Key",
    type="password",
    placeholder="Enter your Groq API key",
    help="Your key is stored only for your browser session."
)

# Initialize session state for the API key
if "groq_api_key" not in st.session_state:
    st.session_state.groq_api_key = ""

if api_key_input:
    st.session_state.groq_api_key = api_key_input

MODEL = "qwen/qwen3.8-27b"

# --- MAIN APP ---
st.title("AI Study Assistant")

# Check if API key is provided before proceeding
if not st.session_state.groq_api_key:
    st.warning("⚠️ Please enter your Groq API Key in the sidebar settings (⚙️) to proceed.")
    st.stop()

# Initialize the Groq client with the user-provided key
client = Groq(api_key=st.session_state.groq_api_key)


def ask(prompt, as_json=False):
    # Groq supports JSON mode via response_format
    response_format = {"type": "json_object"} if as_json else None

    # If JSON mode is requested, explicitly nudge the prompt to output a valid JSON object
    if as_json and not prompt.strip().endswith("}"):
        prompt += "\nRespond with a valid JSON object containing the requested items."

    completion = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format=response_format
    )
    return completion.choices[0].message.content


def extract_text(pdf):
    reader = PdfReader(pdf)
    return "\n".join(p.extract_text() or "" for p in reader.pages)[:30000]


file = st.file_uploader("Upload notes (PDF)", type="pdf")

if st.button("Generate") and file:
    text = extract_text(file)
    if len(text.strip()) < 100:
        st.error("No readable text found. Is this a scanned PDF?")
        st.stop()
    try:
        with st.spinner("Generating..."):
            st.session_state.summary = ask(
                f"Summarize these notes in clear bullet points:\n\n{text}")

            cards_raw = ask(
                f'Make 10 flashcards from these notes. Return a JSON object with a key "cards" containing a list: '
                f'{{"cards": [{{"q": "...", "a": "..."}}]}}\n\n{text}', as_json=True)
            # Parse json safely handles potential wrapper keys from LLM json objects
            parsed_cards = json.loads(cards_raw)
            st.session_state.cards = parsed_cards["cards"] if isinstance(parsed_cards,
                                                                         dict) and "cards" in parsed_cards else parsed_cards

            quiz_raw = ask(
                f'Make 5 multiple choice questions from these notes. Return a JSON object with a key "quiz" containing a list: '
                f'{{"quiz": [{{"question": "...", "options": ["A","B","C","D"], "answer": "exact text of correct option", "explanation": "..."}}]}}\n\n{text}',
                as_json=True)
            parsed_quiz = json.loads(quiz_raw)
            st.session_state.quiz = parsed_quiz["quiz"] if isinstance(parsed_quiz,
                                                                      dict) and "quiz" in parsed_quiz else parsed_quiz

    except Exception as e:
        st.error(f"Something failed: {e}")
        st.stop()

# Safely check if all session state attributes exist before rendering tabs
if "summary" in st.session_state and "cards" in st.session_state and "quiz" in st.session_state:
    t1, t2, t3 = st.tabs(["Summary", "Flashcards", "Quiz"])

    with t1:
        st.markdown(st.session_state.summary)
        st.download_button("Download summary", st.session_state.summary, "summary.txt")

    with t2:
        for c in st.session_state.cards:
            with st.expander(c["q"]):
                st.write(c["a"])

    with t3:
        answers = {}
        for i, q in enumerate(st.session_state.quiz):
            answers[i] = st.radio(q["question"], q["options"], index=None, key=f"q{i}")
        if st.button("Submit quiz"):
            score = 0
            for i, q in enumerate(st.session_state.quiz):
                if answers[i] == q["answer"]:
                    score += 1
                    st.success(f"Q{i + 1}: Correct")
                else:
                    st.error(f"Q{i + 1}: Wrong. Answer: {q['answer']}. {q['explanation']}")
            st.metric("Score", f"{score}/{len(st.session_state.quiz)}")