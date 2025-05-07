import streamlit as st
import tempfile
import os
from groq import Groq

# --- Page setup ---
st.set_page_config(page_title="Audio Subtitle Generator", page_icon="🎵", layout="centered")

# --- CSS ---
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .title {
        font-size: 3em;
        color: #4B8BBE;
        text-align: center;
        font-weight: bold;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2em;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown('<div class="title">🎙️ Audio to Subtitle Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload your audio file or record it, then generate subtitles!</div>', unsafe_allow_html=True)

# --- Session state init ---
if "audio_mode" not in st.session_state:
    st.session_state.audio_mode = "upload"  # or "record"

# --- Groq client ---
client = Groq(api_key=st.secrets["TOKEN"])

# --- Toggle buttons ---
col1, col2 = st.columns(2)
with col1:
    if st.button("🔄 Switch to Upload Mode"):
        st.session_state.audio_mode = "upload"
with col2:
    if st.button("🎙️ Switch to Record Mode"):
        st.session_state.audio_mode = "record"

st.markdown(f"**Current Mode:** `{st.session_state.audio_mode}`")

# --- Upload or record ---
audio_file = None
if st.session_state.audio_mode == "upload":
    audio_file = st.file_uploader("📤 Upload your audio file (mp3, wav, m4a)", type=["mp3", "wav", "m4a"])
elif st.session_state.audio_mode == "record":
    audio_file = st.audio_input("🎤 Record your voice")

# --- Transcribe ---
if st.button("🧠 Generate Subtitles"):
    if not audio_file:
        st.warning("Please provide an audio file or record something first.")
        st.stop()
    if st.session_state.audio_mode == "upload":
        st.audio(audio_file, format="audio/mp3")

    with st.spinner("Transcribing..."):
        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-large-v3-turbo",
            prompt="Specify context or spelling",
            response_format="verbose_json",
            timestamp_granularities=["word", "segment"],
            language="en",
            temperature=0.0
        )
        subtitles = transcription.to_dict()["words"]

    st.success("✅ Transcription complete!")
    st.markdown("### 📝 Subtitles:")
    st.json(subtitles)

# --- Footer ---
st.markdown("---")
st.caption("Made with Omar❤️ using Streamlit")
