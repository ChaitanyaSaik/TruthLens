import streamlit as st
import os
import google.generativeai as genai
import json
from PIL import Image
import io

# --- 1. Gemini API & Page Configuration ---
st.set_page_config(page_title="TruthLens Toolkit", layout="wide", initial_sidebar_state="expanded")

# --- Custom CSS for a more polished, professional design ---
st.markdown("""
<style>
    /* Main app styling */
    .stApp {
        background-color: #f0f2f6; /* Light grey background */
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
    }

    /* Main content styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Custom title styling */
    .title-text {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a1a;
        padding-bottom: 1rem;
    }
    
    /* Custom header for each tool */
    .tool-header {
        font-size: 1.75rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 1rem;
    }

</style>
""", unsafe_allow_html=True)

try:
    API_KEY = "AIzaSyCKqZMTfA_AH0llqCTqeBhPZK4boBm97oc"
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"🚨 Error configuring the Gemini API: {e}", icon="🔥")
    st.stop()

# Function to initialize models
def get_model(model_name="gemini-1.5-flash"):
    return genai.GenerativeModel(model_name)

# --- (PAGE 1) Article Analysis ---
def page_article_analysis():
    st.title('TruthLens (AI-Powered Tool for Combating Misinformation)')
    st.markdown('<p class="tool-header">📝 Article Analysis</p>', unsafe_allow_html=True)
    with st.container(border=True):
        user_input_article = st.text_area("Paste the full news article here:", height=250, key="article_input", label_visibility="collapsed")
        if st.button("Perform Full Analysis", key="analyze_article", type="primary", use_container_width=True):
            if not user_input_article.strip():
                st.warning("Please paste an article to analyze.", icon="⚠️")
            else:
                with st.spinner("Performing unified AI analysis..."):
                    model = get_model()
                    prompt = (
                        "You are an expert fact-checker. Analyze the news text and respond with a single, clean JSON object with keys 'classification', 'confidence', and 'explanation'.\n"
                        "1. 'classification': 'REAL', 'FAKE', or 'MISLEADING'.\n"
                        "2. 'confidence': A float score between 0.0 and 1.0.\n"
                        "3. 'explanation': A detailed markdown explanation.\n\n"
                        f"--- News Text to Analyze ---\n{user_input_article}"
                    )
                    try:
                        response = model.generate_content(prompt)
                        clean_response = response.text.strip().replace("```json", "").replace("```", "")
                        result = json.loads(clean_response)
                        
                        st.divider()
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            label = result.get("classification", "Error")
                            confidence = float(result.get("confidence", 0.0))
                            
                            if label == "FAKE": st.error(f"**Classification: {label}**", icon="❌")
                            elif label == "REAL": st.success(f"**Classification: {label}**", icon="✅")
                            else: st.warning(f"**Classification: {label}**", icon="⚠️")
                            
                            st.metric(label="Confidence Score", value=f"{confidence:.1%}")
                            st.progress(confidence)

                        with col2: st.markdown(result.get("explanation", "Could not generate explanation."))
                    except (json.JSONDecodeError, KeyError) as e:
                        st.error(f"Could not parse the AI's response. Error: {e}")
                        st.code(response.text)

# --- (PAGE 2) Source Credibility ---
def page_source_credibility():
    st.title('TruthLens (AI-Powered Tool for Combating Misinformation)')
    st.markdown('<p class="tool-header">🌐 Source Credibility Checker</p>', unsafe_allow_html=True)
    with st.container(border=True):
        user_input_url = st.text_input("Enter a news website URL (e.g., bbc.com, cnn.com):", key="url_input", label_visibility="collapsed")
        if st.button("Check Source Credibility", key="check_source", type="primary", use_container_width=True):
            if not user_input_url.strip():
                st.warning("Please enter a URL to check.", icon="⚠️")
            else:
                with st.spinner(f"Analyzing credibility of {user_input_url}..."):
                    model = get_model()
                    prompt = (
                        "You are a media analyst. Analyze the credibility of the news source URL provided. Respond with a single JSON object with keys 'rating' and 'summary'.\n"
                        "1. 'rating': 'Highly Credible', 'Mixed Credibility', 'Not Credible', or 'Unknown'.\n"
                        "2. 'summary': A markdown explanation covering reputation, bias, and ownership.\n\n"
                        f"--- URL to Analyze ---\n{user_input_url}"
                    )
                    try:
                        response = model.generate_content(prompt)
                        clean_response = response.text.strip().replace("```json", "").replace("```", "")
                        result = json.loads(clean_response)
                        
                        st.divider()
                        st.metric(label="Credibility Rating", value=result.get('rating', 'Error'))
                        st.markdown(result.get("summary", "Could not generate summary."))
                    except (json.JSONDecodeError, KeyError) as e:
                        st.error(f"Could not parse the AI's response. Error: {e}")
                        st.code(response.text)

