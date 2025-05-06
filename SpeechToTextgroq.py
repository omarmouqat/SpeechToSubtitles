import streamlit as st
import tempfile
import os
from groq import Groq

# Page config
st.set_page_config(page_title="Audio Subtitle Generator", page_icon="🎵", layout="centered")

# Custom CSS
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

# Header
st.markdown('<div class="title">🎙️ Audio to Subtitle Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload your audio file and generate subtitles in seconds!</div>',
            unsafe_allow_html=True)

# Audio file uploader
audio_file = st.file_uploader("📤 Upload your audio file (mp3, wav, m4a)", type=["mp3", "wav", "m4a"])



# Initialize the Groq client
client = Groq(api_key=st.secrets["TOKEN"])
button = st.button("Generate Subtitles")

# Subtitle generation (placeholder)
if audio_file is not None:
    st.audio(audio_file, format="audio/mp3")
    if button is True:
        transcription = client.audio.transcriptions.create(
            file=audio_file,  # Required audio file
            model="whisper-large-v3-turbo",  # Required model to use for transcription
            prompt="Specify context or spelling",  # Optional
            response_format="verbose_json",  # Optional
            timestamp_granularities=["word", "segment"],
            # Optional (must set response_format to "json" to use and can specify "word", "segment" (default), or both)
            language="en",  # Optional
            temperature=0.0  # Optional
        )
        subtitles = transcription.to_dict()["words"]
        # ===========================================
        st.success("✅ Transcription complete!")
        st.markdown("### 📝 Subtitles:")
        st.json(subtitles)
        
        

# Footer
st.markdown("---")
st.caption("Made with ❤️ using Streamlit")
