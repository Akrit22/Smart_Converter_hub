# PDF to Audiobook
import streamlit as st
import os
import tempfile

from utils.styling import set_background_image
from utils.converters import PDFToAudioConverter, save_uploaded_file, clean_temp_files

# Configure page
st.set_page_config(page_title="PDF to Audio Converter", page_icon="📄", layout="wide")

# Set background image
try:
    if os.path.exists("assets/tech_bg.png"):
        set_background_image("assets/tech_bg.png")
except:
    pass

# Header
st.markdown("""
<div class="header-style">
    📄 PDF to Audiobook Converter
</div>
""", unsafe_allow_html=True)

# Description
st.markdown("""
<div class="main-container">
    <h2>Transform Your PDFs into Audiobooks</h2>
    <p>Convert any PDF document into high-quality audio files. Perfect for:</p>
    <ul>
        <li>📚 Creating audiobooks from e-books</li>
        <li>🎓 Converting study materials for audio learning</li>
        <li>♿ Making documents accessible for visually impaired users</li>
        <li>🚗 Listening to documents while commuting</li>
        <li>🏃 Multitasking while absorbing content</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Main interface
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📁 Upload Your PDF")
    uploaded_file = st.file_uploader(
        "Choose a PDF file", 
        type="pdf",
        help="Upload a PDF document to convert to audio"
    )

    if uploaded_file is not None:
        st.success(f"✅ File uploaded: {uploaded_file.name}")

        # Display file info
        st.info(f"📊 File size: {uploaded_file.size / 1024:.1f} KB")

with col2:
    st.subheader("🎵 Audio Settings")

    # Voice settings
    voice_rate = st.slider("🗣️ Speech Rate", 100, 300, 200, 10, 
                          help="Higher values = faster speech")

    voice_volume = st.slider("🔊 Volume", 0.1, 1.0, 0.8, 0.1,
                           help="Audio volume level")

    voice_gender = st.selectbox("👤 Voice Type", ["Female", "Male"], 
                               help="Select preferred voice gender")

# Conversion section
if uploaded_file is not None:
    st.markdown("---")
    st.subheader("🔄 Convert to Audio")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎵 Convert PDF to Audio", use_container_width=True):
            with st.spinner("Converting PDF to audio... This may take a few minutes."):
                try:
                    # Save uploaded file
                    temp_pdf_path = save_uploaded_file(uploaded_file, "temp")

                    if temp_pdf_path:
                        # Extract text from PDF
                        st.info("📝 Extracting text from PDF...")
                        text = PDFToAudioConverter.extract_text_from_pdf(temp_pdf_path)

                        if text:
                            # Show preview of extracted text
                            with st.expander("📖 Preview extracted text"):
                                st.text_area("Extracted text preview:", text[:500] + "..." if len(text) > 500 else text, height=150)

                            st.info("🔊 Converting text to audio...")

                            # Convert to audio
                            output_path = "temp/audiobook.wav"
                            audio_file = PDFToAudioConverter.text_to_audio(
                                text, output_path, rate=voice_rate, volume=voice_volume
                            )

                            if audio_file and os.path.exists(audio_file):
                                st.success("✅ Conversion completed successfully!")

                                # Display audio player
                                st.subheader("🎵 Your Audiobook")
                                audio_file_data = open(audio_file, 'rb').read()
                                st.audio(audio_file_data, format='audio/wav')

                                # Download button
                                st.download_button(
                                    label="📥 Download Audiobook",
                                    data=audio_file_data,
                                    file_name=f"{uploaded_file.name.replace('.pdf', '_audiobook.wav')}",
                                    mime="audio/wav",
                                    use_container_width=True
                                )

                                # Statistics
                                st.markdown("### 📊 Conversion Statistics")
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("📄 Text Length", f"{len(text)} characters")
                                with col2:
                                    st.metric("⏱️ Estimated Duration", f"~{len(text) // 800} minutes")
                                with col3:
                                    st.metric("📁 File Size", f"{os.path.getsize(audio_file) / 1024:.1f} KB")

                            else:
                                st.error("❌ Failed to create audio file. Please try again.")
                        else:
                            st.error("❌ Could not extract text from PDF. Please check if the PDF contains readable text.")
                    else:
                        st.error("❌ Failed to process uploaded file.")

                except Exception as e:
                    st.error(f"❌ Error during conversion: {str(e)}")

                finally:
                    # Clean up temporary files
                    clean_temp_files("temp")

# Tips and help section
st.markdown("---")
st.markdown("""
<div class="main-container">
    <h3>💡 Tips for Best Results</h3>
    <ul>
        <li><strong>📄 PDF Quality:</strong> Works best with text-based PDFs (not scanned images)</li>
        <li><strong>📏 File Size:</strong> For large files, consider splitting them into smaller sections</li>
        <li><strong>🗣️ Speech Rate:</strong> 150-250 WPM is optimal for most listeners</li>
        <li><strong>🔊 Volume:</strong> Test with a small section first to find your preferred settings</li>
        <li><strong>⚡ Performance:</strong> Processing time depends on document length and complexity</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Sidebar help
st.sidebar.title("📄 PDF to Audio Help")
st.sidebar.markdown("""
### How to Use:
1. **Upload** your PDF file
2. **Adjust** audio settings as needed
3. **Click** Convert PDF to Audio
4. **Listen** to preview
5. **Download** your audiobook

### Best Practices:
- Use text-based PDFs
- Check extracted text preview
- Adjust speech rate for comfort
- Test with small files first

### File Requirements:
- **Format:** PDF only
- **Size:** Up to 200MB
- **Type:** Text-based PDFs work best
- **Language:** English supported
""")
