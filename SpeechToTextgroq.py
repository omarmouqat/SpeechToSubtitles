import streamlit as st
from groq import Groq

# --- Page config ---
st.set_page_config(page_title="Audio Subtitle Generator", page_icon="🎵", layout="centered")

# --- CSS ---
st.markdown("""
    <style>
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

st.markdown('<div class="title">🎙️ Audio to Subtitle Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload or record audio, and generate subtitles</div>', unsafe_allow_html=True)

# --- Session state ---
if "audio_mode" not in st.session_state:
    st.session_state.audio_mode = "upload"
if "subtitles" not in st.session_state:
    st.session_state.subtitles = None

# --- Groq Client ---
client = Groq(api_key=st.secrets['TOKEN'])

# --- Mode toggle buttons ---
col1, col2 = st.columns(2)
with col1:
    if st.button("🔄 Switch to Upload Mode"):
        st.session_state.audio_mode = "upload"
with col2:
    if st.button("🎙️ Switch to Record Mode"):
        st.session_state.audio_mode = "record"

# --- Audio input ---
audio_file = None
if st.session_state.audio_mode == "upload":
    audio_file = st.file_uploader("📤 Upload your audio file (mp3, wav, m4a)", type=["mp3", "wav", "m4a"])
elif st.session_state.audio_mode == "record":
    audio_file = st.audio_input("🎤 Record your voice")

# --- Generate subtitles ---
if st.button("🧠 Generate Subtitles"):
    if not audio_file:
        st.warning("Please provide an audio file or record something.")
    else:
        st.audio(audio_file, format="audio/mp3")

        with st.spinner("Transcribing..."):
            transcription = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-large-v3-turbo",
                prompt="",
                response_format="verbose_json",
                timestamp_granularities=["word", "segment"],
                language="en",
                temperature=0.0
            )
            st.session_state.subtitles = transcription.to_dict()["words"]

        st.success("✅ Transcription complete!")

# --- Display Subtitles with Slider ---
if st.session_state.subtitles:
    st.markdown("### 🎚️ Explore Subtitles")
    idx = st.slider("Select subtitle index", 0, len(st.session_state.subtitles) - 1, 0)
    st.json(st.session_state.subtitles[idx])

    # Optional: Display full plain text
    full_text = " ".join([w["word"] for w in st.session_state.subtitles])
    st.markdown("### 🧾 Full Transcript (Plain Text)")
    st.text_area("Transcript", full_text, height=150)

# --- Footer ---
st.markdown("---")
st.caption("Made with Omar❤️ using Streamlit")
