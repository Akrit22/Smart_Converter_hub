
import streamlit as st
import os
import tempfile
from utils.styling import set_background_image
from utils.converters import TextToAudioConverter, clean_temp_files

# Configure page
st.set_page_config(page_title="Text to Audio Converter", page_icon="📝", layout="wide")

# Set background image
try:
    if os.path.exists("assets/tech_bg.png"):
        set_background_image("assets/tech_bg.png")
except:
    pass

# Header
st.markdown("""
<div class="header-style">
    📝 Text to Audio Converter
</div>
""", unsafe_allow_html=True)

# Description
st.markdown("""
<div class="main-container">
    <h2>Transform Text into Natural Speech</h2>
    <p>Convert any text into high-quality audio with customizable voice settings. Perfect for:</p>
    <ul>
        <li>📝 Converting articles and essays to audio</li>
        <li>📚 Creating audio content for learning</li>
        <li>♿ Accessibility and text-to-speech needs</li>
        <li>🎯 Content creation for podcasts or presentations</li>
        <li>🌐 Multi-language text processing</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Input methods
st.subheader("📝 Input Your Text")

# Text input tabs
tab1, tab2 = st.tabs(["✍️ Type Text", "📁 Upload Text File"])

text_content = ""

with tab1:
    st.markdown("### Type or Paste Your Text")
    text_content = st.text_area(
        "Enter your text here:",
        height=200,
        placeholder="Type or paste your text here. You can input articles, essays, stories, or any text you'd like to convert to audio...",
        help="Enter the text you want to convert to speech"
    )

    if text_content:
        word_count = len(text_content.split())
        char_count = len(text_content)
        st.info(f"📊 Text Stats: {word_count} words, {char_count} characters (~{word_count//150} minutes estimated audio)")

with tab2:
    st.markdown("### Upload a Text File")
    uploaded_file = st.file_uploader(
        "Choose a text file",
        type=['txt', 'md', 'csv'],
        help="Upload a .txt, .md, or .csv file containing your text"
    )

    if uploaded_file is not None:
        try:
            text_content = str(uploaded_file.read(), "utf-8")
            st.success(f"✅ File uploaded: {uploaded_file.name}")

            # Show preview
            with st.expander("📖 Preview uploaded text"):
                st.text_area("File content:", text_content[:500] + "..." if len(text_content) > 500 else text_content, height=150)

            word_count = len(text_content.split())
            char_count = len(text_content)
            st.info(f"📊 File Stats: {word_count} words, {char_count} characters")

        except Exception as e:
            st.error(f"❌ Error reading file: {e}")

# Audio settings
if text_content:
    st.markdown("---")
    st.subheader("🎵 Audio Configuration")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🗣️ Voice Settings")
        voice_gender = st.selectbox(
            "Voice Type",
            ["Female", "Male"],
            help="Select preferred voice gender"
        )

        voice_rate = st.slider(
            "Speech Rate (Words per minute)",
            100, 300, 200, 10,
            help="Adjust how fast the voice speaks"
        )

    with col2:
        st.markdown("#### 🔊 Audio Settings")
        voice_volume = st.slider(
            "Volume Level",
            0.1, 1.0, 0.8, 0.1,
            help="Adjust audio volume"
        )

        audio_format = st.selectbox(
            "Output Format",
            ["MP3", "WAV"],
            help="Choose audio file format"
        )

    # Preview section
    st.markdown("#### 🔍 Text Preview")
    preview_text = text_content[:200] + "..." if len(text_content) > 200 else text_content
    st.text(preview_text)

# Conversion section
if text_content.strip():
    st.markdown("---")
    st.subheader("🔄 Convert to Audio")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎵 Convert Text to Audio", use_container_width=True):
            if len(text_content.strip()) < 10:
                st.warning("⚠️ Please enter at least 10 characters of text.")
            else:
                with st.spinner("Converting text to audio... Please wait."):
                    try:
                        # Create temp directory
                        os.makedirs("temp", exist_ok=True)

                        # Set output filename
                        output_filename = f"text_audio.{audio_format.lower()}"
                        output_path = f"temp/{output_filename}"

                        # Convert text to audio
                        audio_file = TextToAudioConverter.convert_text_to_audio(
                            text_content,
                            output_path,
                            rate=voice_rate,
                            volume=voice_volume,
                            voice_gender=voice_gender.lower()
                        )

                        if audio_file and os.path.exists(audio_file):
                            st.success("✅ Conversion completed successfully!")

                            # Display audio player
                            st.subheader("🎵 Your Audio")
                            audio_file_data = open(audio_file, 'rb').read()
                            st.audio(audio_file_data, format=f'audio/{audio_format.lower()}')

                            # Download button
                            st.download_button(
                                label="📥 Download Audio File",
                                data=audio_file_data,
                                file_name=f"converted_text.{audio_format.lower()}",
                                mime=f"audio/{audio_format.lower()}",
                                use_container_width=True
                            )

                            # Statistics
                            st.markdown("### 📊 Conversion Statistics")
                            col1, col2, col3, col4 = st.columns(4)

                            with col1:
                                st.metric("📝 Words", len(text_content.split()))
                            with col2:
                                st.metric("📄 Characters", len(text_content))
                            with col3:
                                st.metric("⏱️ Est. Duration", f"~{len(text_content.split())//150} min")
                            with col4:
                                st.metric("📁 File Size", f"{os.path.getsize(audio_file) / 1024:.1f} KB")

                        else:
                            st.error("❌ Failed to create audio file. Please try again.")

                    except Exception as e:
                        st.error(f"❌ Error during conversion: {str(e)}")
                        st.error("This might be due to system audio configuration. Please try different settings.")

                    finally:
                        # Clean up
                        clean_temp_files("temp")

else:
    st.info("👆 Please enter some text above to convert to audio.")

# Tips section
st.markdown("---")
st.markdown("""
<div class="main-container">
    <h3>💡 Tips for Best Results</h3>
    <ul>
        <li><strong>📝 Text Quality:</strong> Use clear, well-punctuated text for better pronunciation</li>
        <li><strong>📏 Length:</strong> Break very long texts into smaller chunks for better processing</li>
        <li><strong>🗣️ Speech Rate:</strong> 150-200 WPM is ideal for most content</li>
        <li><strong>📖 Formatting:</strong> Remove special characters that might affect pronunciation</li>
        <li><strong>🎵 Audio Quality:</strong> WAV format provides higher quality than MP3</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Sidebar help
st.sidebar.title("📝 Text to Audio Help")
st.sidebar.markdown("""
### How to Use:
1. **Input** your text (type or upload)
2. **Configure** voice and audio settings
3. **Preview** your text content
4. **Click** Convert Text to Audio
5. **Listen** and download

### Input Options:
- **Type:** Direct text input
- **Upload:** .txt, .md, .csv files
- **Paste:** Copy-paste from anywhere

### Voice Options:
- **Gender:** Male/Female voices
- **Speed:** 100-300 WPM
- **Volume:** Adjustable levels
- **Format:** MP3 or WAV output

### Best Practices:
- Use proper punctuation
- Check text preview first
- Test settings with short text
- Choose appropriate speech rate
""")
