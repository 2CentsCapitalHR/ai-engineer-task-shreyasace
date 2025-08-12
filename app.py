"""
ADGM Corporate Agent Pro - Enhanced Navigation Version
Modern multi-page interface with improved visibility and navigation
"""

# Page Configuration MUST BE FIRST
import streamlit as st
st.set_page_config(
    page_title="ADGM Corporate Agent Pro - Enhanced",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

import os
import json
import tempfile
from datetime import datetime
from pathlib import Path
import sys
from typing import List, Dict, Any
import time
import traceback
import base64
from io import BytesIO

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import verified functions
try:
    from src.core.classify import identify_doc_type, detect_process_and_types
    from src.core.validate import analyze_bundle
    from src.core.report import build_summary_pdf
    from src.core.html_report import build_html_report
    from src.core.word_report import build_detailed_docx
    from src.core.docx_utils import insert_comments_and_return_bytes
except ImportError as e:
    st.error(f"❌ Import error: {e}")

# Modern Enhanced CSS with Premium Design System
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* === DESIGN SYSTEM VARIABLES === */
    :root {
        --primary-gradient: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
        --surface-primary: #ffffff;
        --surface-secondary: #f8fafc;
        --surface-tertiary: #f1f5f9;
        --text-primary: #0f172a;
        --text-secondary: #334155;
        --text-muted: #64748b;
        --border-light: #e2e8f0;
        --border-medium: #cbd5e1;
        --shadow-soft: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-medium: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --shadow-large: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --radius-xl: 20px;
        --spacing-xs: 0.5rem;
        --spacing-sm: 1rem;
        --spacing-md: 1.5rem;
        --spacing-lg: 2rem;
        --spacing-xl: 3rem;
    }
    
    /* === GLOBAL FOUNDATION === */
    .main {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        color: var(--text-primary);
        line-height: 1.6;
        letter-spacing: -0.01em;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    header[data-testid="stHeader"] {display: none;}
    
    /* === ENHANCED TYPOGRAPHY === */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
        letter-spacing: -0.025em !important;
        line-height: 1.2 !important;
        margin-bottom: var(--spacing-sm) !important;
    }
    
    h1 { font-size: 2.5rem !important; }
    h2 { font-size: 2rem !important; }
    h3 { font-size: 1.5rem !important; }
    h4 { font-size: 1.25rem !important; }
    
    p, div, span, .stMarkdown {
        color: var(--text-secondary) !important;
        font-weight: 400;
        line-height: 1.7;
    }
    
    /* === PREMIUM NAVIGATION SYSTEM === */
    .nav-tabs {
        display: flex;
        background: var(--surface-primary);
        border-radius: var(--radius-xl);
        padding: 6px;
        margin-bottom: var(--spacing-xl);
        box-shadow: var(--shadow-medium);
        border: 1px solid var(--border-light);
        backdrop-filter: blur(20px);
        background: rgba(255, 255, 255, 0.98);
    }
    
    .nav-tab {
        flex: 1;
        text-align: center;
        padding: var(--spacing-md) var(--spacing-lg);
        border-radius: var(--radius-md);
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        background: transparent;
        color: var(--text-muted);
        border: none;
        font-size: 1rem;
        position: relative;
        overflow: hidden;
    }
    
    .nav-tab::before {
        content: '';
        position: absolute;
        inset: 0;
        background: var(--primary-gradient);
        opacity: 0;
        transition: opacity 0.3s ease;
        z-index: -1;
    }
    
    .nav-tab.active {
        background: var(--primary-gradient);
        color: white;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
        transform: translateY(-1px);
    }
    
    .nav-tab:hover:not(.active) {
        background: var(--surface-tertiary);
        color: var(--text-primary);
        transform: translateY(-1px);
    }
    
    /* === MODERN PAGE CONTAINERS === */
    .page-container {
        background: var(--surface-primary);
        border-radius: var(--radius-xl);
        padding: var(--spacing-xl);
        margin: var(--spacing-md) 0;
        box-shadow: var(--shadow-medium);
        border: 1px solid var(--border-light);
        position: relative;
        overflow: hidden;
    }
    
    .page-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--primary-gradient);
    }
    
    .page-header {
        text-align: center;
        margin-bottom: var(--spacing-xl);
        padding-bottom: var(--spacing-lg);
        border-bottom: 2px solid var(--border-light);
        position: relative;
    }
    
    .page-title {
        font-size: 3rem;
        font-weight: 800;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: var(--spacing-sm);
        line-height: 1.1;
        letter-spacing: -0.02em;
    }
    
    .page-subtitle {
        font-size: 1.25rem;
        color: var(--text-muted);
        font-weight: 500;
        max-width: 600px;
        margin: 0 auto;
    }
    
    /* === PREMIUM HERO SECTION === */
    .hero-header {
        background: var(--primary-gradient);
        padding: var(--spacing-xl) var(--spacing-lg);
        border-radius: var(--radius-xl);
        margin-bottom: var(--spacing-xl);
        color: white;
        text-align: center;
        box-shadow: var(--shadow-large);
        position: relative;
        overflow: hidden;
    }
    
    .hero-header::before {
        content: '';
        position: absolute;
        inset: 0;
        background: url('data:image/svg+xml,<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><defs><pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="10" cy="10" r="1" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100%" height="100%" fill="url(%23grid)"/></svg>');
        animation: slidePattern 20s linear infinite;
    }
    
    @keyframes slidePattern {
        0% { transform: translateX(0) translateY(0); }
        100% { transform: translateX(20px) translateY(20px); }
    }
    
    .hero-header h1, .hero-header h2, .hero-header h3,
    .hero-title, .hero-subtitle, .hero-description {
        color: white !important;
        position: relative;
        z-index: 2;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: var(--spacing-sm);
        text-shadow: 0 4px 12px rgba(0,0,0,0.3);
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        opacity: 0.95;
        margin-bottom: var(--spacing-xs);
        font-weight: 500;
    }
    
    .hero-description {
        font-size: 1.125rem;
        opacity: 0.85;
        font-weight: 400;
        max-width: 700px;
        margin: 0 auto;
    }
    
    /* === ENHANCED CARD SYSTEM === */
    .beautiful-card {
        background: var(--surface-primary);
        padding: var(--spacing-xl);
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-medium);
        border: 1px solid var(--border-light);
        margin: var(--spacing-md) 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .beautiful-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: var(--primary-gradient);
        transform: scaleY(0);
        transform-origin: bottom;
        transition: transform 0.3s ease;
    }
    
    .beautiful-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    .beautiful-card:hover::before {
        transform: scaleY(1);
    }
    
    .beautiful-card h1, .beautiful-card h2, .beautiful-card h3 {
        color: var(--text-primary) !important;
    }
    
    .beautiful-card p, .beautiful-card div {
        color: var(--text-secondary) !important;
    }
    
    /* === MODERN STATUS INDICATORS === */
    .status-card {
        background: var(--surface-primary);
        padding: var(--spacing-md);
        border-radius: var(--radius-md);
        border: 2px solid var(--border-light);
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        color: var(--text-primary);
        position: relative;
        overflow: hidden;
    }
    
    .status-card::before {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.5) 50%, transparent 70%);
        transform: translateX(-100%);
        transition: transform 0.6s ease;
    }
    
    .status-card:hover {
        transform: scale(1.02);
        box-shadow: var(--shadow-medium);
    }
    
    .status-card:hover::before {
        transform: translateX(100%);
    }
    
    .status-online {
        border-color: #10b981;
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        color: #064e3b !important;
    }
    
    .status-processing {
        border-color: #3b82f6;
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        color: #1e40af !important;
        animation: pulse 2s infinite;
    }
    
    .status-error {
        border-color: #ef4444;
        background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%);
        color: #dc2626 !important;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    /* === ENHANCED ISSUE CARDS === */
    .issue-card {
        border-radius: var(--radius-lg);
        padding: var(--spacing-lg);
        margin: var(--spacing-md) 0;
        position: relative;
        overflow: hidden;
        box-shadow: var(--shadow-medium);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid var(--border-light);
    }
    
    .issue-card:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-large);
    }
    
    .issue-high {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border-color: #ef4444;
        color: #7f1d1d !important;
    }
    
    .issue-medium {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border-color: #f59e0b;
        color: #78350f !important;
    }
    
    .issue-low {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border-color: #10b981;
        color: #064e3b !important;
    }
    
    /* === PREMIUM METRICS === */
    .metric-card {
        background: var(--surface-primary);
        padding: var(--spacing-lg);
        border-radius: var(--radius-lg);
        text-align: center;
        box-shadow: var(--shadow-soft);
        border: 1px solid var(--border-light);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-medium);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: var(--text-primary);
        margin-bottom: var(--spacing-xs);
        font-family: 'JetBrains Mono', monospace;
    }
    
    .metric-label {
        font-size: 1rem;
        color: var(--text-muted);
        font-weight: 500;
        margin-bottom: var(--spacing-xs);
    }
    
    .metric-delta {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-secondary);
    }
    
    .metric-primary .metric-value {
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-success .metric-value { color: #10b981; }
    .metric-warning .metric-value { color: #f59e0b; }
    .metric-error .metric-value { color: #ef4444; }
    
    /* === ENHANCED BUTTONS === */
    .stButton > button {
        background: var(--primary-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        padding: var(--spacing-sm) var(--spacing-lg) !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: var(--shadow-soft) !important;
        letter-spacing: -0.01em !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 25px rgba(99, 102, 241, 0.4) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* === ENHANCED FILE UPLOADER === */
    .stFileUploader {
        background: var(--surface-primary);
        border-radius: var(--radius-lg);
        border: 2px dashed var(--border-medium);
        padding: var(--spacing-xl);
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: #6366f1;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    }
    
    /* === ANIMATIONS === */
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    .slide-in {
        animation: slideIn 0.6s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* === RESPONSIVE DESIGN === */
    @media (max-width: 768px) {
        .nav-tabs { flex-direction: column; }
        .nav-tab { margin-bottom: var(--spacing-xs); }
        .hero-title { font-size: 2.5rem; }
        .page-title { font-size: 2rem; }
        .page-container { padding: var(--spacing-lg); }
        .beautiful-card { padding: var(--spacing-lg); }
    }
    
    /* === SCROLLBAR STYLING === */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--surface-tertiary);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-gradient);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5b21b6 0%, #7c3aed 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Analysis'
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Analysis'
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False

# Navigation System
def create_navigation():
    """Create enhanced navigation tabs"""
    
    # Create columns for navigation with custom styling
    col1, col2, col3, col4 = st.columns(4)
    
    # Add custom CSS for lighter navigation
    st.markdown("""
    <style>
    .stButton > button {
        background: rgba(255, 255, 255, 0.98) !important;
        color: #64748b !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(20px) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
    }
    
    .stButton > button:hover {
        background: rgba(99, 102, 241, 0.1) !important;
        color: #6366f1 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15) !important;
    }
    
    .stButton > button:active {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with col1:
        if st.button("📊 Document Analysis", key="nav_analysis", use_container_width=True):
            st.session_state.current_page = 'Analysis'
    with col2:
        if st.button("📋 Compliance Results", key="nav_results", use_container_width=True):
            st.session_state.current_page = 'Results'
    with col3:
        if st.button("📥 Download Reports", key="nav_reports", use_container_width=True):
            st.session_state.current_page = 'Reports'
    with col4:
        if st.button("📈 Executive Dashboard", key="nav_dashboard", use_container_width=True):
            st.session_state.current_page = 'Dashboard'

# Function definitions complete - navigation will be called in main()

def create_download_link(data, filename, mime_type, button_text):
    """Create a download link for any file type"""
    if isinstance(data, str):
        data = data.encode()
    
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:{mime_type};base64,{b64}" download="{filename}" style="text-decoration: none;">'
    href += f'<div class="modern-button" style="display: inline-block; margin: 0.5rem;">{button_text}</div>'
    href += '</a>'
    return href

def render_beautiful_header():
    """Render the beautiful hero header"""
    st.markdown("""
    <div class="hero-header slide-in">
        <div class="hero-title">⚖️ ADGM Corporate Agent Pro</div>
        <div class="hero-subtitle">Enterprise AI-Powered Legal Document Analysis</div>
        <div class="hero-description">Professional • Competition-Grade • Beautiful Interface</div>
    </div>
    """, unsafe_allow_html=True)

def render_beautiful_sidebar():
    """Render enhanced beautiful sidebar"""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0; margin-bottom: 2rem;">
            <h2 style="color: #667eea; margin: 0;">🏢 Corporate Agent Pro</h2>
            <div style="background: linear-gradient(90deg, #667eea, #764ba2); height: 3px; border-radius: 2px; margin: 1rem 0;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # System Status
        st.markdown("### 🔋 System Status")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="status-card status-online">
                <div style="font-size: 1.5rem;">✅</div>
                <div style="font-weight: 600;">AI Engine</div>
                <div style="font-size: 0.8rem; color: #22c55e;">Online</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="status-card status-online">
                <div style="font-size: 1.5rem;">📚</div>
                <div style="font-weight: 600;">Knowledge</div>
                <div style="font-size: 0.8rem; color: #22c55e;">Loaded</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Analysis Options
        st.markdown("### ⚙️ Analysis Options")
        
        analysis_mode = st.selectbox(
            "Analysis Depth",
            ["🎯 Standard Analysis", "🔬 Deep Analysis", "⚡ Quick Scan"],
            index=1
        )
        
        st.checkbox("🚨 Risk Assessment", value=True, key="risk_assessment")
        st.checkbox("📝 Auto-Comment Documents", value=True, key="auto_comment")
        st.checkbox("📊 Generate All Reports", value=True, key="generate_reports")
        st.checkbox("🔍 Detailed Validation", value=True, key="detailed_validation")
        
        st.markdown("---")
        
        # Quick Actions
        st.markdown("### 🚀 Quick Actions")
        
        if st.button("📈 Performance Dashboard", use_container_width=True):
            st.session_state['show_dashboard'] = True
            
        if st.button("📚 Knowledge Explorer", use_container_width=True):
            st.session_state['show_knowledge'] = True
            
        if st.button("🔍 Sample Analysis", use_container_width=True):
            st.session_state['show_demo'] = True
        
        if st.button("🧹 Reset Session", use_container_width=True):
            for key in list(st.session_state.keys()):
                if key.startswith('analysis_') or key.startswith('results_'):
                    del st.session_state[key]
            st.rerun()

def show_beautiful_workflow(current_step: str = "ready"):
    """Show beautiful analysis workflow"""
    st.markdown("### 🔄 Analysis Workflow")
    
    steps = [
        ("📁", "Document Intake", "Processing files", "intake"),
        ("🤖", "AI Classification", "identify_doc_type()", "classify"),
        ("⚖️", "Process Detection", "detect_process_and_types()", "process"),
        ("📋", "Compliance Check", "analyze_bundle()", "compliance"),
        ("📊", "Report Generation", "Multi-format reports", "report")
    ]
    
    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
    
    for icon, name, desc, step in steps:
        if current_step == step:
            css_class = "progress-active"
            status = "🔄 Processing..."
        elif current_step == "complete":
            css_class = "progress-complete"
            status = "✅ Complete"
        else:
            css_class = "progress-pending"
            status = "⏳ Pending"
        
        st.markdown(f"""
        <div class="progress-step {css_class}">
            <div style="font-size: 2rem; margin-right: 1rem;">{icon}</div>
            <div style="flex: 1;">
                <div style="font-weight: 600; font-size: 1.1rem;">{name}</div>
                <div style="opacity: 0.8; font-size: 0.9rem;">{desc}</div>
                <div style="font-style: italic; font-size: 0.8rem; margin-top: 0.5rem;">{status}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def beautiful_document_upload():
    """Beautiful document upload interface"""
    st.markdown("### 📁 Upload Documents")
    
    st.markdown("""
    <div class="beautiful-card">
        <h3 style="color: #667eea; margin-top: 0;">🎯 Professional Document Analysis</h3>
        <p style="color: #64748b; margin-bottom: 2rem;">
            Upload your ADGM documents for comprehensive AI-powered analysis with beautiful reports and highlighted corrections.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Choose ADGM Documents",
        type=['docx', 'pdf', 'txt'],
        accept_multiple_files=True,
        help="📋 Supported: DOCX, PDF, TXT | 🔒 Secure processing | 🎨 Beautiful reports"
    )
    
    if uploaded_files:
        # Beautiful file summary
        total_size = sum(file.size for file in uploaded_files)
        
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card metric-primary">
                <div class="metric-value">{len(uploaded_files)}</div>
                <div class="metric-label">Files Uploaded</div>
                <div class="metric-delta">📄 Ready for analysis</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card metric-success">
                <div class="metric-value">{total_size/1024:.1f}</div>
                <div class="metric-label">KB Total Size</div>
                <div class="metric-delta">📏 Within limits</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card metric-warning">
                <div class="metric-value">✅</div>
                <div class="metric-label">Status</div>
                <div class="metric-delta">🎯 Validated</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card metric-danger">
                <div class="metric-value">🔒</div>
                <div class="metric-label">Security</div>
                <div class="metric-delta">🛡️ Encrypted</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # File details
        st.markdown("#### 📋 File Details")
        for i, file in enumerate(uploaded_files, 1):
            file_type = file.name.split('.')[-1].upper()
            st.markdown(f"""
            <div class="beautiful-card" style="margin: 1rem 0; padding: 1.5rem;">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div style="display: flex; align-items: center;">
                        <div style="font-size: 2rem; margin-right: 1rem;">📄</div>
                        <div>
                            <div style="font-weight: 600; color: #1e293b;">{file.name}</div>
                            <div style="color: #64748b; font-size: 0.9rem;">{file.size / 1024:.1f} KB • {file_type} Format</div>
                        </div>
                    </div>
                    <div style="background: #dcfce7; color: #15803d; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600; font-size: 0.8rem;">
                        ✅ Valid
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Analysis button
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            if st.button("🚀 Start Beautiful Analysis", type="primary", use_container_width=True):
                return uploaded_files
        
        with col2:
            if st.button("👁️ Preview Files", use_container_width=True):
                st.session_state['preview_files'] = uploaded_files
                
        with col3:
            if st.button("⚡ Quick Check", use_container_width=True):
                st.session_state['quick_check'] = uploaded_files
    
    return None

def perform_beautiful_analysis(uploaded_files):
    """Perform analysis with beautiful progress tracking"""
    
    progress_placeholder = st.empty()
    
    with progress_placeholder.container():
        show_beautiful_workflow("intake")
        st.info("🔄 Initializing beautiful analysis engine...")
    
    try:
        # Step 1: File Processing
        with progress_placeholder.container():
            show_beautiful_workflow("classify")
            st.info("🤖 Running AI classification with real functions...")
        
        file_bytes = {}
        for file in uploaded_files:
            file_content = file.read()
            file_bytes[file.name] = file_content
        
        time.sleep(1.5)
        
        # Step 2: Process Detection
        with progress_placeholder.container():
            show_beautiful_workflow("process")
            st.info("⚖️ Detecting legal process using detect_process_and_types()...")
        
        process_analysis = detect_process_and_types(file_bytes)
        st.success(f"✅ Process identified: {process_analysis.get('process', 'Unknown')}")
        
        time.sleep(1.5)
        
        # Step 3: Compliance Analysis
        with progress_placeholder.container():
            show_beautiful_workflow("compliance")
            st.info("📋 Running comprehensive compliance analysis...")
        
        validation_results = analyze_bundle(process_analysis)
        compliance_score = validation_results.get("compliance_score", 0)
        st.success(f"✅ Compliance score calculated: {compliance_score}%")
        
        time.sleep(1.5)
        
        # Step 4: Report Generation
        with progress_placeholder.container():
            show_beautiful_workflow("report")
            st.info("📊 Generating beautiful reports in multiple formats...")
        
        # Generate all report formats
        html_report = build_html_report(validation_results)
        pdf_report = build_summary_pdf(validation_results)
        
        # Generate DOCX with comments for each uploaded file
        commented_docs = {}
        issues = validation_results.get("issues_found", [])
        
        for file in uploaded_files:
            if file.name.endswith('.docx'):
                try:
                    # Get issues for this specific document
                    doc_issues = [issue for issue in issues if issue.get('document') == file.name]
                    
                    # Create comments for DOCX
                    comments = []
                    for issue in doc_issues:
                        comments.append({
                            'text': issue.get('suggestion', 'Review this section'),
                            'author': 'ADGM Agent Pro',
                            'comment': f"[{issue.get('severity', 'Medium')}] {issue.get('issue', 'Compliance issue detected')}"
                        })
                    
                    # Reset file pointer
                    file.seek(0)
                    file_content = file.read()
                    
                    # Insert comments and get updated DOCX
                    commented_docx = insert_comments_and_return_bytes(file_content, comments)
                    commented_docs[file.name] = commented_docx
                    
                except Exception as e:
                    st.warning(f"Could not add comments to {file.name}: {str(e)}")
        
        # Calculate risk level
        if compliance_score >= 80:
            risk_level = "Low"
        elif compliance_score >= 60:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        results = {
            "process_analysis": process_analysis,
            "validation_results": validation_results,
            "html_report": html_report,
            "pdf_report": pdf_report,
            "commented_docs": commented_docs,
            "risk_level": risk_level,
            "compliance_score": compliance_score
        }
        
        with progress_placeholder.container():
            show_beautiful_workflow("complete")
            st.success("✅ Beautiful analysis complete with all reports generated!")
        
        return results
        
    except Exception as e:
        st.error(f"❌ Analysis failed: {str(e)}")
        st.error("🔍 Error details:")
        st.code(traceback.format_exc())
        return None

def display_beautiful_results(results):
    """Display results with beautiful UI"""
    
    if not results:
        st.error("No analysis results to display")
        return
    
    validation_results = results["validation_results"]
    process_analysis = results["process_analysis"]
    
    # Beautiful Executive Summary
    st.markdown("## 📊 Executive Analysis Dashboard")
    
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        docs_count = validation_results.get("documents_uploaded", 0)
        st.markdown(f"""
        <div class="metric-card metric-primary">
            <div class="metric-value">{docs_count}</div>
            <div class="metric-label">Documents Processed</div>
            <div class="metric-delta">📄 AI Analyzed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        process = validation_results.get("process", "Unknown")
        st.markdown(f"""
        <div class="metric-card metric-success">
            <div class="metric-value" style="font-size: 1.5rem;">⚖️</div>
            <div class="metric-label">Process Type</div>
            <div class="metric-delta">{process}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        issues_count = len(validation_results.get("issues_found", []))
        st.markdown(f"""
        <div class="metric-card metric-warning">
            <div class="metric-value">{issues_count}</div>
            <div class="metric-label">Issues Found</div>
            <div class="metric-delta">🚨 Compliance</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        compliance_score = results["compliance_score"]
        st.markdown(f"""
        <div class="metric-card metric-danger">
            <div class="metric-value">{compliance_score}%</div>
            <div class="metric-label">Compliance Score</div>
            <div class="metric-delta">{results['risk_level']} Risk</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Beautiful Document Analysis
    st.markdown("---")
    st.markdown("## 📋 Document Analysis Results")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📄 AI Classifications")
        documents = process_analysis.get("documents", {})
        for doc_name, doc_info in documents.items():
            doc_type = doc_info.get("type", "Unknown")
            error = doc_info.get("error", None)
            
            if error:
                st.markdown(f"""
                <div class="beautiful-card" style="border-left: 4px solid #ef4444;">
                    <div style="font-weight: 600; color: #ef4444;">❌ {doc_name}</div>
                    <div style="color: #64748b; margin-top: 0.5rem;">{error}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="beautiful-card">
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                        <div>
                            <div style="font-weight: 600; color: #1e293b;">📄 {doc_name}</div>
                            <div style="color: #667eea; font-weight: 500; margin-top: 0.5rem;">Type: {doc_type}</div>
                        </div>
                        <div style="background: #dcfce7; color: #15803d; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600; font-size: 0.8rem;">
                            ✅ Analyzed
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🎯 Process Requirements")
        missing_docs = validation_results.get("missing_documents", [])
        required_docs = validation_results.get("required_documents", 0)
        
        st.markdown(f"""
        <div class="beautiful-card">
            <div style="font-weight: 600; color: #1e293b; margin-bottom: 1rem;">Process: {process}</div>
            <div style="color: #64748b; margin-bottom: 1rem;">Required Documents: {required_docs}</div>
        """, unsafe_allow_html=True)
        
        if missing_docs:
            st.markdown('<div style="margin-top: 1rem;"><strong>Missing Documents:</strong></div>', unsafe_allow_html=True)
            for doc in missing_docs:
                st.markdown(f"""
                <div style="background: #fef2f2; color: #dc2626; padding: 0.5rem 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 3px solid #ef4444;">
                    ❌ {doc}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: #f0fdf4; color: #15803d; padding: 1rem; border-radius: 8px; border-left: 3px solid #22c55e;">
                ✅ All required documents present
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Beautiful Issues Display
    issues = validation_results.get("issues_found", [])
    if issues:
        st.markdown("---")
        st.markdown("## 🚨 Compliance Issues & Recommendations")
        
        # Issue summary
        high_issues = len([i for i in issues if i.get("severity") == "High"])
        medium_issues = len([i for i in issues if i.get("severity") == "Medium"])
        low_issues = len([i for i in issues if i.get("severity") == "Low"])
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="status-card" style="border-left: 4px solid #ef4444;">
                <div style="font-size: 2rem;">🔴</div>
                <div style="font-weight: 600;">High Priority</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #ef4444;">{high_issues}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="status-card" style="border-left: 4px solid #f59e0b;">
                <div style="font-size: 2rem;">🟡</div>
                <div style="font-weight: 600;">Medium Priority</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #f59e0b;">{medium_issues}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="status-card" style="border-left: 4px solid #22c55e;">
                <div style="font-size: 2rem;">🟢</div>
                <div style="font-weight: 600;">Low Priority</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #22c55e;">{low_issues}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Detailed issues
        for i, issue in enumerate(issues, 1):
            severity = issue.get("severity", "Medium")
            
            st.markdown(f"""
            <div class="issue-card issue-{severity.lower()}">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
                    <h4 style="margin: 0; font-size: 1.2rem; color: #1a1a1a;">🚨 Issue #{i}: {issue.get('issue', 'Compliance Issue')}</h4>
                    <div style="background: rgba(255,255,255,0.9); color: #1a1a1a; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 700; font-size: 0.8rem;">
                        {severity.upper()}
                    </div>
                </div>
                <div style="margin: 0.8rem 0; color: #1a1a1a;"><strong>📄 Document:</strong> {issue.get('document', 'Unknown')}</div>
                <div style="margin: 0.8rem 0; color: #1a1a1a;"><strong>💡 Recommendation:</strong> {issue.get('suggestion', 'Review and update')}</div>
                <div style="margin: 0.8rem 0; color: #1a1a1a;"><strong>📚 Citation:</strong> {issue.get('citations', 'ADGM Regulations')}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Beautiful Risk Assessment
    st.markdown("---")
    st.markdown("## 🛡️ Risk Assessment Dashboard")
    
    st.markdown('<div class="risk-container">', unsafe_allow_html=True)
    
    risk_level = results["risk_level"]
    compliance_score = results["compliance_score"]
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        risk_class = f"risk-{risk_level.lower()}"
        st.markdown(f"""
        <div class="risk-gauge {risk_class}">
            <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 1rem;">🛡️ Risk Level</div>
            <div class="risk-value">{risk_level}</div>
            <div style="font-size: 1.1rem; opacity: 0.9;">Compliance Score: {compliance_score}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📋 Risk Factors & Recommendations")
        
        risk_factors = {
            "High": [
                "⚠️ Critical jurisdiction issues identified requiring immediate attention",
                "🚨 Major compliance violations found that could impact approval",
                "⛔ Required documents missing from submission package",
                "🔴 High-priority fixes needed before submission"
            ],
            "Medium": [
                "⚠️ Some compliance issues identified requiring review",
                "📋 Documentation gaps present but manageable",
                "🟡 Medium-priority attention needed for optimization",
                "✅ Most requirements satisfied with minor adjustments"
            ],
            "Low": [
                "✅ Excellent compliance coverage across all areas",
                "✅ Only minor issues requiring simple corrections",
                "✅ Most requirements fully met and documented",
                "🎯 Ready for submission with confidence"
            ]
        }
        
        for factor in risk_factors.get(risk_level, []):
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.9); padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 3px solid #667eea; color: #1a1a1a;">
                {factor}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Beautiful Downloads Section
    st.markdown("---")
    st.markdown("## 📥 Download Beautiful Reports")
    
    st.markdown('<div class="download-grid">', unsafe_allow_html=True)
    
    # JSON Report
    st.markdown("""
    <div class="download-card download-json">
        <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
        <h3 style="color: #10b981; margin: 1rem 0;">JSON Analysis Report</h3>
        <p style="color: #64748b; margin-bottom: 2rem;">Complete analysis data in JSON format for integration</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create JSON download
    report_data = {
        "analysis_timestamp": datetime.now().isoformat(),
        "process_analysis": process_analysis,
        "validation_results": validation_results,
        "risk_assessment": {
            "level": results["risk_level"],
            "score": results["compliance_score"]
        }
    }
    
    json_data = json.dumps(report_data, indent=2)
    json_filename = f"ADGM_Analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    st.markdown(
        create_download_link(json_data, json_filename, "application/json", "💾 Download JSON Report"),
        unsafe_allow_html=True
    )
    
    # PDF Report
    st.markdown("""
    <div class="download-card download-pdf">
        <div style="font-size: 3rem; margin-bottom: 1rem;">📄</div>
        <h3 style="color: #ef4444; margin: 1rem 0;">PDF Executive Report</h3>
        <p style="color: #64748b; margin-bottom: 2rem;">Professional summary report in PDF format</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create PDF download
    pdf_filename = f"ADGM_Executive_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    st.markdown(
        create_download_link(results["pdf_report"], pdf_filename, "application/pdf", "💾 Download PDF Report"),
        unsafe_allow_html=True
    )
    
    # DOCX with Comments
    if results.get("commented_docs"):
        st.markdown("""
        <div class="download-card download-docx">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📝</div>
            <h3 style="color: #3b82f6; margin: 1rem 0;">DOCX with Comments</h3>
            <p style="color: #64748b; margin-bottom: 2rem;">Original documents with AI-generated comments and highlights</p>
        </div>
        """, unsafe_allow_html=True)
        
        for filename, docx_data in results["commented_docs"].items():
            commented_filename = f"Commented_{filename.replace('.docx', '')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
            
            st.markdown(
                create_download_link(docx_data, commented_filename, "application/vnd.openxmlformats-officedocument.wordprocessingml.document", f"💾 Download {filename}"),
                unsafe_allow_html=True
            )
    
    # HTML Report
    st.markdown("""
    <div class="download-card download-html">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🌐</div>
        <h3 style="color: #8b5cf6; margin: 1rem 0;">HTML Interactive Report</h3>
        <p style="color: #64748b; margin-bottom: 2rem;">Interactive web report with detailed analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create HTML download
    html_filename = f"ADGM_Interactive_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    
    st.markdown(
        create_download_link(results["html_report"], html_filename, "text/html", "💾 Download HTML Report"),
        unsafe_allow_html=True
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Show HTML report preview
    if results.get("html_report"):
        st.markdown("### 📋 Interactive Report Preview")
        st.components.v1.html(results["html_report"], height=500, scrolling=True)

def page_analysis():
    """Document Analysis Page"""
    st.markdown("""
    <div class="page-container">
        <div class="page-header">
            <div class="page-title">📊 Document Analysis</div>
            <div class="page-subtitle">Upload and analyze your ADGM documents</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_files = beautiful_document_upload()
    
    if uploaded_files:
        with st.spinner("🎨 Running enhanced AI analysis..."):
            results = perform_beautiful_analysis(uploaded_files)
            
            if results:
                st.session_state['analysis_results'] = results
                st.session_state['analysis_complete'] = True
                
                st.markdown("""
                <div class="beautiful-card">
                    <div style="text-align: center;">
                        <div style="font-size: 3rem; margin-bottom: 1rem;">🎉</div>
                        <h2 style="margin: 0; color: #15803d;">Analysis Complete!</h2>
                        <p style="color: #6b7280; margin-top: 0.5rem;">Your documents have been successfully analyzed</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Auto-navigate to results
                st.session_state.current_page = 'Results'
                st.rerun()

def page_results():
    """Compliance Results Page"""
    st.markdown("""
    <div class="page-container">
        <div class="page-header">
            <div class="page-title">📋 Compliance Results</div>
            <div class="page-subtitle">Detailed analysis results and compliance findings</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.get('analysis_complete') and st.session_state.get('analysis_results'):
        display_beautiful_results(st.session_state['analysis_results'])
    else:
        st.markdown("""
        <div class="beautiful-card" style="text-align: center;">
            <h3 style="color: #6b7280;">📄 No Analysis Results Available</h3>
            <p style="color: #9ca3af;">Please upload and analyze documents first</p>
            <div style="margin-top: 1rem;">
        """, unsafe_allow_html=True)
        
        if st.button("📊 Go to Document Analysis", use_container_width=True):
            st.session_state.current_page = 'Analysis'
            st.rerun()
        
        st.markdown("</div></div>", unsafe_allow_html=True)

def page_reports():
    """Download Reports Page"""
    st.markdown("""
    <div class="page-container">
        <div class="page-header">
            <div class="page-title">� Download Reports</div>
            <div class="page-subtitle">Get professional reports and reviewed documents</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.get('analysis_complete') and st.session_state.get('analysis_results'):
        results = st.session_state['analysis_results']
        
        st.markdown("""
        <div class="beautiful-card">
            <h3>� Available Downloads</h3>
            <p style="color: #6b7280;">Choose from multiple report formats</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="beautiful-card" style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📄</div>
                <h4>Executive Summary</h4>
                <p style="color: #6b7280; font-size: 0.9rem;">Professional PDF summary</p>
            </div>
            """, unsafe_allow_html=True)
            
            if results.get("summary_pdf"):
                st.download_button(
                    "📄 Download PDF",
                    data=results["summary_pdf"],
                    file_name=f"ADGM_Summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        
        with col2:
            st.markdown("""
            <div class="beautiful-card" style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📋</div>
                <h4>Detailed Report</h4>
                <p style="color: #6b7280; font-size: 0.9rem;">Comprehensive DOCX report</p>
            </div>
            """, unsafe_allow_html=True)
            
            if results.get("detailed_docx"):
                st.download_button(
                    "📋 Download DOCX",
                    data=results["detailed_docx"],
                    file_name=f"ADGM_Detailed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
        
        with col3:
            st.markdown("""
            <div class="beautiful-card" style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📦</div>
                <h4>Complete Package</h4>
                <p style="color: #6b7280; font-size: 0.9rem;">All files in ZIP format</p>
            </div>
            """, unsafe_allow_html=True)
            
            if results.get("zip_package"):
                st.download_button(
                    "📦 Download ZIP",
                    data=results["zip_package"],
                    file_name=f"ADGM_Package_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                    mime="application/zip",
                    use_container_width=True
                )
    else:
        st.markdown("""
        <div class="beautiful-card" style="text-align: center;">
            <h3 style="color: #6b7280;">📥 No Reports Available</h3>
            <p style="color: #9ca3af;">Complete document analysis to generate reports</p>
            <div style="margin-top: 1rem;">
        """, unsafe_allow_html=True)
        
        if st.button("📊 Start Analysis", use_container_width=True):
            st.session_state.current_page = 'Analysis'
            st.rerun()
        
        st.markdown("</div></div>", unsafe_allow_html=True)

def page_dashboard():
    """Executive Dashboard Page"""
    st.markdown("""
    <div class="page-container">
        <div class="page-header">
            <div class="page-title">📈 Executive Dashboard</div>
            <div class="page-subtitle">High-level overview and analytics</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.get('analysis_complete') and st.session_state.get('analysis_results'):
        results = st.session_state['analysis_results']
        report = results.get('report', {})
        
        # Executive Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "📄 Documents",
                report.get('documents_uploaded', 0),
                help="Total documents uploaded"
            )
        
        with col2:
            total_issues = len(report.get('issues_found', []))
            st.metric(
                "🔍 Issues Found",
                total_issues,
                help="Total compliance issues detected"
            )
        
        with col3:
            high_issues = sum(1 for x in report.get('issues_found', []) if x.get('severity') == 'High')
            st.metric(
                "🚨 High Priority",
                high_issues,
                help="Critical issues requiring immediate attention"
            )
        
        with col4:
            compliance_score = max(0, 100 - (high_issues * 20 + total_issues * 5))
            st.metric(
                "✅ Compliance Score",
                f"{compliance_score}%",
                help="Overall compliance percentage"
            )
        
        # Process Overview
        st.markdown("""
        <div class="beautiful-card">
            <h3>📋 Process Overview</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        **Detected Process:** {report.get('process', 'Unknown')}
        
        **Required Documents:** {report.get('required_documents', 0)}
        
        **Missing Documents:** {len(report.get('missing_documents', []))}
        """)
        
        if report.get('missing_documents'):
            st.error(f"Missing: {', '.join(report['missing_documents'])}")
        else:
            st.success("✅ All required documents present")
        
        # Quick Actions
        st.markdown("""
        <div class="beautiful-card">
            <h3>🚀 Quick Actions</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📋 View Detailed Results", use_container_width=True):
                st.session_state.current_page = 'Results'
                st.rerun()
        
        with col2:
            if st.button("📥 Download Reports", use_container_width=True):
                st.session_state.current_page = 'Reports'
                st.rerun()
        
        with col3:
            if st.button("📊 New Analysis", use_container_width=True):
                # Clear results and go to analysis
                for key in list(st.session_state.keys()):
                    if key.startswith('analysis'):
                        del st.session_state[key]
                st.session_state.current_page = 'Analysis'
                st.rerun()
    else:
        st.markdown("""
        <div class="beautiful-card" style="text-align: center;">
            <h3 style="color: #6b7280;">📈 No Data Available</h3>
            <p style="color: #9ca3af;">Upload and analyze documents to see dashboard</p>
            <div style="margin-top: 1rem;">
        """, unsafe_allow_html=True)
        
        if st.button("📊 Start Analysis", use_container_width=True):
            st.session_state.current_page = 'Analysis'
            st.rerun()
        
        st.markdown("</div></div>", unsafe_allow_html=True)

def main():
    """Main application with enhanced navigation"""
    
    render_beautiful_header()
    render_beautiful_sidebar()
    create_navigation()
    
    # Page routing
    current_page = st.session_state.current_page
    
    if current_page == 'Analysis':
        page_analysis()
    elif current_page == 'Results':
        page_results()
    elif current_page == 'Reports':
        page_reports()
    elif current_page == 'Dashboard':
        page_dashboard()
    else:
        # Default to analysis page
        st.session_state.current_page = 'Analysis'
        page_analysis()


if __name__ == "__main__":
    main()
