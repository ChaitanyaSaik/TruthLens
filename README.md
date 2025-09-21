# 🛡️ TruthLens: An AI-Powered Tool for Combating Misinformation

[![Hackathon](https://img.shields.io/badge/Hackathon-Google%20GenAI%20Exchange-blue)](https://cloud.google.com/)
[![Language](https://img.shields.io/badge/Language-Python-brightgreen)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Streamlit-ff69b4)](https://streamlit.io/)
[![AI Model](https://img.shields.io/badge/AI%20Model-Gemini%201.5%20Flash-purple)](https://deepmind.google/technologies/gemini/)

[cite_start]**Team:** The Sweat and Success [cite: 5]
<br>
[cite_start]**Team Leader:** Chaitanya Sai Kurapati [cite: 6]

---

## 📄 Overview

[cite_start]TruthLens is an AI-powered toolkit designed to help users navigate the complex modern information landscape by detecting misinformation in real time[cite: 11]. [cite_start]Developed for the Google GenAI Exchange Hackathon [cite: 3, 10][cite_start], this prototype leverages the power of the Google Gemini LLM to analyze news articles, website credibility, images, and manipulative language without the need for traditional dataset training[cite: 14, 22]. [cite_start]Its core mission is to empower users by not just classifying content, but also explaining *why* it might be misleading and guiding them toward verified, trustworthy sources[cite: 13, 24].

## ✨ Key Features

TruthLens is a multi-functional platform offering a suite of specialized tools:

* **📝 Article Analysis:**
    * [cite_start]Paste a full news article to receive an instant analysis[cite: 12].
    * [cite_start]The tool classifies the content as `REAL`, `FAKE`, or `MISLEADING`[cite: 13, 29].
    * [cite_start]It provides a confidence score for its classification and a detailed explanation of its reasoning[cite: 32].

* **🌐 Source Credibility Checker:**
    * [cite_start]Enter a news website URL to evaluate the source's reputation[cite: 12, 61].
    * The tool returns a credibility rating (`Highly Credible`, `Mixed Credibility`, `Not Credible`) and a summary covering reputation, potential bias, and ownership.

* **🖼️ Image Authenticity Scan:**
    * [cite_start]Upload an image to check for misleading context or digital manipulation[cite: 12, 63].
    * The AI, acting as a visual forensics expert, analyzes if the image has been used in misinformation campaigns and assesses its likely origin and context.

* **🎯 Bias & Propaganda Analyzer:**
    * [cite_start]Paste any text to scan its language for manipulative techniques[cite: 65].
    * The tool identifies and quotes examples of emotional language, ad hominem attacks, loaded questions, false dichotomies, and other propaganda techniques.

## 🛠️ Technology Stack

The project is built with a modern, scalable, and efficient technology stack:

* [cite_start]**AI Engine:** Google Gemini LLM [cite: 92]
* [cite_start]**Frontend:** Streamlit [cite: 90]
* [cite_start]**Programming Language:** Python [cite: 94]
* **Core Libraries:**
    * [cite_start]`google-generativeai`[cite: 98]: The official Python SDK for the Gemini API.
    * `Pillow` (as `PIL` in `app.py`): For image processing.
    * [cite_start]`streamlit`[cite: 1]: For building the web application interface.
* [cite_start]**Deployment:** Designed for local hosting or deployment on Streamlit Cloud[cite: 99].

## 🏗️ Architecture

The application follows a simple yet powerful architecture:

1.  [cite_start]**User Interface (Streamlit):** The user provides input—an article, URL, or image—through the clean web interface[cite: 74].
2.  [cite_start]**Backend Orchestrator (`app.py`):** The Streamlit application code acts as the orchestrator[cite: 76]. It receives the user input and constructs a specific, detailed prompt.
3.  [cite_start]**Gemini LLM API:** The prompt and data are sent to the Gemini LLM API, which performs the core analysis and returns the structured output[cite: 82].
4.  [cite_start]**Output to User:** The backend parses the AI's response and presents the final results—classification, confidence scores, explanations, and bias detection—to the user in an easy-to-understand format[cite: 81, 86].



## 🚀 Getting Started

Follow these instructions to set up and run TruthLens on your local machine.

### Prerequisites

* Python 3.8+
* Git

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/truthlens.git](https://github.com/your-username/truthlens.git)
    cd truthlens
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    *(Note: The original `requirements.txt` file had a typo (`PIPImage`) which has been corrected to `Pillow` below).*
    ```bash
    pip install streamlit Pillow pandas numpy google-generativeai
    ```

4.  **Configure your Gemini API Key:**
    * Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
    * **IMPORTANT:** For security, do not hardcode your API key as seen in the example `app.py`. Instead, use Streamlit's secrets management.
    * Create a file: `.streamlit/secrets.toml`
    * Add your API key to this file:
        ```toml
        API_KEY = "YOUR_GEMINI_API_KEY_HERE"
        ```
    * Modify `app.py` to load the key securely:
        ```python
        # Replace the hardcoded key with this:
        try:
            API_KEY = st.secrets["API_KEY"]
            genai.configure(api_key=API_KEY)
        except Exception as e:
            st.error("🚨 API Key not found! Please add it to your .streamlit/secrets.toml file.", icon="🔥")
            st.stop()
        ```

### Running the Application

Once the setup is complete, run the following command in your terminal:

```bash
streamlit run app.py
Open your web browser and navigate to the local URL provided by Streamlit (usually http://localhost:8501).
```
### Future Vision
TruthLens aims to expand its reach and capabilities:
Browser Extension: Develop a browser plugin for real-time analysis of content as users browse the web.
Mobile Application: Create a dedicated mobile app for on-the-go fact-checking.
Multimedia Support: Enhance capabilities to analyze videos and other multimedia formats.
Social Media Integration: Build tools to directly integrate with social media platforms to flag misinformation at its source.
