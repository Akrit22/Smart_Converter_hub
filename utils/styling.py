
import streamlit as st
import base64

def get_base64_of_bin_file(bin_file):
    """Convert binary file to base64 string"""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background_image(image_path):
    """Set background image for the app"""
    try:
        bin_str = get_base64_of_bin_file(image_path)
        page_bg_img = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        .stApp > div:first-child {{
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(10px);
        }}

        /* Custom styling for containers */
        .main-container {{
            background: rgba(0, 0, 0, 0.7);
            padding: 2rem;
            border-radius: 15px;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}

        /* Header styling */
        .header-style {{
            background: linear-gradient(90deg, #4CAF50 0%, #2196F3 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 2rem;
        }}

        /* Card styling */
        .feature-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            color: white;
            text-align: center;
            transition: transform 0.2s ease;
        }}

        .feature-card:hover {{
            transform: translateY(-5px);
        }}

        /* Success/Error message styling */
        .success-msg {{
            background: linear-gradient(90deg, #4CAF50, #45a049);
            color: white;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }}

        .error-msg {{
            background: linear-gradient(90deg, #f44336, #da190b);
            color: white;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }}

        /* Button styling */
        .stButton > button {{
            background: linear-gradient(90deg, #4CAF50 0%, #2196F3 100%);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.5rem 2rem;
            font-weight: bold;
            transition: all 0.3s ease;
        }}

        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }}

        /* File uploader styling */
        .uploadedFile {{
            background: rgba(255, 255, 255, 0.9);
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
        }}

        </style>
        """
        st.markdown(page_bg_img, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Could not load background image: {e}")

def create_download_link(file_path, download_name):
    """Create a download link for files"""
    with open(file_path, "rb") as f:
        bytes_data = f.read()

    b64 = base64.b64encode(bytes_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{download_name}">Click here to download {download_name}</a>'
    return href

def show_feature_card(title, description, icon="🔄"):
    """Create a feature card"""
    st.markdown(f"""
    <div class="feature-card">
        <h3>{icon} {title}</h3>
        <p>{description}</p>
    </div>
    """, unsafe_allow_html=True)
