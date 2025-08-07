
import io
import os
import tempfile
import PyPDF2
import pyttsx3
from gtts import gTTS
import speech_recognition as sr
import nltk
import pdfplumber
from fpdf import FPDF
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
from pydub import AudioSegment
import streamlit as st

# Download required NLTK data
try:
    nltk.download('punkt_tab', quiet=True)
    nltk.download('stopwords', quiet=True)
except:
    pass

class PDFToAudioConverter:
    """Handles PDF to Audio conversion"""

    @staticmethod
    def extract_text_from_pdf(pdf_file):
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            st.error(f"Error extracting text from PDF: {e}")
            return None

    @staticmethod
    def text_to_audio(text, output_path="output_audio.mp3", rate=200, volume=0.8):
        """Convert text to audio using gTTS"""
        try:
            tts = gTTS(text=text, lang='en')
            tts.save(output_path)
            return output_path
        except Exception as e:
            st.error(f"Error converting text to audio: {e}")
            return None

class TextToAudioConverter:
    """Handles Text to Audio conversion"""


    @staticmethod
    def convert_text_to_audio(text, output_path="text_audio.mp3", **kwargs):
        """Convert plain text to audio using gTTS"""
        try:
            tts = gTTS(text=text, lang='en')
            tts.save(output_path)
            return output_path
        except Exception as e:
            st.error(f"Error converting text to audio: {e}")
            return None


class PDFSummarizer:
    """Handles PDF text summarization"""

    @staticmethod
    def extract_text_with_pdfplumber(pdf_file):
        """Extract text using pdfplumber for better accuracy"""
        try:
            with pdfplumber.open(pdf_file) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            st.error(f"Error extracting text: {e}")
            return None

    @staticmethod
    def summarize_text(text, num_sentences=5):
        """Summarize text using NLTK"""
        try:
            # Tokenize sentences
            sentences = sent_tokenize(text)
            if len(sentences) <= num_sentences:
                return text

            # Tokenize words and remove stopwords
            stop_words = set(stopwords.words('english'))
            words = word_tokenize(text.lower())
            words = [word for word in words if word.isalnum() and word not in stop_words]

            # Calculate word frequency
            word_freq = Counter(words)

            # Score sentences
            sentence_scores = {}
            for i, sentence in enumerate(sentences):
                words_in_sentence = word_tokenize(sentence.lower())
                score = 0
                word_count = 0

                for word in words_in_sentence:
                    if word in word_freq:
                        score += word_freq[word]
                        word_count += 1

                if word_count > 0:
                    sentence_scores[i] = score / word_count

            # Get top sentences
            top_sentences = sorted(sentence_scores.items(), 
                                 key=lambda x: x[1], reverse=True)[:num_sentences]
            top_sentences = sorted([x[0] for x in top_sentences])

            # Create summary
            summary = ' '.join([sentences[i] for i in top_sentences])
            return summary

        except Exception as e:
            st.error(f"Error summarizing text: {e}")
            return None

    @staticmethod
    def create_summary_pdf(summary_text, output_path="summary.txt"):
        """Save summary as text file (PDF libraries need additional setup)"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("PDF SUMMARY\n")
                f.write("=" * 50 + "\n\n")
                f.write(summary_text)
            return output_path
        except Exception as e:
            st.error(f"Error creating summary file: {e}")
            return None

class AudioToPDFConverter:
    """Handles Audio to PDF conversion"""

    @staticmethod
    def convert_to_wav(input_path):
        """Convert any audio format to WAV"""
        try:
            audio = AudioSegment.from_file(input_path)
            wav_path = input_path.rsplit('.', 1)[0] + "_converted.wav"
            audio.export(wav_path, format="wav")
            return wav_path
        except Exception as e:
            st.error(f"Error converting audio to WAV: {e}")
            return None

    @staticmethod
    def audio_to_text(audio_file_path):
        """Convert audio to text using speech recognition"""
        try:
            r = sr.Recognizer()

            # Convert to WAV if necessary
            if not audio_file_path.lower().endswith(".wav"):
                audio_file_path = AudioToPDFConverter.convert_to_wav(audio_file_path)
                if audio_file_path is None:
                    return None

            with sr.AudioFile(audio_file_path) as source:
                r.adjust_for_ambient_noise(source, duration=1)
                audio = r.record(source)

            text = r.recognize_google(audio)
            return text

        except sr.UnknownValueError:
            st.error("❌ Could not understand the audio. Please try with clearer audio.")
            return None
        except sr.RequestError as e:
            st.error(f"❌ Error with the speech recognition service: {e}")
            return None
        except Exception as e:
            st.error(f"❌ Error processing audio: {e}")
            return None
    
    @staticmethod
    def text_to_file(text, output_path="audio_transcript.txt"):
        """Save transcribed text as .txt, .md, .rtf or .pdf"""
        try:
            ext = os.path.splitext(output_path)[1].lower()

            if ext in ['.txt', '.md', '.rtf']:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write("AUDIO TRANSCRIPT\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(text)

            elif ext == '.pdf':
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, "AUDIO TRANSCRIPT\n" + "=" * 50 + "\n\n" + text)
                pdf.output(output_path)

            else:
                raise ValueError("Unsupported file format")

            return output_path
        except Exception as e:
            st.error(f"Error saving file: {e}")
            return None


# Utility functions
def save_uploaded_file(uploaded_file, directory="temp"):
    """Save uploaded file to temporary directory"""
    try:
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return None

def clean_temp_files(directory="temp"):
    """Clean temporary files"""
    try:
        if os.path.exists(directory):
            for file in os.listdir(directory):
                os.remove(os.path.join(directory, file))
    except:
        pass