# --- (PAGE 3) Image Authenticity ---
def page_image_authenticity():
    st.title('TruthLens (AI-Powered Tool for Combating Misinformation)')
    st.markdown('<p class="tool-header">🖼️ Image Authenticity Scan</p>', unsafe_allow_html=True)
    with st.container(border=True):
        uploaded_image = st.file_uploader("Upload an image to check for misleading context or manipulation", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
        if uploaded_image is not None:
            st.image(uploaded_image, caption="Image to be analyzed", use_column_width=True)
            if st.button("Analyze Image", key="analyze_image", type="primary", use_container_width=True):
                with st.spinner("Scanning image context and authenticity..."):
                    model = get_model("gemini-1.5-flash") # Vision model
                    image = Image.open(uploaded_image)
                    prompt = (
                        "You are a visual forensics expert. Analyze this image. Has it been used in prominent misinformation campaigns? "
                        "Are there signs of digital alteration? Describe the image's likely origin and context. "
                        "Provide a brief, clear summary of your findings in markdown."
                    )
                    try:
                        response = model.generate_content([prompt, image])
                        st.divider()
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Could not analyze the image. Error: {e}")

# --- (PAGE 4) Bias & Propaganda ---
def page_bias_analyzer():
    st.title('TruthLens (AI-Powered Tool for Combating Misinformation)')
    st.markdown('<p class="tool-header">🎯 Bias & Propaganda Analyzer</p>', unsafe_allow_html=True)
    with st.container(border=True):
        user_input_bias = st.text_area("Paste text here to analyze its language for manipulative techniques:", height=250, key="bias_input", label_visibility="collapsed")
        if st.button("Analyze for Bias", key="analyze_bias", type="primary", use_container_width=True):
            if not user_input_bias.strip():
                st.warning("Please enter text to analyze.", icon="⚠️")
            else:
                with st.spinner("Scanning for manipulative language..."):
                    model = get_model()
                    prompt = (
                        "You are an expert in linguistics. Analyze the text to identify manipulative techniques like 'emotional language', 'ad hominem attacks', 'loaded questions', or 'false dichotomies'. "
                        "For each technique, provide the quote. Present findings as a markdown-formatted list."
                        f"\n\n--- Text to Analyze ---\n{user_input_bias}"
                    )
                    try:
                        response = model.generate_content(prompt)
                        st.divider()
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"An error occurred. Error: {e}")

# --- Main App Router ---
with st.sidebar:
    st.markdown('<p class="title-text">🛡️ TruthLens (AI-Powered Tool for Combating Misinformation) </p>', unsafe_allow_html=True)
    st.markdown("Your AI-powered toolkit for navigating the complex information landscape.")
    st.divider()
    
    page = st.radio("Choose a tool:",
                    ["Article Analysis", "Source Credibility", "Image Authenticity", "Bias & Propaganda"],
                    captions=["Analyze article text", "Check website reputation", "Verify image context", "Detect manipulative language"])
    
    st.divider()
    st.info("This project was developed for the Google GenAI Hackathon.")

if page == "Article Analysis":
    page_article_analysis()
elif page == "Source Credibility":
    page_source_credibility()
elif page == "Image Authenticity":
    page_image_authenticity()
elif page == "Bias & Propaganda":
    page_bias_analyzer()

