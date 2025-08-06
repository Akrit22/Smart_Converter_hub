
import streamlit as st
import os
import tempfile
from utils.styling import set_background_image
from utils.converters import PDFSummarizer, save_uploaded_file, clean_temp_files

# Configure page
st.set_page_config(page_title="PDF Summarizer", page_icon="📋", layout="wide")

# Set background image
try:
    if os.path.exists("assets/tech_bg.png"):
        set_background_image("assets/tech_bg.png")
except:
    pass

# Header
st.markdown("""
<div class="header-style">
    📋 PDF Document Summarizer
</div>
""", unsafe_allow_html=True)

# Description
st.markdown("""
<div class="main-container">
    <h2>Intelligent Document Summarization</h2>
    <p>Extract key insights from lengthy PDF documents using advanced AI summarization. Perfect for:</p>
    <ul>
        <li>📚 Summarizing research papers and academic articles</li>
        <li>📊 Creating executive summaries of reports</li>
        <li>⏰ Quick review of lengthy documents</li>
        <li>📝 Generating study notes from textbooks</li>
        <li>🔍 Extracting main points from legal documents</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# File upload section
st.subheader("📁 Upload Your PDF Document")

uploaded_file = st.file_uploader(
    "Choose a PDF file to summarize",
    type="pdf",
    help="Upload a PDF document that you want to summarize"
)

if uploaded_file is not None:
    st.success(f"✅ File uploaded: {uploaded_file.name}")

    # Display file info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📄 File Name", uploaded_file.name.split('.')[0])
    with col2:
        st.metric("📊 File Size", f"{uploaded_file.size / 1024:.1f} KB")
    with col3:
        st.metric("📁 File Type", "PDF Document")

# Summarization settings
if uploaded_file is not None:
    st.markdown("---")
    st.subheader("⚙️ Summarization Settings")

    col1, col2 = st.columns(2)

    with col1:
        summary_length = st.selectbox(
            "📏 Summary Length",
            ["Short (3-5 sentences)", "Medium (5-8 sentences)", "Long (8-12 sentences)", "Custom"],
            help="Choose the desired length of your summary"
        )

        if summary_length == "Custom":
            custom_sentences = st.number_input(
                "Number of sentences",
                min_value=1,
                max_value=20,
                value=5,
                help="Specify exact number of sentences for summary"
            )
        else:
            sentence_map = {
                "Short (3-5 sentences)": 4,
                "Medium (5-8 sentences)": 6,
                "Long (8-12 sentences)": 10
            }
            custom_sentences = sentence_map[summary_length]

    with col2:
        output_format = st.selectbox(
            "📄 Output Format",
            ["Text Summary", "Downloadable Text File"],
            help="Choose how you want to receive the summary"
        )

        show_original = st.checkbox(
            "Show Original Text Preview",
            value=False,
            help="Display a preview of the extracted text from PDF"
        )

# Processing section
if uploaded_file is not None:
    st.markdown("---")
    st.subheader("🔄 Generate Summary")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📋 Generate Summary", use_container_width=True):
            with st.spinner("Analyzing document and generating summary... This may take a moment."):
                try:
                    # Save uploaded file
                    temp_pdf_path = save_uploaded_file(uploaded_file, "temp")

                    if temp_pdf_path:
                        # Extract text from PDF
                        st.info("📝 Extracting text from PDF...")
                        text = PDFSummarizer.extract_text_with_pdfplumber(temp_pdf_path)

                        if text and len(text.strip()) > 100:
                            # Show original text if requested
                            if show_original:
                                st.subheader("📖 Original Text Preview")
                                with st.expander("View extracted text (first 1000 characters)"):
                                    st.text_area(
                                        "Extracted text:",
                                        text[:1000] + "..." if len(text) > 1000 else text,
                                        height=200
                                    )

                            # Generate summary
                            st.info("🤖 Generating intelligent summary...")
                            summary = PDFSummarizer.summarize_text(text, num_sentences=custom_sentences)

                            if summary:
                                st.success("✅ Summary generated successfully!")

                                # Display summary
                                st.subheader("📋 Document Summary")
                                st.markdown(f"""
                                <div class="main-container">
                                    <p style="font-size: 1.1em; line-height: 1.6; text-align: justify;">
                                        {summary}
                                    </p>
                                </div>
                                """, unsafe_allow_html=True)

                                # Summary statistics
                                st.subheader("📊 Summary Statistics")
                                original_words = len(text.split())
                                summary_words = len(summary.split())
                                reduction_ratio = (1 - summary_words / original_words) * 100

                                col1, col2, col3, col4 = st.columns(4)
                                with col1:
                                    st.metric("📄 Original Words", f"{original_words:,}")
                                with col2:
                                    st.metric("📝 Summary Words", f"{summary_words:,}")
                                with col3:
                                    st.metric("📊 Reduction", f"{reduction_ratio:.1f}%")
                                with col4:
                                    st.metric("⏱️ Reading Time", f"~{summary_words // 200} min")

                                # Download options
                                if output_format == "Downloadable Text File":
                                    st.markdown("---")
                                    st.subheader("📥 Download Summary")

                                    # Create downloadable file
                                    summary_file_path = PDFSummarizer.create_summary_pdf(summary, "temp/summary.txt")

                                    if summary_file_path and os.path.exists(summary_file_path):
                                        with open(summary_file_path, 'rb') as f:
                                            summary_data = f.read()

                                        st.download_button(
                                            label="📄 Download Summary as Text File",
                                            data=summary_data,
                                            file_name=f"{uploaded_file.name.replace('.pdf', '_summary.txt')}",
                                            mime="text/plain",
                                            use_container_width=True
                                        )

                                # Action buttons
                                st.markdown("---")
                                col1, col2 = st.columns(2)
                                with col1:
                                    if st.button("🔄 Generate New Summary", use_container_width=True):
                                        st.experimental_rerun()
                                with col2:
                                    if st.button("📋 Copy Summary to Clipboard", use_container_width=True):
                                        # Note: Clipboard functionality requires JavaScript
                                        st.info("💡 Use Ctrl+A, Ctrl+C to copy the summary text above")

                            else:
                                st.error("❌ Failed to generate summary. The document might be too short or contain insufficient text.")

                        elif text:
                            st.error("❌ The extracted text is too short to summarize effectively. Please try a longer document.")
                        else:
                            st.error("❌ Could not extract readable text from the PDF. Please ensure the document contains selectable text.")

                    else:
                        st.error("❌ Failed to process the uploaded file.")

                except Exception as e:
                    st.error(f"❌ Error during summarization: {str(e)}")
                    st.error("This might be due to document complexity or format issues.")

                finally:
                    # Clean up temporary files
                    clean_temp_files("temp")

else:
    st.info("👆 Please upload a PDF document to start the summarization process.")

# Algorithm explanation
st.markdown("---")
st.markdown("""
<div class="main-container">
    <h3>🤖 How Our Summarization Works</h3>
    <p>Our intelligent summarization algorithm uses advanced natural language processing techniques:</p>
    <ol>
        <li><strong>Text Extraction:</strong> Extract and clean text content from PDF</li>
        <li><strong>Sentence Tokenization:</strong> Break text into individual sentences</li>
        <li><strong>Word Frequency Analysis:</strong> Calculate importance of words using TF-IDF</li>
        <li><strong>Sentence Scoring:</strong> Rank sentences based on word importance</li>
        <li><strong>Summary Generation:</strong> Select top-ranked sentences for final summary</li>
    </ol>
</div>
""", unsafe_allow_html=True)

# Sidebar help
st.sidebar.title("📋 PDF Summarizer Help")
st.sidebar.markdown("""
### How to Use:
1. **Upload** your PDF document
2. **Configure** summarization settings
3. **Choose** summary length and format
4. **Click** Generate Summary
5. **Review** and download results

### Best For:
- Research papers
- Business reports  
- Academic articles
- Legal documents
- Technical manuals

### Settings Guide:
- **Short:** Quick overview (3-5 sentences)
- **Medium:** Balanced summary (5-8 sentences)  
- **Long:** Detailed summary (8-12 sentences)
- **Custom:** Specify exact length

### Output Options:
- **Text:** View summary on screen
- **File:** Download as .txt file
- **Preview:** See original text extraction
""")
