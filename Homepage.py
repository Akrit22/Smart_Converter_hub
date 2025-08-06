
import streamlit as st
import os
from utils.styling import set_background_image, show_feature_card

# Configure the page
st.set_page_config(
    page_title="Smart Converter Hub",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set background image (if available)
try:
    if os.path.exists("assets/tech_bg.png"):
        set_background_image("assets/tech_bg.png")
except:
    pass

# Header
st.markdown("""
<div class="header-style">
    🔄 Smart Converter Hub
</div>
""", unsafe_allow_html=True)

# Features Section
st.markdown("## 🚀 Available Features")

col1, col2 = st.columns(2)

with col1:
    show_feature_card(
        "PDF to Audiobook", 
        "Convert your PDF documents into high-quality audiobooks. Perfect for learning on-the-go or accessibility needs.",
        "📄"
    )

    show_feature_card(
        "PDF Summarizer", 
        "Get concise, intelligent summaries of your PDF documents. Save time by extracting key information quickly.",
        "📋"
    )

with col2:
    show_feature_card(
        "Text to Audio", 
        "Transform any text into natural-sounding speech. Customize voice, speed, and save as audio files.",
        "📝"
    )

    show_feature_card(
        "Audio to PDF", 
        "Convert audio recordings into text documents. Perfect for transcribing meetings, lectures, or interviews.",
        "🎵"
    )

# Navigation help
st.markdown("""
<div class="main-container" >
  <div style="background: rgba(0, 0, 0, 0.8);">
    <h3>🧭 How to Get Started</h3>
    <ol>
        <li>Choose a conversion tool from the sidebar navigation</li>
        <li>Upload your file or input your text</li>
        <li>Configure your preferences (optional)</li>
        <li>Click convert and download your results!</li>
    </ol>
  </div>
</div>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🔄 Navigation")
st.sidebar.markdown("""
Select a conversion tool from the pages above to get started!

### Quick Access:
- 📄 **PDF to Audio**: Convert documents to audiobooks
- 📝 **Text to Audio**: Convert text to speech
- 📋 **PDF Summarizer**: Summarize long documents  
- 🎵 **Audio to PDF**: Transcribe audio to text

### Need Help?
Each page includes:
- Step-by-step instructions
- Usage examples
- Tips for best results
- Download options
""")

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem; background: rgba(0,0,0,0.1); border-radius: 10px; margin-top: 2rem;">
    <p>© 2025 Smart Converter Hub | Built using Streamlit</p>
    <p>Transform • Convert • Innovate</p>
    <p>Build by Akrit Pathania</p>
</div>
""", unsafe_allow_html=True)
