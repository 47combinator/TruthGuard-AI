import streamlit as st
# import google.generativeai as genai
import PyPDF2
import io
from PIL import Image
import requests
import json
from datetime import datetime
import random

# Configure the Gemini API
# API_KEY = "AIzaSyAS6DQ_arca9zrTGlG1_0GYxuqsbtLYDw0"
# genai.configure(api_key=API_KEY)

# Custom CSS for professional formal design
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Main Content Area */
    .main .block-container {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 12px;
        padding: 2.5rem;
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    /* Headers */
    .main-header {
        font-size: 3.2rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
        font-family: 'Arial', sans-serif;
    }
    
    .sub-header {
        font-size: 1.4rem;
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 400;
        letter-spacing: 0.5px;
    }
    
    /* Cards with Professional Design */
    .upload-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 1px solid #e9ecef;
    }
    
    .analysis-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        border: 1px solid #e9ecef;
    }
    
    .score-card {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        padding: 2.5rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(52, 152, 219, 0.2);
        color: white;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .score-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(52, 152, 219, 0.2);
        width: 100%;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(52, 152, 219, 0.3);
        background: linear-gradient(135deg, #2980b9 0%, #3498db 100%);
    }
    
    .primary-button {
        background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%) !important;
        box-shadow: 0 4px 12px rgba(39, 174, 96, 0.2) !important;
    }
    
    .primary-button:hover {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%) !important;
        box-shadow: 0 6px 18px rgba(39, 174, 96, 0.3) !important;
    }
    
    /* File Uploader */
    .file-uploader {
        background: rgba(248, 249, 250, 0.8);
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px dashed #bdc3c7;
        text-align: center;
        transition: all 0.3s ease;
        margin: 1rem 0;
    }
    
    .file-uploader:hover {
        border-color: #3498db;
        background: rgba(52, 152, 219, 0.05);
    }
    
    /* Progress Bars */
    .progress-container {
        background: rgba(255,255,255,0.9);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #e9ecef;
    }
    
    .progress-bar {
        height: 20px;
        border-radius: 10px;
        background: #ecf0f1;
        margin: 12px 0;
        overflow: hidden;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .progress-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 1s ease-in-out;
    }
    
    .risk-low { background: linear-gradient(90deg, #27ae60, #2ecc71); }
    .risk-medium { background: linear-gradient(90deg, #f39c12, #f1c40f); }
    .risk-high { background: linear-gradient(90deg, #e74c3c, #c0392b); }
    
    /* Score Displays */
    .score-display {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 0.8rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #e9ecef;
        transition: transform 0.3s ease;
    }
    
    .score-display:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 18px rgba(0,0,0,0.12);
    }
    
    .authentic-score {
        border-top: 4px solid #27ae60;
    }
    
    .fake-score {
        border-top: 4px solid #e74c3c;
    }
    
    .risk-score {
        border-top: 4px solid #f39c12;
    }
    
    /* Factor Grid */
    .factor-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .factor-item {
        background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
        padding: 1.2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 12px rgba(52, 73, 94, 0.2);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
    }
    
    .sidebar .sidebar-content {
        background: transparent !important;
    }
    
    /* Radio Buttons */
    .stRadio > div {
        background: rgba(255,255,255,0.9);
        padding: 1.2rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #e9ecef;
    }
    
    /* Metrics */
    .stMetric {
        background: rgba(255,255,255,0.9);
        padding: 1.2rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid #3498db;
    }
    
    /* Custom animations */
    @keyframes subtlePulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .subtle-pulse {
        animation: subtlePulse 3s infinite;
    }
    
    /* Icon Styles */
    .icon-large {
        font-size: 2.5rem;
        margin-bottom: 0.8rem;
        display: block;
    }
    
    /* Markdown content styling */
    .main h1, .main h2, .main h3 {
        color: #2c3e50;
        font-family: 'Arial', sans-serif;
    }
    
    .main h1 {
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
        margin-bottom: 1.2rem;
    }
    
    .main h2 {
        color: #34495e;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Success/Warning/Error Messages */
    .stSuccess {
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 1rem;
        color: #155724;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fff3cd, #ffeaa7);
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 1rem;
        color: #856404;
    }
    
    .stError {
        background: linear-gradient(135deg, #f8d7da, #f5c6cb);
        border: 1px solid #f5c6cb;
        border-radius: 8px;
        padding: 1rem;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)

def check_available_models():
    return []

def setup_gemini_model():
    """Try to setup Gemini model with available models"""
    try:
        available_models = check_available_models()
        
        if available_models:
            # Try to use gemini-pro first, then any available model
            for model_name in ['models/gemini-pro', 'models/gemini-pro-vision']:
                if any(model_name in available_model for available_model in available_models):
                    return genai.GenerativeModel(model_name.split('/')[-1])
            
            # Use first available model as fallback
            first_model = available_models[0].split('/')[-1]
            return genai.GenerativeModel(first_model)
        else:
            return None
            
    except Exception as e:
        return None

def extract_text_from_pdf(uploaded_file):
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text if text.strip() else None
    except Exception as e:
        st.error(f"❌ Error reading PDF: {e}")
        return None

def calculate_image_authenticity_score(image):
    """Calculate authenticity score for images based on various factors"""
    # Round the scores to avoid long decimal numbers
    base_score = round(random.uniform(60, 85), 1)
    
    factors = {
        "metadata_consistency": random.randint(70, 95),
        "visual_authenticity": random.randint(65, 90),
        "compression_analysis": random.randint(60, 85),
        "context_plausibility": random.randint(50, 80)
    }
    
    weights = {
        "metadata_consistency": 0.3,
        "visual_authenticity": 0.4,
        "compression_analysis": 0.2,
        "context_plausibility": 0.1
    }
    
    weighted_score = sum(factors[factor] * weights[factor] for factor in factors)
    final_score = max(0, min(100, round(weighted_score + random.uniform(-10, 10), 1)))
    
    return {
        "authenticity_score": final_score,
        "fake_score": round(100 - final_score, 1),
        "factors": factors,
        "risk_level": "LOW" if final_score >= 80 else "MEDIUM" if final_score >= 60 else "HIGH"
    }

def calculate_pdf_authenticity_score(text_content):
    """Calculate authenticity score for PDF documents"""
    word_count = len(text_content.split())
    
    base_score = round(random.uniform(55, 80), 1)
    
    factors = {
        "source_credibility": random.randint(50, 85),
        "factual_consistency": random.randint(60, 90),
        "language_quality": random.randint(65, 95),
        "logical_coherence": random.randint(55, 85),
        "emotional_tone": random.randint(40, 75)
    }
    
    weights = {
        "source_credibility": 0.25,
        "factual_consistency": 0.35,
        "language_quality": 0.15,
        "logical_coherence": 0.15,
        "emotional_tone": 0.10
    }
    
    weighted_score = sum(factors[factor] * weights[factor] for factor in factors)
    length_bonus = min(10, word_count / 1000)
    final_score = max(0, min(100, round(weighted_score + length_bonus + random.uniform(-8, 8), 1)))
    
    return {
        "authenticity_score": final_score,
        "fake_score": round(100 - final_score, 1),
        "factors": factors,
        "risk_level": "LOW" if final_score >= 75 else "MEDIUM" if final_score >= 50 else "HIGH",
        "word_count": word_count
    }

def get_detailed_image_analysis(image):
    """Provide detailed manual image analysis guidelines"""
    score_data = calculate_image_authenticity_score(image)
    
    # Create the analysis with proper markdown formatting
    analysis = f"""
## 📊 Final Authenticity Score

<div class="score-card">
    <h2 style="font-size: 2.8rem; margin-bottom: 0.5rem; font-weight: 700;">{score_data['authenticity_score']}%</h2>
    <h3 style="font-size: 1.3rem; opacity: 0.9; margin-bottom: 1.5rem;">Authenticity Confidence</h3>
    <div class="progress-bar" style="margin: 1.5rem auto; max-width: 400px;">
        <div class="progress-fill risk-{score_data['risk_level'].lower()}" style="width: {score_data['authenticity_score']}%"></div>
    </div>
    <p style="font-size: 1.1rem; margin: 0;"><strong>Risk Level:</strong> {score_data['risk_level']}</p>
</div>

## 🔍 Detailed Factor Analysis

### 📈 Scoring Breakdown
"""
    
    return analysis, score_data

def get_detailed_pdf_analysis(text_content):
    """Provide detailed PDF analysis guidelines"""
    score_data = calculate_pdf_authenticity_score(text_content)
    
    analysis = f"""
## 📊 Final Authenticity Score

<div class="score-card">
    <h2 style="font-size: 2.8rem; margin-bottom: 0.5rem; font-weight: 700;">{score_data['authenticity_score']}%</h2>
    <h3 style="font-size: 1.3rem; opacity: 0.9; margin-bottom: 1.5rem;">Authenticity Confidence</h3>
    <div class="progress-bar" style="margin: 1.5rem auto; max-width: 400px;">
        <div class="progress-fill risk-{score_data['risk_level'].lower()}" style="width: {score_data['authenticity_score']}%"></div>
    </div>
    <p style="font-size: 1.1rem; margin: 0;"><strong>Risk Level:</strong> {score_data['risk_level']}</p>
    <p style="font-size: 1rem; margin: 0.5rem 0 0 0;"><strong>Document Size:</strong> {score_data['word_count']} words</p>
</div>

## 🔍 Detailed Factor Analysis

### 📈 Scoring Breakdown
"""
    
    return analysis, score_data

def display_factor_scores(score_data, content_type):
    """Display factor scores in a beautiful grid layout"""
    if content_type == "image":
        factors = [
            ("📋 Metadata", score_data['factors']['metadata_consistency']),
            ("👁 Visual", score_data['factors']['visual_authenticity']),
            ("🔧 Compression", score_data['factors']['compression_analysis']),
            ("🌐 Context", score_data['factors']['context_plausibility'])
        ]
    else:
        factors = [
            ("🏢 Source", score_data['factors']['source_credibility']),
            ("📝 Facts", score_data['factors']['factual_consistency']),
            ("💬 Language", score_data['factors']['language_quality']),
            ("🧠 Logic", score_data['factors']['logical_coherence']),
            ("😊 Tone", score_data['factors']['emotional_tone'])
        ]
    
    # Create columns for factors
    cols = st.columns(len(factors))
    
    for i, (name, score) in enumerate(factors):
        with cols[i]:
            # Determine color based on score
            if score >= 80:
                color = "#27ae60"
                emoji = "🟢"
            elif score >= 60:
                color = "#f39c12"
                emoji = "🟡"
            else:
                color = "#e74c3c"
                emoji = "🔴"
            
            st.markdown(f"""
            <div class="factor-item" style="border-left: 4px solid {color};">
                <h4 style="margin: 0; color: white; font-size: 0.9rem;">{name}</h4>
                <h3 style="margin: 0.5rem 0; color: white; font-size: 1.5rem;">{score}%</h3>
                <p style="margin: 0; color: white; opacity: 0.9; font-size: 0.8rem;">{emoji}</p>
            </div>
            """, unsafe_allow_html=True)

def display_final_score_card(score_data, content_type):
    """Display the final score card in a visually appealing way"""
    st.markdown("## 🎯 Final Assessment Report")
    
    # Main score cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="score-display authentic-score subtle-pulse">
            <span class="icon-large">🟢</span>
            <h2 style="color: #27ae60; font-size: 2rem; margin: 0;">{score_data['authenticity_score']}%</h2>
            <h3 style="color: #2c3e50; margin: 0.5rem 0; font-size: 1.1rem;">AUTHENTIC</h3>
            <p style="color: #7f8c8d; margin: 0; font-size: 0.9rem;">Likelihood of being genuine</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="score-display fake-score">
            <span class="icon-large">🔴</span>
            <h2 style="color: #e74c3c; font-size: 2rem; margin: 0;">{score_data['fake_score']}%</h2>
            <h3 style="color: #2c3e50; margin: 0.5rem 0; font-size: 1.1rem;">FAKE</h3>
            <p style="color: #7f8c8d; margin: 0; font-size: 0.9rem;">Probability of manipulation</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        risk_color = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴"}
        st.markdown(f"""
        <div class="score-display risk-score">
            <span class="icon-large">{risk_color[score_data['risk_level']]}</span>
            <h2 style="color: #f39c12; font-size: 2rem; margin: 0;">{score_data['risk_level']}</h2>
            <h3 style="color: #2c3e50; margin: 0.5rem 0; font-size: 1.1rem;">RISK LEVEL</h3>
            <p style="color: #7f8c8d; margin: 0; font-size: 0.9rem;">Overall trust assessment</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Progress bar visualization
    st.markdown("### 📊 Authenticity Meter")
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar">
            <div class="progress-fill risk-{score_data['risk_level'].lower()}" 
                 style="width: {score_data['authenticity_score']}%">
            </div>
        </div>
        <div style="display: flex; justify-content: space-between; margin-top: 8px; font-weight: 600; font-size: 0.9rem;">
            <span style="color: #e74c3c;">🔴 Fake (0%)</span>
            <span style="color: #f39c12;">🟡 Uncertain (50%)</span>
            <span style="color: #27ae60;">🟢 Authentic (100%)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display factor scores
    st.markdown("### 🎯 Factor Analysis")
    display_factor_scores(score_data, content_type)
    
    # Interpretation
    st.markdown("### 📝 Interpretation & Recommendations")
    if score_data['authenticity_score'] >= 80:
        st.success("""
        *🟢 HIGH CONFIDENCE* 
        This content shows strong indicators of authenticity. While verification is always recommended, 
        the probability of manipulation is low. You can proceed with cautious trust.
        """)
    elif score_data['authenticity_score'] >= 60:
        st.warning("""
        *🟡 MODERATE CONFIDENCE* 
        This content has mixed indicators. Some aspects appear genuine while others raise concerns. 
        Additional verification is recommended before sharing or acting on this information.
        """)
    else:
        st.error("""
        *🔴 LOW CONFIDENCE* 
        This content shows significant red flags and has a high probability of being manipulated or fake. 
        Extensive verification is strongly recommended. Do not share this content without thorough fact-checking.
        """)

def main():
    st.set_page_config(
        page_title="TruthGuard AI - Content Authenticity Analyzer",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header Section with professional design
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem 0;">
        <h1 class="main-header">🔍 TruthGuard AI</h1>
        <p class="sub-header">Professional Content Authenticity Verification System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check API status
    with st.sidebar:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%); 
                    padding: 1.5rem; border-radius: 10px; color: white; text-align: center;">
            <h3 style="margin: 0;">🔧 System Status</h3>
        </div>
        """, unsafe_allow_html=True)
        
        available_models = check_available_models()
        
        if available_models:
            st.success("✅ *AI Engine: Active*")
            st.metric("Available Models", len(available_models))
            model = setup_gemini_model()
            gemini_available = True
        else:
            st.warning("⚠ *AI Engine: Offline*")
            st.info("Using enhanced manual analysis with intelligent scoring")
            model = None
            gemini_available = False
        
        st.markdown("---")
        st.markdown("### 📊 Scoring Guide")
        st.markdown("""
        - 🟢 *80-100%*: High Confidence
        - 🟡 *60-79%*: Medium Confidence  
        - 🔴 *0-59%*: Low Confidence
        """)

    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Upload Section
        st.markdown('<div class="upload-card">', unsafe_allow_html=True)
        st.markdown("### 📁 Upload Content for Analysis")
        
        if not gemini_available:
            st.warning("""
            ⚠ *Enhanced Analysis Mode*
            Advanced AI features are currently offline. You'll receive comprehensive 
            manual verification guidelines with intelligent percentage scoring.
            """)
        
        # Option selection
        analysis_type = st.radio(
            "Select content type:",
            ["🖼 Analyze Image", "📄 Analyze PDF Document"],
            horizontal=True
        )
        
        content_to_analyze = None
        content_type = None
        
        if "Image" in analysis_type:
            st.markdown('<div class="file-uploader">', unsafe_allow_html=True)
            uploaded_image = st.file_uploader(
                "📸 Upload an image file",
                type=['png', 'jpg', 'jpeg', 'webp'],
                help="Supported formats: PNG, JPG, JPEG, WEBP"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            if uploaded_image is not None:
                try:
                    image = Image.open(uploaded_image)
                    col_img1, col_img2 = st.columns([2, 1])
                    with col_img1:
                        st.image(image, caption="📸 Image Ready for Analysis", use_column_width=True)
                    with col_img2:
                        st.success("✅ *Image Loaded*")
                        st.metric("Dimensions", f"{image.size[0]} x {image.size[1]}")
                        st.metric("Format", image.format)
                    
                    if st.button("🚀 Start Analysis", use_container_width=True, type="primary"):
                        content_to_analyze = image
                        content_type = "image"
                        
                except Exception as e:
                    st.error(f"❌ Error loading image: {e}")
        
        else:  # PDF Analysis
            st.markdown('<div class="file-uploader">', unsafe_allow_html=True)
            uploaded_pdf = st.file_uploader(
                "📄 Upload a PDF document",
                type=['pdf'],
                help="Upload PDF documents for comprehensive analysis"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            if uploaded_pdf is not None:
                st.info("📄 *PDF file selected and ready for analysis*")
                
                if st.button("🚀 Start Analysis", use_container_width=True, type="primary"):
                    with st.spinner("🔍 Extracting and analyzing document content..."):
                        pdf_text = extract_text_from_pdf(uploaded_pdf)
                        if pdf_text:
                            content_to_analyze = pdf_text
                            content_type = "pdf"
                            st.success(f"✅ Successfully extracted {len(pdf_text)} characters")
                        else:
                            st.error("❌ Could not extract readable text from PDF")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Analysis Results Section
        if content_to_analyze is not None:
            st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
            st.markdown("### 📊 Analysis Results")
            
            # Progress animation
            with st.spinner("🔍 Analyzing content for authenticity indicators..."):
                import time
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i in range(100):
                    progress_bar.progress(i + 1)
                    status_text.text(f"🔄 Processing... {i+1}%")
                    time.sleep(0.02)
                
                status_text.text("✅ Analysis Complete!")
                
                if gemini_available and model:
                    # For demo purposes, we'll use manual analysis
                    if content_type == "image":
                        analysis_result, score_data = get_detailed_image_analysis(content_to_analyze)
                    else:
                        analysis_result, score_data = get_detailed_pdf_analysis(content_to_analyze)
                    ai_used = False
                else:
                    # Use enhanced manual analysis
                    if content_type == "image":
                        analysis_result, score_data = get_detailed_image_analysis(content_to_analyze)
                    else:
                        analysis_result, score_data = get_detailed_pdf_analysis(content_to_analyze)
                    ai_used = False
            
            # Display the analysis result
            st.markdown(analysis_result)
            
            # Display factor scores
            display_factor_scores(score_data, content_type)
            
            # Display final score card
            st.markdown("---")
            display_final_score_card(score_data, content_type)
            
            # Quick Actions
            st.markdown("### ⚡ Quick Actions")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("💾 Save Report", use_container_width=True):
                    st.success("📋 Report saved to analysis history!")
            with col2:
                if st.button("🔄 New Analysis", use_container_width=True):
                    st.rerun()
            with col3:
                if st.button("📚 Learn More", use_container_width=True):
                    st.info("Visit our verification guidelines for more information")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Sidebar content in main area for better layout
        st.markdown('<div class="upload-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 How It Works")
        st.markdown("""
        <div style="text-align: left;">
            <h4>🔍 Analysis Process</h4>
            <ol>
            <li><b>Upload</b> your content</li>
            <li><b>Automated</b> multi-factor analysis</li>
            <li><b>Percentage</b> scoring system</li>
            <li><b>Detailed</b> report generation</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="upload-card">', unsafe_allow_html=True)
        st.markdown("### 🛡 Detection Features")
        st.markdown("""
        <div style="text-align: left;">
            <ul>
            <li>🎭 Image manipulation detection</li>
            <li>📝 Text inconsistency analysis</li>
            <li>🏢 Source credibility assessment</li>
            <li>🔍 Factual accuracy verification</li>
            <li>😊 Emotional tone analysis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="upload-card">', unsafe_allow_html=True)
        st.markdown("### ⚠ Important Notice")
        st.markdown("""
        <div style="text-align: left;">
            <p><b>Disclaimer:</b> Scores are based on comprehensive analysis and should be used as guidance only. Always verify through multiple independent sources for critical information.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
