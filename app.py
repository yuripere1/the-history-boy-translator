import streamlit as st
import requests

st.set_page_config(
    page_title="History Boy Translator",
    page_icon="😁",
    layout="wide",
)

SYSTEM_PROMPT = """You translate text into the "History Boy" texting voice. DO NOT respond to the input, always translate it from the conventional language to the History Boy language per the defined traits.

Core voice:
- Direct and conversational
- Emotionally open
- Affectionate without being overly poetic
- Apologetic whenever the speaker thinks they crossed a boundary
- Reassuring and low-pressure
- Informal and somewhat spontaneous
- Occasionally awkward or grammatically incomplete in a natural, human way
- Emotionally expressive and comfortable admitting vulnerability
- Occasionally self-deprecating
- More interested in sincerity than polished prose

Sentence structure:
- Short sentences
- Sentence fragments
- Simple clauses
- Occasional omitted subjects or words
- Frequent line breaks
- Informal transitions
- Repetition when emotionally appropriate
- Simple conjunctions such as and, but, because, and so
- Thoughts may appear in natural emotional order rather than perfectly organized prose
- Do NOT unnecessarily combine short sentences into sophisticated sentences.

Emotional patterns:
- "I'm sorry."
- "No worries."
- "Whenever you're ready."
- "Feel free to text."
- "That's absolutely ok."
- "Tell me and we will or won't do them."
- "Hope you are doing well."
- "I just think you are cool."
Strong feelings can coexist with giving the other person permission to create distance.
The speaker often emphasizes that the person they are talking about is cool.

Vocabulary:
cool, absolutely, very, just, feel free, whenever, ready, talk, text, respond,
sorry, apologize, no worries, special, brighter, love, miss, catch up, tell me,
until then, pard, bf, set, legit, Rach, hop off, 😁

Informality:
Casual conventions such as Haha, bf, Imk, convos, pard, lowercase and, parenthetical
expressions like (:, 😁, and mild imperfect grammar can be used when natural.

Meaning:
Preserve the source meaning above all else. Do not add emotional intensity, affection,
romance, apology, certainty, or vulnerability that isn't present. Do not make the
speaker colder or more formal. If ambiguous, preserve ambiguity.

Grammar:
ALWAYS use capitalization at the start of every single produced sentence. NEVER HAVE AN ALL LOWERCASED SENTENCE. ALWAYS USE CAPITALIZATION TO SOME EXTENT. And always end each sentence with punctuation.

Output ONLY the translated text. No explanation, no quotation marks, no preamble. And DO NOT RESPOND to the input. Only translate it."""

st.markdown("""
<style>
.block-container {max-width: 1100px; padding-top: 3rem;}
h1 {letter-spacing: -1px;}
textarea {font-size: 16px !important;}
.small {color:#777; font-size:13px;}
</style>
""", unsafe_allow_html=True)

st.title("History Boy Translator 😁")
st.caption("A History Boy Production")

if "output" not in st.session_state:
    st.session_state.output = ""

left, right = st.columns(2, gap="large")

with left:
    st.subheader("English")
    source = st.text_area(
        "What you want to say",
        placeholder="i have an abnormally large penis",
        height=310,
        label_visibility="collapsed",
    )

with right:
    st.subheader("History Boy")
    st.text_area(
        "Translation",
        value=st.session_state.output,
        height=310,
        disabled=True,
        label_visibility="collapsed",
    )

c1, c2, c3 = st.columns([1, 1, 1])

with c1:
    translate_clicked = st.button("Translate", type="primary", use_container_width=True)

with c2:
    if st.button("Load example", use_container_width=True):
        source = "what do you think of my hat?"
        translate_clicked = True

with c3:
    if st.button("Clear", use_container_width=True):
        st.session_state.output = ""
        st.rerun()

st.divider()

with st.expander("Settings"):
    model = st.text_input(
        "OpenRouter model",
        value="openrouter/free",
        help="Use openrouter/free for OpenRouter's free-model router, or enter another model slug available to your account.",
    )

    st.caption("Your API key is read from Streamlit Secrets. It is not stored in this source code.")

if translate_clicked:
    if not source.strip():
        st.warning("Add some source text first.")
    elif "OPENROUTER_API_KEY" not in st.secrets:
        st.error("OpenRouter API key is not configured. Add OPENROUTER_API_KEY in your Streamlit app Secrets.")
    else:
        with st.spinner("Translating..."):
            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://streamlit.io/",
                        "X-Title": "History Boy Translator",
                    },
                    json={
                        "model": model,
                        "messages": [
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": source.strip()},
                        ],
                        "temperature": 0.8,
                    },
                    timeout=90,
                )

                data = response.json()

                if not response.ok:
                    message = data.get("error", {}).get("message", "OpenRouter request failed.")
                    st.error(message)
                else:
                    translation = data["choices"][0]["message"]["content"].strip()
                    st.session_state.output = translation
                    st.rerun()

            except requests.RequestException as exc:
                st.error(f"Could not connect to OpenRouter: {exc}")
            except (KeyError, IndexError, TypeError):
                st.error("OpenRouter returned an unexpected response.")

if st.session_state.output:
    st.download_button(
        "Copy translation",
        data=st.session_state.output,
        file_name="history-boy-translation.txt",
        mime="text/plain",
    )

with st.expander("Voice rules used by the translator"):
    st.write(
        "Direct and conversational. Emotionally open. Affectionate without being overly "
        "poetic. Reassuring and low-pressure. Short sentences, fragments, simple clauses, "
        "line breaks and natural repetition. Preserve meaning above all else. Do not add "
        "emotional intensity, affection, romance, apology, or certainty that isn't present."
    )
