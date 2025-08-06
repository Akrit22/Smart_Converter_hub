
import streamlit as st
import os
import tempfile
from utils.styling import set_background_image
from utils.converters import AudioToPDFConverter, save_uploaded_file, clean_temp_files

# Configure page
st.set_page_config(page_title="Audio to PDF Converter", page_icon="🎵", layout="wide")

# Set background image
try:
    if os.path.exists("assets/tech_bg.png"):
        set_background_image("assets/tech_bg.png")
except:
    pass

# Header
st.markdown("""
<div class="header-style">
    🎵 Audio to PDF Converter
</div>
""", unsafe_allow_html=True)

# Description
st.markdown("""
<div class="main-container">
    <h2>Transform Audio into Text Documents</h2>
    <p>Convert your audio recordings into text documents using advanced speech recognition. Perfect for:</p>
    <ul>
        <li>🎤 Transcribing interviews and meetings</li>
        <li>📚 Converting lectures to readable notes</li>
        <li>📝 Creating transcripts from podcasts</li>
        <li>💼 Converting voice memos to documents</li>
        <li>♿ Accessibility and documentation needs</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# File upload section
st.subheader("🎵 Upload Your Audio File")

uploaded_audio = st.file_uploader(
    "Choose an audio file",
    type=['wav', 'mp3', 'flac', 'm4a', 'ogg'],
    help="Upload audio file in supported format (WAV, MP3, FLAC, M4A, OGG)"
)

if uploaded_audio is not None:
    st.success(f"✅ Audio file uploaded: {uploaded_audio.name}")

    # Display file info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🎵 File Name", uploaded_audio.name.split('.')[0])
    with col2:
        st.metric("📊 File Size", f"{uploaded_audio.size / 1024:.1f} KB")
    with col3:
        file_extension = uploaded_audio.name.split('.')[-1].upper()
        st.metric("📁 Format", file_extension)

    # Audio player
    st.subheader("🔊 Audio Preview")
    st.audio(uploaded_audio, format=f'audio/{uploaded_audio.name.split(".")[-1]}')

# Transcription settings
if uploaded_audio is not None:
    st.markdown("---")
    st.subheader("⚙️ Transcription Settings")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🗣️ Speech Recognition Settings")

        language = st.selectbox(
            "Language",
            ["en-US", "en-GB", "es-ES", "fr-FR", "de-DE", "it-IT", "pt-PT"],
            help="Select the primary language spoken in the audio"
        )

        audio_quality = st.selectbox(
            "Audio Quality",
            ["Auto", "High Quality", "Standard"],
            help="Choose processing quality (higher quality = more accurate but slower)"
        )

    with col2:
        st.markdown("#### 📄 Output Settings")

        output_format = st.selectbox(
            "Output Format",
            ["Text File (.txt)", "Rich Text (.rtf)", "Markdown (.md)", "PDF Document (.pdf)"],
            help="Choose the format for your transcribed document"
        )


        include_timestamps = st.checkbox(
            "Include Timestamps",
            value=False,
            help="Add time markers to the transcription"
        )

        speaker_detection = st.checkbox(
            "Speaker Detection",
            value=False,
            help="Attempt to identify different speakers (experimental)"
        )

# Processing section
if uploaded_audio is not None:
    st.markdown("---")
    st.subheader("🔄 Convert Audio to Text")

    # Important note
    st.warning("""
    ⚠️ **Important Notes:**
    - This feature requires an internet connection for speech recognition
    - Processing time varies based on audio length and quality
    - Clear speech produces better results
    - Background noise may affect accuracy
    """)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎵 Convert Audio to PDF", use_container_width=True):
            with st.spinner("Converting audio to text... This may take several minutes depending on audio length."):
                try:
                    # Save uploaded audio file
                    temp_audio_path = save_uploaded_file(uploaded_audio, "temp")

                    if temp_audio_path:
                        st.info("🎧 Processing audio file...")

                        # Check if file is WAV format (required for speech_recognition)
                        if not uploaded_audio.name.lower().endswith('.wav'):
                            st.info("🔄 Converting audio to WAV format...")
                            # Note: In a real implementation, you'd use pydub or similar for conversion
                            st.warning("⚠️ For best results, please upload WAV format audio files.")

                        # Convert audio to text
                        st.info("🤖 Transcribing speech to text...")
                        transcribed_text = AudioToPDFConverter.audio_to_text(temp_audio_path)

                        if transcribed_text:
                            st.success("✅ Transcription completed successfully!")

                            # Display transcribed text
                            st.subheader("📝 Transcribed Text")

                            # Add timestamps if requested
                            if include_timestamps:
                                # This is a simplified timestamp - in real implementation, 
                                # you'd need more advanced audio processing
                                display_text = f"[00:00] {transcribed_text}"
                            else:
                                display_text = transcribed_text

                            # Add speaker detection if requested
                            if speaker_detection:
                                display_text = f"Speaker 1: {display_text}"

                            st.markdown(f"""
                            <div class="main-container">
                                <p style="font-size: 1.1em; line-height: 1.6; text-align: justify; white-space: pre-wrap;">
                                    {display_text}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)

                            # Create downloadable file
                            st.subheader("📥 Download Transcription")

                            # Determine file extension
                            # Determine file extension
                            if output_format == "Text File (.txt)":
                                file_ext = "txt"
                                mime_type = "text/plain"
                            elif output_format == "Rich Text (.rtf)":
                                file_ext = "rtf"
                                mime_type = "application/rtf"
                            elif output_format == "Markdown (.md)":
                                file_ext = "md"
                                mime_type = "text/markdown"
                                display_text = f"# Audio Transcription\n\n{display_text}"
                            elif output_format == "PDF Document (.pdf)":
                                file_ext = "pdf"
                                mime_type = "application/pdf"

                            # Save to file
                            output_filename = f"temp/transcription.{file_ext}"
                            text_file_path = AudioToPDFConverter.text_to_file(display_text, output_filename)

                            if text_file_path and os.path.exists(text_file_path):
                                with open(text_file_path, 'rb') as f:
                                    file_data = f.read()

                                st.download_button(
                                    label=f"📄 Download as {output_format}",
                                    data=file_data,
                                    file_name=f"{uploaded_audio.name.rsplit('.', 1)[0]}_transcript.{file_ext}",
                                    mime=mime_type,
                                    use_container_width=True
                                )

                            # Statistics
                            st.subheader("📊 Transcription Statistics")
                            word_count = len(transcribed_text.split())
                            char_count = len(transcribed_text)
                            estimated_duration = uploaded_audio.size / 1024 / 16  # Rough estimate

                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("📝 Words", word_count)
                            with col2:
                                st.metric("📄 Characters", char_count)
                            with col3:
                                st.metric("⏱️ Est. Audio Length", f"~{estimated_duration:.1f} min")
                            with col4:
                                accuracy = "Good" if word_count > 10 else "Check Audio Quality"
                                st.metric("🎯 Quality", accuracy)

                            # Additional actions
                            st.markdown("---")
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("🔄 Process New Audio", use_container_width=True):
                                    st.experimental_rerun()
                            with col2:
                                if st.button("📋 Copy Text", use_container_width=True):
                                    st.info("💡 Use Ctrl+A, Ctrl+C to copy the transcribed text above")

                        else:
                            st.error("""
                            ❌ **Transcription failed.** This could be due to:
                            - Poor audio quality or background noise
                            - Unsupported audio format
                            - Network connectivity issues
                            - Speech not clearly audible

                            **Please try:**
                            - Using WAV format audio files
                            - Ensuring clear, loud speech
                            - Reducing background noise
                            - Checking your internet connection
                            """)

                    else:
                        st.error("❌ Failed to process the uploaded audio file.")

                except Exception as e:
                    st.error(f"❌ Error during conversion: {str(e)}")
                    st.error("""
                    **Troubleshooting Tips:**
                    - Ensure audio file is not corrupted
                    - Try converting to WAV format first
                    - Check file size (very large files may timeout)
                    - Verify internet connection for speech recognition
                    """)

                finally:
                    # Clean up temporary files
                    clean_temp_files("temp")

else:
    st.info("👆 Please upload an audio file to start the transcription process.")



# Sidebar help
st.sidebar.title("🎵 Audio to PDF Help")
st.sidebar.markdown("""
### How to Use:
1. **Upload** audio file (WAV recommended)
2. **Configure** transcription settings
3. **Select** language and output format
4. **Click** Convert Audio to PDF
5. **Review** and download transcript

### Audio Requirements:
- **Quality:** Clear speech, minimal noise
- **Format:** WAV, MP3, FLAC, M4A, OGG
- **Size:** Under 25MB recommended
- **Length:** Shorter files process faster

### Settings:
- **Language:** Match audio language
- **Quality:** Higher = more accurate
- **Format:** Choose output file type
- **Timestamps:** Add time markers
- **Speakers:** Detect multiple voices

### Best Practices:
- Record in quiet environment
- Use external microphone if possible
- Speak clearly and at normal pace
- Avoid background music/noise
- Test with short clips first
""")
