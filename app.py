# app.py

import streamlit as st
from ai_translator import translate, SUPPORTED_PAIRS

# ---------------------------------------------------------------------------
# Page configuration — must be the very first Streamlit call
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌐",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Custom CSS — clean, modern, minimal aesthetic
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
        /* ── General ── */
        html, body, [class*="css"] {
            font-family: 'Inter', 'Segoe UI', sans-serif;
        }

        /* ── Hide Streamlit default chrome ── */
        #MainMenu, footer, header { visibility: hidden; }

        /* ── Page wrapper ── */
        .block-container {
            max-width: 780px;
            padding-top: 2.5rem;
            padding-bottom: 3rem;
        }

        /* ── Hero header ── */
        .hero-title {
            text-align: center;
            font-size: 2.4rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            margin-bottom: 0.2rem;
            background: linear-gradient(135deg, #6C63FF, #3ECFCF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero-sub {
            text-align: center;
            color: #888;
            font-size: 0.95rem;
            margin-bottom: 2rem;
        }

        /* ── Card container ── */
        .card {
            background: #1E1E2E;
            border: 1px solid #2E2E42;
            border-radius: 16px;
            padding: 1.6rem 1.8rem;
            margin-bottom: 1.2rem;
        }

        /* ── Section label ── */
        .section-label {
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            color: #6C63FF;
            margin-bottom: 0.5rem;
        }

        /* ── Text areas ── */
        textarea {
            background-color: #12121C !important;
            border: 1px solid #2E2E42 !important;
            border-radius: 10px !important;
            color: #E0E0F0 !important;
            font-size: 1rem !important;
            line-height: 1.6 !important;
        }
        textarea:focus {
            border-color: #6C63FF !important;
            box-shadow: 0 0 0 2px rgba(108,99,255,0.25) !important;
        }

        /* ── Translate button ── */
        div.stButton > button {
            width: 100%;
            background: linear-gradient(135deg, #6C63FF, #3ECFCF);
            color: white;
            font-weight: 700;
            font-size: 1rem;
            border: none;
            border-radius: 10px;
            padding: 0.65rem 0;
            cursor: pointer;
            transition: opacity 0.2s ease;
            letter-spacing: 0.4px;
        }
        div.stButton > button:hover {
            opacity: 0.88;
        }

        /* ── Select boxes ── */
        div[data-baseweb="select"] > div {
            background-color: #12121C !important;
            border-color: #2E2E42 !important;
            border-radius: 10px !important;
            color: #E0E0F0 !important;
        }

        /* ── Output box ── */
        .output-box {
            background: #12121C;
            border: 1px solid #2E2E42;
            border-radius: 10px;
            padding: 1rem 1.2rem;
            min-height: 140px;
            color: #E0E0F0;
            font-size: 1rem;
            line-height: 1.7;
            white-space: pre-wrap;
            word-break: break-word;
        }
        .output-placeholder {
            color: #444;
            font-style: italic;
        }

        /* ── Divider ── */
        .divider {
            border: none;
            border-top: 1px solid #2E2E42;
            margin: 1.4rem 0;
        }

        /* ── Footer ── */
        .app-footer {
            text-align: center;
            color: #444;
            font-size: 0.78rem;
            margin-top: 2.5rem;
        }
        .app-footer a {
            color: #6C63FF;
            text-decoration: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Session State initialisation — preserves values across reruns
# ---------------------------------------------------------------------------
if "source_text" not in st.session_state:
    st.session_state.source_text = ""
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""
if "selected_pair" not in st.session_state:
    st.session_state.selected_pair = list(SUPPORTED_PAIRS.keys())[0]
if "error_message" not in st.session_state:
    st.session_state.error_message = ""

# ---------------------------------------------------------------------------
# Hero header
# ---------------------------------------------------------------------------
st.markdown('<div class="hero-title">🌐 AI Language Translator</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">Powered by Helsinki-NLP MarianMT · Offline neural translation</div>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Language pair selector
# ---------------------------------------------------------------------------
st.markdown('<div class="section-label">Translation Direction</div>', unsafe_allow_html=True)
selected_pair = st.selectbox(
    label="language_pair",
    options=list(SUPPORTED_PAIRS.keys()),
    index=list(SUPPORTED_PAIRS.keys()).index(st.session_state.selected_pair),
    label_visibility="collapsed",
)
st.session_state.selected_pair = selected_pair

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Source text input
# ---------------------------------------------------------------------------
st.markdown('<div class="section-label">Source Text</div>', unsafe_allow_html=True)
source_text = st.text_area(
    label="source_input",
    value=st.session_state.source_text,
    placeholder="Type or paste the text you want to translate...",
    height=160,
    max_chars=2000,
    label_visibility="collapsed",
)
st.session_state.source_text = source_text

char_count = len(source_text)
st.caption(f"{char_count} / 2000 characters")

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Translate button + inference
# ---------------------------------------------------------------------------
translate_clicked = st.button("⚡ Translate", use_container_width=True)

if translate_clicked:
    st.session_state.error_message = ""
    if not source_text.strip():
        st.session_state.error_message = "⚠️ Please enter some text before translating."
        st.session_state.translated_text = ""
    else:
        src_code, tgt_code = SUPPORTED_PAIRS[selected_pair]
        with st.spinner(f"Translating with Helsinki-NLP/opus-mt-{src_code}-{tgt_code} …"):
            try:
                result = translate(source_text, src_code, tgt_code)
                st.session_state.translated_text = result
            except OSError as e:
                st.session_state.error_message = f"❌ Model not found: {e}"
                st.session_state.translated_text = ""
            except Exception as e:
                st.session_state.error_message = f"❌ Translation failed: {e}"
                st.session_state.translated_text = ""

# ---------------------------------------------------------------------------
# Error banner
# ---------------------------------------------------------------------------
if st.session_state.error_message:
    st.error(st.session_state.error_message)

# ---------------------------------------------------------------------------
# Translation output
# ---------------------------------------------------------------------------
st.markdown("<hr class='divider'>", unsafe_allow_html=True)
st.markdown('<div class="section-label">Translation</div>', unsafe_allow_html=True)

if st.session_state.translated_text:
    st.markdown(
        f'<div class="output-box">{st.session_state.translated_text}</div>',
        unsafe_allow_html=True,
    )
    # Copy-to-clipboard via hidden text area trick
    st.code(st.session_state.translated_text, language=None)
else:
    st.markdown(
        '<div class="output-box output-placeholder">Your translation will appear here…</div>',
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Clear button
# ---------------------------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🗑️ Clear", use_container_width=False):
    st.session_state.source_text = ""
    st.session_state.translated_text = ""
    st.session_state.error_message = ""
    st.rerun()

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="app-footer">
        Built by <a href="https://github.com/Swapnil-bo" target="_blank">Swapnil-bo</a> ·
        Models by <a href="https://huggingface.co/Helsinki-NLP" target="_blank">Helsinki-NLP</a>
    </div>
    """,
    unsafe_allow_html=True,
)