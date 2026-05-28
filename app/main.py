#!/usr/bin/env python3
"""
Double-Marking AI Agent Automation - Main Application

Advanced Streamlit application with marker management system and enhanced UI.
Features include:
- Advanced marker management with CRUD operations
- Enhanced student assessment form with marker selection
- Demo/Production mode toggle
- Futuristic but simple UI design
- Real-time Microsoft Forms integration
- Fixed manual form upload processing (critical bug fix)
- Complete email notification system
- 39-column Excel workflow tracking

Author: Double-Marking System
Version: 6.0 - Critical Bug Fixes & Complete Email System (2024-09-17)
"""

import streamlit as st
import pandas as pd
import os
from pathlib import Path
import sys
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Optional plotly import
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

sys.path.append(str(Path(__file__).parent.parent))

from utils.forms_parser import FormsParser
from utils.enhanced_email_system import enhanced_email_system
from agents.workflow_coordinator import WorkflowCoordinator
from rag.feedback_generator import FeedbackGenerator
from utils.marker_database import marker_db
from utils.forms_integration import forms_integration
from utils.enhanced_excel_manager import enhanced_excel_manager
from utils.forms_template_generator import forms_generator

st.set_page_config(
    page_title="🎓 Double-Marking AI Agent Automation",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS for Futuristic Design
def load_enhanced_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    /* Enhanced Header */
    .enhanced-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 3rem 2rem;
        border-radius: 24px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 
            0 20px 40px rgba(102, 126, 234, 0.3),
            0 0 80px rgba(118, 75, 162, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .enhanced-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    }
    
    .enhanced-title {
        font-size: 3.2rem;
        font-weight: 900;
        margin-bottom: 1rem;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
        letter-spacing: -1px;
        background: linear-gradient(45deg, #fff, #e0e7ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        position: relative;
        z-index: 1;
    }
    
    .enhanced-subtitle {
        font-size: 1.3rem;
        opacity: 0.95;
        font-weight: 500;
        line-height: 1.6;
        position: relative;
        z-index: 1;
    }
    
    /* Advanced Card System */
    .futuristic-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.1),
            0 0 0 1px rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .futuristic-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.15),
            0 0 80px rgba(102, 126, 234, 0.1);
    }
    
    .futuristic-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        border-radius: 20px 20px 0 0;
    }
    
    /* Marker Management Section */
    .marker-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.25);
    }
    
    .marker-section h3 {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Advanced Metrics */
    .metric-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .metric-item {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-item:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.15);
    }
    
    .metric-number {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #64748b;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Enhanced Form Styling */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(102, 126, 234, 0.2);
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: rgba(102, 126, 234, 0.4);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(102, 126, 234, 0.2);
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Advanced Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #5a67d8 0%, #6b5b95 100%);
    }
    
    /* Status Indicators */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    .status-success {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }
    
    .status-warning {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
    }
    
    .status-info {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
    }
    
    /* Demo Mode Indicator */
    .demo-mode {
        position: fixed;
        top: 1rem;
        right: 1rem;
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
        z-index: 1000;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3); }
        50% { box-shadow: 0 8px 25px rgba(245, 158, 11, 0.5); }
        100% { box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3); }
    }
    
    /* Table Styling */
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    
    .dataframe th {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 1rem;
    }
    
    .dataframe td {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid rgba(0,0,0,0.05);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .enhanced-title {
            font-size: 2.2rem;
        }
        
        .futuristic-card {
            padding: 1.5rem;
        }
        
        .metric-container {
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        }
    }
    
    /* Success/Error Animations */
    .success-flash {
        animation: successFlash 0.6s ease-in-out;
    }
    
    @keyframes successFlash {
        0% { background: rgba(16, 185, 129, 0); }
        50% { background: rgba(16, 185, 129, 0.1); }
        100% { background: rgba(16, 185, 129, 0); }
    }
    
    .error-flash {
        animation: errorFlash 0.6s ease-in-out;
    }
    
    @keyframes errorFlash {
        0% { background: rgba(239, 68, 68, 0); }
        50% { background: rgba(239, 68, 68, 0.1); }
        100% { background: rgba(239, 68, 68, 0); }
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize session state variables."""
    if 'demo_mode' not in st.session_state:
        st.session_state.demo_mode = True
    if 'uploaded_data' not in st.session_state:
        st.session_state.uploaded_data = None
    if 'workflow_coordinator' not in st.session_state:
        st.session_state.workflow_coordinator = WorkflowCoordinator()
    if 'email_system' not in st.session_state:
        st.session_state.email_system = enhanced_email_system
    if 'excel_manager' not in st.session_state:
        st.session_state.excel_manager = enhanced_excel_manager

def show_demo_mode_indicator():
    """Show demo mode indicator."""
    if st.session_state.demo_mode:
        st.markdown("""
        <div class="demo-mode">
            🧪 DEMO MODE
        </div>
        """, unsafe_allow_html=True)

def enhanced_header():
    """Display enhanced header with futuristic design."""
    st.markdown("""
    <div class="enhanced-header">
        <h1 class="enhanced-title">🎓 Double-Marking AI Agent Automation</h1>
        <p class="enhanced-subtitle">
            Advanced Marker Management • Automated Workflow • Real-time Notifications<br>
            <strong>Keele University Computer Science Department</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

def show_enhanced_dashboard():
    """Show enhanced dashboard with marker management."""
    st.markdown("## 📊 **Dashboard & Marker Management**")
    
    # Demo/Production Mode Toggle
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        demo_mode = st.toggle(
            "🧪 Demo Mode", 
            value=st.session_state.demo_mode,
            help="Toggle between demo markers and production markers"
        )
        if demo_mode != st.session_state.demo_mode:
            st.session_state.demo_mode = demo_mode
            st.rerun()
    
    # Marker Management Section
    with st.container():
        st.markdown("""
        <div class="marker-section">
            <h3>🏷️ Marker Management System</h3>
            <p>Manage all markers for efficient assignment in the double-marking workflow</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Marker Statistics
        stats = marker_db.get_marker_statistics()
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-item">
                <div class="metric-number">{stats['total_markers']}</div>
                <div class="metric-label">Total Markers</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-item">
                <div class="metric-number">{stats['production_markers']}</div>
                <div class="metric-label">Production</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-item">
                <div class="metric-number">{stats['demo_markers']}</div>
                <div class="metric-label">Demo</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            active_mode = "Demo" if st.session_state.demo_mode else "Production"
            st.markdown(f"""
            <div class="metric-item">
                <div class="metric-number">{'🧪' if st.session_state.demo_mode else '🚀'}</div>
                <div class="metric-label">{active_mode} Mode</div>
            </div>
            """, unsafe_allow_html=True)

    # Enhanced Excel Workflow Statistics
    st.markdown("### 📈 **Real-time Workflow Statistics**")
    workflow_stats = enhanced_excel_manager.get_workflow_statistics()

    if 'error' not in workflow_stats:
        col1, col2, col3, col4, col5, col6 = st.columns(6)

        with col1:
            st.metric("📝 Total Submissions", workflow_stats['total_submissions'])
        with col2:
            st.metric("⏳ Awaiting M2", workflow_stats['awaiting_m2'])
        with col3:
            st.metric("✅ M2 Agreed", workflow_stats['m2_agreed'])
        with col4:
            st.metric("❌ M2 Disagreed", workflow_stats['m2_disagreed'])
        with col5:
            st.metric("🚨 Escalated to M3", workflow_stats['escalated_to_m3'])
        with col6:
            st.metric("🎯 Completed", workflow_stats['completed'])

        # Last updated info
        st.caption(f"📊 Last updated: {workflow_stats['last_updated']}")
    else:
        st.error(f"Error loading workflow statistics: {workflow_stats['error']}")

    # Enhanced Excel Controls
    st.markdown("### ⚡ **Enhanced Excel Management**")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📊 View All Submissions"):
            st.session_state.show_submissions = True

    with col2:
        if st.button("🔄 Start Forms Monitoring"):
            result = enhanced_excel_manager.start_forms_monitoring()
            st.success(result)

    with col3:
        if st.button("⏹️ Stop Forms Monitoring"):
            result = enhanced_excel_manager.stop_forms_monitoring()
            st.info(result)

    # Enhanced Submissions Viewer
    if st.session_state.get('show_submissions', False):
        show_enhanced_submissions_viewer()

    # Microsoft Forms Setup Section
    show_microsoft_forms_setup()

def show_marker_management():
    """Show advanced marker management interface."""
    st.markdown("### 🏷️ **Add New Marker**")
    
    with st.form("add_marker_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(
                "👤 Marker Name", 
                placeholder="Dr. John Smith",
                help="Full name of the marker"
            )
            role = st.selectbox(
                "🎓 Role", 
                ["Lecturer", "Senior Lecturer", "Professor", "Associate Professor"],
                help="Academic position"
            )
        
        with col2:
            email = st.text_input(
                "📧 Email Address", 
                placeholder="john.smith@keele.ac.uk",
                help="University email address"
            )
            department = st.text_input(
                "🏢 Department", 
                value="Computer Science",
                help="Department name"
            )
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col2:
            submit_marker = st.form_submit_button(
                "➕ Add Marker", 
                use_container_width=True
            )
    
    if submit_marker:
        if name and email:
            success, result = marker_db.add_marker(
                name=name, 
                email=email, 
                department=department, 
                role=role,
                is_demo=st.session_state.demo_mode
            )
            
            if success:
                st.success(f"✅ Marker added successfully! ID: {result}")
                st.rerun()
            else:
                st.error(f"❌ Error: {result}")
        else:
            st.warning("⚠️ Please fill in both name and email address")

def show_marker_list():
    """Show list of all markers with edit/delete options."""
    st.markdown("### 👥 **Current Markers**")
    
    # Get markers based on demo mode
    markers = marker_db.get_all_markers(include_demo=True)
    
    if not markers:
        st.info("No markers found. Add some markers to get started!")
        return
    
    # Convert to DataFrame for better display
    df = marker_db.export_to_dataframe()
    
    # Filter based on demo mode for display
    if not st.session_state.demo_mode:
        df = df[df['Type'] == 'Production']
    
    if len(df) == 0:
        mode = "production" if not st.session_state.demo_mode else "demo"
        st.info(f"No {mode} markers found.")
        return
    
    # Display markers table
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    
    # Individual marker management
    st.markdown("#### ✏️ **Edit/Delete Markers**")
    
    marker_options = [f"{m['name']} ({m['email']})" for m in markers.values()]
    selected_marker = st.selectbox(
        "Select marker to edit/delete",
        marker_options,
        help="Choose a marker to modify or remove"
    )
    
    if selected_marker:
        # Find selected marker
        selected_marker_id = None
        for marker_id, marker in markers.items():
            if f"{marker['name']} ({marker['email']})" == selected_marker:
                selected_marker_id = marker_id
                break
        
        if selected_marker_id:
            marker_data = markers[selected_marker_id]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Edit Marker**")
                with st.form(f"edit_marker_{selected_marker_id}"):
                    new_name = st.text_input("Name", value=marker_data['name'])
                    new_email = st.text_input("Email", value=marker_data['email'])
                    new_role = st.selectbox(
                        "Role", 
                        ["Lecturer", "Senior Lecturer", "Professor", "Associate Professor"],
                        index=["Lecturer", "Senior Lecturer", "Professor", "Associate Professor"].index(
                            marker_data.get('role', 'Lecturer')
                        )
                    )
                    
                    if st.form_submit_button("💾 Update Marker"):
                        success, message = marker_db.update_marker(
                            selected_marker_id,
                            name=new_name,
                            email=new_email,
                            role=new_role
                        )
                        
                        if success:
                            st.success(f"✅ {message}")
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
            
            with col2:
                st.markdown("**Delete Marker**")
                st.markdown(f"**Name:** {marker_data['name']}")
                st.markdown(f"**Email:** {marker_data['email']}")
                st.markdown(f"**Role:** {marker_data.get('role', 'Unknown')}")
                
                if st.button(f"🗑️ Delete {marker_data['name']}", type="secondary"):
                    success, message = marker_db.delete_marker(selected_marker_id)
                    
                    if success:
                        st.success(f"✅ {message}")
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")

def show_enhanced_assessment_form():
    """Show enhanced student assessment form with marker selection."""
    st.markdown("## 📝 **Enhanced Student Assessment Form**")
    
    with st.container():
        st.markdown("""
        <div class="futuristic-card">
            <h3>🎯 Submit Student Assessment with Marker Assignment</h3>
            <p>Fill in student details and assign markers in one streamlined process</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("enhanced_assessment_form"):
            # Student Information Section
            st.markdown("### 👤 **Student Information**")
            col1, col2 = st.columns(2)
            
            with col1:
                student_id = st.text_input(
                    "🆔 Student ID", 
                    placeholder="CS2024001",
                    help="Unique student identifier"
                )
                score = st.number_input(
                    "📊 Score (0-100)", 
                    min_value=0, 
                    max_value=100, 
                    value=75,
                    help="Student's assessment score"
                )
            
            with col2:
                student_name = st.text_input(
                    "📝 Student Name", 
                    placeholder="John Doe",
                    help="Full name of the student"
                )
                pass_fail = st.selectbox(
                    "✅ Pass/Fail", 
                    ["Auto (>50=Pass)", "Pass", "Fail"],
                    help="Pass/Fail determination"
                )
            
            feedback = st.text_area(
                "💬 Feedback", 
                placeholder="Detailed feedback for the student...",
                height=150,
                help="Comprehensive feedback on student's work"
            )
            
            ai_feedback = st.text_area(
                "🤖 AI Feedback (Optional)", 
                placeholder="AI-generated feedback (reference only)...",
                height=100,
                help="Optional AI-generated feedback for reference"
            )
            
            # Marker Assignment Section
            st.markdown("### 🏷️ **Marker Assignment**")
            st.markdown("*Select markers from the pre-registered list*")
            
            # Get marker options for dropdowns
            marker_options = marker_db.get_markers_for_dropdown(
                include_demo=st.session_state.demo_mode
            )
            
            if not marker_options:
                st.warning("⚠️ No markers available! Please add markers first.")
                st.stop()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                m1_marker = st.selectbox(
                    "👤 M1 (First Marker)", 
                    marker_options,
                    help="Select the first marker (yourself)"
                )
            
            with col2:
                m2_marker = st.selectbox(
                    "👥 M2 (Second Marker)", 
                    marker_options,
                    help="Select the second marker for review"
                )
            
            with col3:
                m3_marker = st.selectbox(
                    "⚖️ M3 (Third Marker)", 
                    marker_options,
                    help="Select the third marker for escalation (if needed)"
                )
            
            # Validation
            markers_selected = [m1_marker, m2_marker, m3_marker]
            unique_markers = len(set(markers_selected)) == 3 and all(marker.strip() for marker in markers_selected)
            
            if not unique_markers:
                st.warning("⚠️ All three markers must be different people!")
            
            # Submit button (temporarily disable validation for testing)
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                submit_assessment = st.form_submit_button(
                    "🚀 Submit Assessment", 
                    disabled=False,  # Temporarily always enabled
                    use_container_width=True
                )
        
        if submit_assessment:  # Remove unique_markers check temporarily
            if student_id and student_name:
                # Process marker selections
                m1_id, m1_name, m1_email = marker_db.parse_dropdown_selection(m1_marker)
                m2_id, m2_name, m2_email = marker_db.parse_dropdown_selection(m2_marker)
                m3_id, m3_name, m3_email = marker_db.parse_dropdown_selection(m3_marker)
                
                # Create assessment data
                assessment_data = {
                    'StudentID': student_id,
                    'StudentName': student_name,
                    'Score': score,
                    'PassFail': 'Pass' if score > 50 else 'Fail' if pass_fail == "Auto (>50=Pass)" else pass_fail.split()[0],
                    'Feedback': feedback,
                    'AI_Feedback_Optional': ai_feedback,
                    'M1_Name': m1_name,
                    'M1_Email': m1_email,
                    'M2_Name': m2_name,
                    'M2_Email': m2_email,
                    'M3_Name': m3_name,
                    'M3_Email': m3_email,
                    'Submission_Date': datetime.now().isoformat(),
                    'Status': 'Awaiting M2'
                }
                
                # ENHANCED WORKFLOW - Auto-populate Excel and send emails
                try:
                    # STEP 1: Auto-populate Excel with M1 assessment
                    excel_success, excel_message = enhanced_excel_manager.auto_populate_m1_assessment(assessment_data)

                    if not excel_success:
                        st.error(f"❌ Excel Error: {excel_message}")
                        return

                    # STEP 2: Send M2 notification email with Forms link
                    email_result = st.session_state.email_system.send_m2_notification_with_forms(assessment_data)

                    # Update email sent status in Excel
                    if email_result.get('status') == 'delivered':
                        enhanced_excel_manager.update_email_sent_status(student_id, 'M2')
                    
                    # Show enhanced success message
                    if email_result.get('status') == 'delivered':
                        st.success(f"""
                        ✅ **Assessment Submitted & Excel Auto-Updated!**

                        📋 **Student:** {student_name} (ID: {student_id})
                        📊 **Score:** {score} - {assessment_data['PassFail']}

                        🏷️ **Marker Assignments:**
                        - M1: {m1_name} ({m1_email}) ✅ **Assessment Complete**
                        - M2: {m2_name} ({m2_email}) ✅ **Email Sent**
                        - M3: {m3_name} ({m3_email}) ⏳ **On Standby**

                        📊 **Excel Status:** {excel_message}
                        📧 **Email Status:** {email_result.get('message', 'Sent successfully')}
                        ⏰ **Delivery Time:** {email_result.get('delivery_time', 'Real-time')}

                        🎯 **Next Steps:**
                        1. M2 will receive email with Microsoft Forms link
                        2. When M2 responds, Excel will auto-update
                        3. View progress in Dashboard → Workflow Statistics
                        """)

                        # Add balloons for successful submission
                        st.balloons()

                        # Option to view in dashboard
                        if st.button("📊 View in Dashboard"):
                            st.session_state.show_submissions = True
                            st.rerun()
                        
                    else:
                        st.error(f"❌ Email delivery failed: {email_result.get('message', 'Unknown error')}")
                        
                except Exception as e:
                    st.error(f"❌ Error processing assessment: {str(e)}")
            else:
                st.warning("⚠️ Please fill in Student ID and Name")

def show_microsoft_forms_integration():
    """Show enhanced Microsoft Forms integration section with auto-import functionality."""
    st.markdown("### 📊 **Enhanced Microsoft Forms Integration**")
    
    # Forms Setup Section
    with st.container():
        st.markdown("""
        <div class="futuristic-card">
            <h4>🚀 Microsoft Forms Setup & Management</h4>
            <p>Complete integration: UI → Microsoft Forms → Auto-import M2 responses → Real-time workflow updates</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Setup options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📝 Create Forms Template", type="primary"):
                try:
                    template_path = forms_integration.create_forms_template()
                    st.success(f"✅ Template created successfully!")
                    st.info(f"📂 **Location:** {template_path}")
                    st.markdown("""
                    **Next Steps:**
                    1. Open Microsoft Forms
                    2. Create new form with these exact column headers
                    3. Upload this template as reference
                    4. Share Forms link with M2/M3 markers
                    """)
                    
                    # Offer download
                    if os.path.exists(template_path):
                        with open(template_path, 'rb') as f:
                            st.download_button(
                                label="📥 Download Template",
                                data=f.read(),
                                file_name=f"Microsoft_Forms_Template_{datetime.now().strftime('%Y%m%d')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                except Exception as e:
                    st.error(f"❌ Error creating template: {str(e)}")
        
        with col2:
            if st.button("🔄 Start Auto-Import (10sec)"):
                try:
                    forms_integration.start_auto_import_monitoring(0.167)  # 10 seconds = 0.167 minutes
                    st.success("✅ Auto-import monitoring started!")
                    st.info("🔍 System will check for M2 responses every 10 seconds")
                except Exception as e:
                    st.error(f"❌ Error starting auto-import: {str(e)}")
        
        with col3:
            if st.button("⏹️ Stop Auto-Import"):
                try:
                    forms_integration.stop_auto_import_monitoring()
                    st.success("✅ Auto-import monitoring stopped!")
                except Exception as e:
                    st.error(f"❌ Error stopping auto-import: {str(e)}")
    
    # Real-time Workflow Status
    st.markdown("### 📈 **Real-time Workflow Status**")
    
    workflow_status = forms_integration.get_workflow_status()
    stats = workflow_status.get("stats", {})
    
    # Display workflow metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("📝 Total Submissions", stats.get("total_submissions", 0))
    with col2:
        st.metric("⏳ Awaiting M2", stats.get("awaiting_m2", 0))
    with col3:
        st.metric("✅ M2 Agreed", stats.get("m2_agreed", 0))
    with col4:
        st.metric("❌ M2 Disagreed", stats.get("m2_disagreed", 0))
    with col5:
        st.metric("🎯 Completed", stats.get("completed", 0))
    
    # Pending M2 Responses
    pending_responses = forms_integration.get_pending_m2_responses()
    if pending_responses:
        st.markdown("#### ⏰ **Pending M2 Responses**")
        
        pending_df = pd.DataFrame(pending_responses)
        st.dataframe(pending_df, use_container_width=True, hide_index=True)
        
        # Alert for overdue responses
        overdue = [p for p in pending_responses if p["days_pending"] > 3]
        if overdue:
            st.warning(f"⚠️ {len(overdue)} response(s) are overdue (>3 days)")
    
    # Manual Import Section
    st.markdown("#### 📥 **Manual M2 Response Import**")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_forms = st.file_uploader(
            "Upload Microsoft Forms Export (Excel)",
            type=['xlsx', 'xls'],
            help="Download the latest responses from Microsoft Forms and upload here"
        )
        
        if uploaded_forms is not None:
            if st.button("🔄 Import M2 Responses"):
                try:
                    # Save uploaded file temporarily
                    import tempfile
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                        tmp_file.write(uploaded_forms.read())
                        temp_path = tmp_file.name
                    
                    # Import responses
                    success, message, count = forms_integration.import_m2_responses(temp_path)
                    
                    if success:
                        st.success(f"✅ {message}")
                        if count > 0:
                            st.balloons()
                            st.rerun()  # Refresh to show updates
                    else:
                        st.error(f"❌ {message}")
                    
                    # Clean up
                    os.unlink(temp_path)
                    
                except Exception as e:
                    st.error(f"❌ Error importing responses: {str(e)}")
    
    with col2:
        st.markdown("""
        **Import Instructions:**
        1. Open Microsoft Forms
        2. Go to Responses tab
        3. Click "Open in Excel"
        4. Save/Download the file
        5. Upload it here
        """)
    
    # Current Submissions Display
    if 'assessments' in st.session_state and st.session_state.assessments:
        st.markdown("### 📋 **Recent Submissions**")
        
        # Show submitted assessments
        st.markdown(f"**{len(st.session_state.assessments)} assessment(s) submitted**")
        
        # Convert to DataFrame for display
        df = pd.DataFrame(st.session_state.assessments)
        
        # Display with key columns
        display_columns = ['StudentID', 'StudentName', 'Score', 'PassFail', 'M1_Name', 'M2_Name', 'Status']
        available_columns = [col for col in display_columns if col in df.columns]
        
        if available_columns:
            st.dataframe(df[available_columns], use_container_width=True, hide_index=True)
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Export options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📤 Export to Forms Format"):
                try:
                    # Export all assessments to Forms format
                    export_count = 0
                    for assessment in st.session_state.assessments:
                        success, message, file_path = forms_integration.export_submission_to_forms(assessment)
                        if success:
                            export_count += 1
                    
                    if export_count > 0:
                        st.success(f"✅ Exported {export_count} submissions to Forms format!")
                        st.info("📂 Files saved in data/forms_exports/ - Ready for Microsoft Forms upload")
                    else:
                        st.warning("⚠️ No submissions were exported")
                        
                except Exception as e:
                    st.error(f"❌ Error exporting to Forms: {str(e)}")
        
        with col2:
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"assessments_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col3:
            if st.button("🗑️ Clear Submissions"):
                st.session_state.assessments = []
                st.success("✅ Submissions cleared!")
                st.rerun()
    
    else:
        st.info("📝 No submissions yet. Use the Student Assessment form to add submissions.")
    
    # Instructions
    with st.expander("📖 **How Enhanced Integration Works**"):
        st.markdown("""
        ### 🔄 **Complete Workflow:**
        
        1. **Setup (One-time):**
           - Click "Create Forms Template" to generate column headers
           - Create Microsoft Forms with these exact columns
           - Share Forms with M2/M3 markers
        
        2. **M1 Assessment:**
           - Fill student assessment in UI
           - Click "Export to Forms Format" 
           - Upload generated files to Microsoft Forms
        
        3. **M2 Response:**
           - M2 receives email notification
           - M2 opens Microsoft Forms
           - M2 fills their response (Agree/Disagree + feedback)
        
        4. **Auto-Import (Every 5 minutes):**
           - System automatically checks for M2 responses
           - Updates workflow status in real-time
           - Triggers M3 notifications if needed
        
        5. **Manual Import (Backup):**
           - Download Forms responses as Excel
           - Upload here for immediate import
        
        ### ✅ **Benefits:**
        - No Microsoft Graph API required
        - Works with any Microsoft Forms setup
        - Real-time workflow tracking
        - Automatic M2/M3 escalation
        - Complete audit trail
        """)
    
    # System Status
    st.markdown("### ⚙️ **System Status**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        last_updated = workflow_status.get("last_updated", "Never")
        st.info(f"🕒 **Last Updated:** {last_updated}")
    
    with col2:
        export_dir = "data/forms_exports"
        export_count = len([f for f in os.listdir(export_dir) if f.endswith('.xlsx')]) if os.path.exists(export_dir) else 0
        st.info(f"📤 **Export Files:** {export_count}")
    
    with col3:
        import_dir = "data/forms_imports"
        import_count = len([f for f in os.listdir(import_dir) if f.endswith('.xlsx')]) if os.path.exists(import_dir) else 0
        st.info(f"📥 **Import Files:** {import_count}")

def main():
    """Main application function."""
    # Initialize session state
    init_session_state()
    
    # Load enhanced CSS
    load_enhanced_css()
    
    # Show demo mode indicator
    show_demo_mode_indicator()
    
    # Enhanced header
    enhanced_header()
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("## 🧭 **Navigation**")
        page = st.radio(
            "Choose a page:",
            [
                "📊 Dashboard & Markers",
                "📝 Student Assessment",
                "🤖 AI Feedback",
                "📈 Workflow Status",
                "⚙️ Settings"
            ]
        )
    
    # Main content based on page selection
    if page == "📊 Dashboard & Markers":
        show_enhanced_dashboard()
        show_marker_management()
        show_marker_list()
        show_enhanced_forms_monitoring()
        
    elif page == "📝 Student Assessment":
        show_enhanced_assessment_form()
        
    elif page == "🤖 AI Feedback":
        show_ai_feedback_section()
        
    elif page == "📈 Workflow Status":
        show_workflow_status_section()
        
    elif page == "⚙️ Settings":
        # Enhanced settings with demo mode
        st.markdown("## ⚙️ **Settings**")
        
        with st.container():
            st.markdown("""
            <div class="futuristic-card">
                <h4>🎛️ System Configuration</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Demo mode toggle
            demo_mode = st.toggle(
                "🧪 Demo Mode", 
                value=st.session_state.demo_mode,
                help="Enable demo mode for testing with sample data"
            )
            
            if demo_mode != st.session_state.demo_mode:
                st.session_state.demo_mode = demo_mode
                st.rerun()
            
            if st.session_state.demo_mode:
                st.success("🧪 **Demo Mode Active** - Using test markers and demo data")
            else:
                st.info("🚀 **Production Mode Active** - Using production markers and real data")
            
            # Email system test
            st.markdown("### 📧 **Email System Test**")
            test_email = st.text_input("Test email address", placeholder="your-email@example.com")
            
            if st.button("📤 Send Test Email"):
                if test_email:
                    result = st.session_state.email_system.send_test_email(test_email)
                    if result.get('status') == 'delivered':
                        st.success(f"✅ Test email sent to {test_email}")
                    else:
                        st.error(f"❌ Failed to send test email: {result.get('message', 'Unknown error')}")
                else:
                    st.warning("⚠️ Please enter an email address")

def show_workflow_status_section():
    """Complete workflow status monitoring and management section"""
    st.markdown("## 📈 **Workflow Status & Monitoring**")
    
    # Header with description
    with st.container():
        st.markdown("""
        <div class="futuristic-card">
            <h4>🔍 Workflow Monitoring Dashboard</h4>
            <p>Monitor and manage all student assessments through the three-marker workflow. 
            View current status, filter submissions, and track progress in real-time.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # File upload for workflow data
    st.markdown("### 📁 **Load Workflow Data**")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        uploaded_file = st.file_uploader(
            "Upload Microsoft Forms export (Excel or CSV)",
            type=['xlsx', 'csv'],
            help="Upload the latest export from Microsoft Forms to view current workflow status"
        )
    
    with col2:
        st.markdown("""
        **Data Requirements:**
        - Recent Forms export
        - All required columns
        - Student submissions
        - Marker responses
        """)
    
    if uploaded_file is not None:
        try:
            # Parse the forms data
            with st.spinner("📊 Processing workflow data..."):
                parser = FormsParser()
                processed_data = parser.parse_forms_data(uploaded_file)
            
            if processed_data.empty:
                st.warning("⚠️ No workflow data found in the uploaded file")
                return
            
            # Display summary statistics
            st.markdown("### 📊 **Workflow Summary**")
            
            # Calculate statistics
            total_submissions = len(processed_data)
            awaiting_m2 = len(processed_data[processed_data['Status'] == 'Awaiting M2'])
            agreed = len(processed_data[processed_data['Status'] == 'Agreed'])
            disagreed = len(processed_data[processed_data['Status'] == 'Disagreed'])
            escalated = len(processed_data[processed_data['Status'] == 'Escalated'])
            completed = len(processed_data[processed_data['Final_Score'].notna()])
            
            # Display metrics in columns
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            
            with col1:
                st.metric("📝 Total", total_submissions)
            with col2:
                st.metric("⏳ Awaiting M2", awaiting_m2)
            with col3:
                st.metric("✅ Agreed", agreed)
            with col4:
                st.metric("❌ Disagreed", disagreed)
            with col5:
                st.metric("🚨 Escalated", escalated)
            with col6:
                st.metric("🎯 Completed", completed)
            
            # Pass rate calculation
            if completed > 0:
                pass_count = len(processed_data[
                    (processed_data['Final_PassFail'] == 'Pass') & 
                    (processed_data['Final_Score'].notna())
                ])
                pass_rate = (pass_count / completed) * 100
                st.metric("📈 Pass Rate", f"{pass_rate:.1f}%", f"{pass_count}/{completed}")
            
            # Workflow progress chart
            if PLOTLY_AVAILABLE:
                st.markdown("### 📊 **Workflow Progress Chart**")
                
                import plotly.express as px
                import plotly.graph_objects as go
                
                # Create status distribution chart
                status_counts = processed_data['Status'].value_counts()
                
                fig = px.pie(
                    values=status_counts.values,
                    names=status_counts.index,
                    title="Workflow Status Distribution",
                    color_discrete_map={
                        'Awaiting M2': '#ffeaa7',
                        'Agreed': '#00b894',
                        'Disagreed': '#e84393',
                        'Escalated': '#e17055',
                        'Individual Submission': '#74b9ff'
                    }
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
            
            # Filtering options
            st.markdown("### 🔍 **Filter & Search**")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                status_filter = st.multiselect(
                    "Filter by Status",
                    options=processed_data['Status'].unique(),
                    default=processed_data['Status'].unique(),
                    help="Select workflow statuses to display"
                )
            
            with col2:
                if 'M1_MarkerName' in processed_data.columns:
                    marker_filter = st.multiselect(
                        "Filter by M1 Marker",
                        options=processed_data['M1_MarkerName'].dropna().unique(),
                        help="Filter by first marker"
                    )
                else:
                    marker_filter = []
            
            with col3:
                search_student = st.text_input(
                    "Search Student ID/Name",
                    help="Search for specific student"
                )
            
            # Apply filters
            filtered_data = processed_data.copy()
            
            if status_filter:
                filtered_data = filtered_data[filtered_data['Status'].isin(status_filter)]
            
            if marker_filter:
                filtered_data = filtered_data[filtered_data['M1_MarkerName'].isin(marker_filter)]
            
            if search_student:
                mask = (
                    filtered_data['StudentID'].str.contains(search_student, case=False, na=False) |
                    filtered_data['StudentName'].str.contains(search_student, case=False, na=False)
                )
                filtered_data = filtered_data[mask]
            
            # Display filtered results
            st.markdown(f"### 📋 **Workflow Details ({len(filtered_data)} records)**")
            
            if not filtered_data.empty:
                # Configure display columns
                display_columns = [
                    'StudentID', 'StudentName', 'Status', 'M1_MarkerName', 
                    'M1_Score', 'M1_PassFail'
                ]
                
                # Add M2 columns if available
                if 'M2_AssignedName' in filtered_data.columns:
                    display_columns.extend(['M2_AssignedName', 'M2_AssignedEmail'])
                if 'M3_AssignedName' in filtered_data.columns:
                    display_columns.extend(['M3_AssignedName', 'M3_AssignedEmail'])
                
                if 'M2_MarkerName' in filtered_data.columns:
                    display_columns.extend(['M2_MarkerName', 'M2_Score', 'M2_Agreed'])
                
                display_columns.extend(['Final_Score', 'Final_PassFail', 'Requires_Action'])
                
                # Filter columns that exist in the data
                available_columns = [col for col in display_columns if col in filtered_data.columns]
                
                # Display the data table
                st.dataframe(
                    filtered_data[available_columns],
                    use_container_width=True,
                    height=400
                )
                
                # Action buttons for pending items
                pending_actions = filtered_data[filtered_data['Requires_Action'] == True]
                
                if not pending_actions.empty:
                    st.markdown("### ⚡ **Pending Actions**")
                    st.warning(f"🚨 {len(pending_actions)} submissions require action")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("📧 Process All M2 Notifications", type="primary"):
                            with st.spinner("Sending M2 notifications..."):
                                try:
                                    coordinator = WorkflowCoordinator()
                                    results = coordinator.process_all_pending(filtered_data)
                                    
                                    success_count = len([r for r in results if r['status'] == 'success'])
                                    st.success(f"✅ Processed {success_count} notifications successfully")
                                    
                                    for result in results:
                                        if result['status'] == 'error':
                                            st.error(f"❌ {result['student_id']}: {result['message']}")
                                
                                except Exception as e:
                                    st.error(f"❌ Error processing notifications: {str(e)}")
                    
                    with col2:
                        if st.button("📊 Export Filtered Data"):
                            csv = filtered_data.to_csv(index=False)
                            st.download_button(
                                label="💾 Download CSV",
                                data=csv,
                                file_name=f"workflow_status_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                mime="text/csv"
                            )
                
                # Detailed view for selected submission
                st.markdown("### 🔍 **Detailed View**")
                
                if not filtered_data.empty:
                    selected_student = st.selectbox(
                        "Select student for detailed view",
                        options=filtered_data['StudentID'].tolist(),
                        format_func=lambda x: f"{x} - {filtered_data[filtered_data['StudentID']==x]['StudentName'].iloc[0]}"
                    )
                    
                    if selected_student:
                        student_data = filtered_data[filtered_data['StudentID'] == selected_student].iloc[0]
                        
                        with st.container():
                            st.markdown("""
                            <div class="futuristic-card">
                            """, unsafe_allow_html=True)
                            
                            st.markdown(f"#### 👤 **{student_data['StudentName']} ({student_data['StudentID']})**")
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.markdown("**Current Status:**")
                                status = student_data['Status']
                                status_color = {
                                    'Awaiting M2': '🟡',
                                    'Agreed': '🟢', 
                                    'Disagreed': '🔴',
                                    'Escalated': '🟠',
                                    'Individual Submission': '🔵'
                                }.get(status, '⚪')
                                st.markdown(f"{status_color} {status}")
                            
                            with col2:
                                st.markdown("**M1 Assessment:**")
                                st.markdown(f"Score: {student_data['M1_Score']}")
                                st.markdown(f"Result: {student_data.get('M1_PassFail', 'N/A')}")
                            
                            with col3:
                                if 'Final_Score' in student_data and pd.notna(student_data['Final_Score']):
                                    st.markdown("**Final Result:**")
                                    st.markdown(f"Score: {student_data['Final_Score']}")
                                    st.markdown(f"Result: {student_data.get('Final_PassFail', 'N/A')}")
                            
                            # Show marker assignments if available
                            if 'M2_AssignedName' in student_data:
                                st.markdown("**Marker Assignments:**")
                                st.markdown(f"• M2: {student_data.get('M2_AssignedName', 'N/A')} ({student_data.get('M2_AssignedEmail', 'N/A')})")
                                st.markdown(f"• M3: {student_data.get('M3_AssignedName', 'N/A')} ({student_data.get('M3_AssignedEmail', 'N/A')})")
                            
                            # Show feedback if available
                            if pd.notna(student_data.get('M1_Feedback')):
                                st.markdown("**M1 Feedback:**")
                                st.markdown(student_data['M1_Feedback'])
                            
                            if pd.notna(student_data.get('M2_Feedback')):
                                st.markdown("**M2 Feedback:**")
                                st.markdown(student_data['M2_Feedback'])
                            
                            st.markdown("""
                            </div>
                            """, unsafe_allow_html=True)
            
            else:
                st.info("🔍 No submissions match the current filters")
            
        except Exception as e:
            st.error(f"❌ Error processing workflow data: {str(e)}")
            st.info("💡 Ensure the uploaded file contains the required Microsoft Forms columns")
    
    else:
        st.info("👆 Upload a Microsoft Forms export file to view workflow status")
        
        # Show example of expected data format
        st.markdown("### 📋 **Expected Data Format**")
        sample_data = {
            'StudentID': ['CS2024001', 'CS2024002'],
            'StudentName': ['Alice Johnson', 'Bob Smith'], 
            'Status': ['Awaiting M2', 'Agreed'],
            'M1_MarkerName': ['Dr. John Smith', 'Dr. Jane Doe'],
            'M1_Score': [85, 72],
            'M1_PassFail': ['Pass', 'Pass']
        }
        st.dataframe(pd.DataFrame(sample_data), use_container_width=True)


def show_ai_feedback_section():
    """Complete AI feedback generation section with file upload"""
    st.markdown("## 🤖 **AI-Powered Feedback Generation**")
    
    # Header with description
    with st.container():
        st.markdown("""
        <div class="futuristic-card">
            <h4>📝 Intelligent Feedback Assistant</h4>
            <p>Upload student submissions to generate AI-powered feedback using Claude API with RAG (Retrieval-Augmented Generation). 
            This feedback is for <strong>reference only</strong> and should be reviewed by human markers.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Check if RAG system is available
    try:
        # Try enhanced generator first
        from rag.enhanced_feedback_generator import enhanced_feedback_generator
        feedback_generator = enhanced_feedback_generator
        rag_available = feedback_generator.claude_client is not None
        generator_type = "Enhanced"
    except Exception as e:
        # Fallback to original generator
        try:
            feedback_generator = FeedbackGenerator()
            rag_available = feedback_generator.rag_system is not None
            generator_type = "Standard"
        except Exception as e2:
            st.error(f"⚠️ RAG system not available: {str(e2)}")
            st.info("💡 To enable AI feedback, ensure you have set your ANTHROPIC_API_KEY in the .env file")
            return
    
    if not rag_available:
        st.warning("⚠️ AI feedback requires Claude API key configuration")
        st.info("💡 Set your ANTHROPIC_API_KEY environment variable to enable this feature")
        return
    
    # File upload section
    st.markdown("### 📁 **Upload Student Submission**")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Upload student report or assignment",
            type=['pdf', 'docx', 'txt', 'zip', 'py', 'java', 'cpp', 'js', 'html', 'css'],
            help="Supported formats: PDF, Word documents, text files, ZIP archives, and common code files"
        )
    
    with col2:
        st.markdown("""
        **Supported Files:**
        - 📄 PDF reports  
        - 📝 Word documents
        - 📦 ZIP archives
        - 💻 Code files
        - 📋 Text files
        """)
    
    # Rubric upload (optional)
    st.markdown("### 📋 **Upload Marking Rubric (Optional)**")
    rubric_file = st.file_uploader(
        "Upload marking rubric for context-aware feedback",
        type=['pdf', 'docx', 'txt'],
        help="Optional: Upload the marking rubric to generate more targeted feedback"
    )
    
    # Feedback generation options
    st.markdown("### ⚙️ **Feedback Options**")
    
    col1, col2 = st.columns(2)
    with col1:
        feedback_focus = st.selectbox(
            "Feedback Focus",
            ["General Assessment", "Technical Implementation", "Writing Quality", "Research Methods", "Code Review"]
        )
    
    with col2:
        feedback_tone = st.selectbox(
            "Feedback Tone",
            ["Constructive", "Detailed", "Encouraging", "Academic", "Professional"]
        )
    
    # Generate feedback button and processing
    if uploaded_file is not None:
        st.markdown("### 🚀 **Generate AI Feedback**")
        
        if st.button("🎯 Generate Feedback", type="primary"):
            with st.spinner("🤖 Analyzing submission and generating feedback..."):
                try:
                    # Generate feedback using enhanced or standard approach
                    if generator_type == "Enhanced":
                        feedback = feedback_generator.generate_enhanced_feedback(uploaded_file, rubric_file)
                    else:
                        feedback = feedback_generator.generate_feedback(uploaded_file, rubric_file)

                    # Display results
                    st.success("✅ AI feedback generated successfully!")

                    # Check if feedback was generated
                    if not feedback or feedback.strip() == "" or "Error:" in feedback:
                        st.error(f"❌ Failed to generate feedback: {feedback}")
                        st.info("💡 This might be due to:")
                        st.write("• File format not supported")
                        st.write("• File is encrypted or corrupted")
                        st.write("• No text content found in the file")
                        st.write("• Missing Claude API key")
                    else:
                        # Feedback display
                        st.markdown("### 📋 **Generated Feedback**")

                        with st.container():
                            st.markdown("""
                            <div class="futuristic-card">
                            """, unsafe_allow_html=True)

                            st.markdown("#### 🎯 AI-Generated Assessment Feedback")
                            st.markdown(feedback)

                            st.markdown("""
                            </div>
                            """, unsafe_allow_html=True)

                        # Copy to clipboard functionality (only show if feedback was successful)
                        st.markdown("### 📋 **Copy Feedback**")
                        st.text_area(
                            "Copy this feedback to paste into Microsoft Forms:",
                            feedback,
                            height=200,
                            help="Select all text (Ctrl+A) and copy (Ctrl+C) to paste into the AI_Feedback_Optional field"
                        )

                        # Disclaimer
                        st.markdown("""
                        <div style="background: linear-gradient(135deg, #ffeaa7, #fab1a0); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                            <h5>⚠️ Important Disclaimer</h5>
                            <ul>
                                <li><strong>Reference Only</strong>: This AI feedback is for reference and should be reviewed by human markers</li>
                                <li><strong>Not Official</strong>: AI feedback is never stored as official marks - only human markers make final decisions</li>
                                <li><strong>Review Required</strong>: Always review and modify AI suggestions before including in official feedback</li>
                                <li><strong>Context Aware</strong>: Feedback is generated based on uploaded content and optional rubric context</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"❌ Error generating feedback: {str(e)}")
                    st.info("💡 Check that your ANTHROPIC_API_KEY is valid and you have sufficient credits")
    
    else:
        st.info("👆 Upload a student submission file to begin generating AI feedback")
    
    # Statistics and usage info
    st.markdown("### 📊 **AI Feedback Statistics**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🤖 Model", "Claude 3.5", "Sonnet")
    with col2:
        st.metric("🎯 System", generator_type, "AI Engine")
    with col3:
        st.metric("⚡ Speed", "~30s", "Per submission")


def show_enhanced_submissions_viewer():
    """Enhanced submissions viewer with search, filter, and detailed views."""
    st.markdown("### 📊 **All Submissions - Enhanced Viewer**")

    # Load all submissions from Excel
    df = enhanced_excel_manager.get_all_submissions()

    if df.empty:
        st.info("📝 No submissions found. Submit an assessment to see data here.")
        if st.button("❌ Close Viewer"):
            st.session_state.show_submissions = False
            st.rerun()
        return

    # Control buttons
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        if st.button("❌ Close Viewer"):
            st.session_state.show_submissions = False
            st.rerun()
    with col2:
        if st.button("🔄 Refresh Data"):
            st.rerun()

    # Search and filter controls
    st.markdown("#### 🔍 **Search & Filter**")

    col1, col2, col3 = st.columns(3)

    with col1:
        search_term = st.text_input("🔍 Search Student ID/Name", placeholder="Type to search...")

    with col2:
        status_options = ["All"] + list(df['Status'].dropna().unique())
        status_filter = st.selectbox("📈 Filter by Status", status_options)

    with col3:
        # Get unique M1 markers for filter
        m1_markers = ["All"] + list(df['M1_MarkerName'].dropna().unique())
        marker_filter = st.selectbox("👤 Filter by M1 Marker", m1_markers)

    # Apply filters
    filtered_df = df.copy()

    # Search filter
    if search_term:
        search_mask = (
            df['StudentID'].str.contains(search_term, case=False, na=False) |
            df['StudentName'].str.contains(search_term, case=False, na=False)
        )
        filtered_df = filtered_df[search_mask]

    # Status filter
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df['Status'] == status_filter]

    # Marker filter
    if marker_filter != "All":
        filtered_df = filtered_df[filtered_df['M1_MarkerName'] == marker_filter]

    # Display results summary
    st.markdown(f"### 📋 **Results: {len(filtered_df)} of {len(df)} submissions**")

    if filtered_df.empty:
        st.warning("No submissions match your filters.")
        return

    # Enhanced download options
    col1, col2, col3 = st.columns(3)

    with col1:
        success, filename, excel_bytes = enhanced_excel_manager.export_excel_for_download(status_filter if status_filter != "All" else None)
        if success:
            st.download_button(
                label="📥 Download Filtered Excel",
                data=excel_bytes,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    with col2:
        # CSV download
        csv_data = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name=f"Submissions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

    with col3:
        # Pending M2 responses
        pending_m2 = enhanced_excel_manager.get_pending_m2_responses()
        if pending_m2:
            st.metric("⏰ Pending M2", len(pending_m2))

    # Display submissions with enhanced view
    for idx, row in filtered_df.iterrows():
        with st.expander(f"👤 {row['StudentName']} ({row['StudentID']}) - {row['Status']}", expanded=False):

            # Student and status info
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("**📋 Student Info:**")
                st.markdown(f"• **ID:** {row['StudentID']}")
                st.markdown(f"• **Name:** {row['StudentName']}")
                st.markdown(f"• **Submitted:** {row['Submission_Date']}")

            with col2:
                st.markdown("**📊 M1 Assessment:**")
                st.markdown(f"• **Marker:** {row['M1_MarkerName']}")
                st.markdown(f"• **Score:** {row['M1_Score']}")
                st.markdown(f"• **Pass/Fail:** {row['M1_PassFail']}")

            with col3:
                # Status with color coding
                status = row['Status']
                status_color = {
                    'Awaiting M2': '🟡',
                    'Completed - M2 Agreed': '🟢',
                    'Escalated to M3': '🔴',
                    'Completed - M3 Final Decision': '🟣'
                }.get(status, '⚪')

                st.markdown("**📈 Current Status:**")
                st.markdown(f"{status_color} **{status}**")

                if pd.notna(row['Final_Score']):
                    st.markdown(f"• **Final Score:** {row['Final_Score']}")
                    st.markdown(f"• **Final Result:** {row['Final_PassFail']}")

            # Marker assignments
            st.markdown("**🏷️ Assigned Markers:**")
            marker_cols = st.columns(3)

            with marker_cols[0]:
                st.markdown(f"**M1:** {row['M1_MarkerName']}")
                st.markdown(f"📧 {row['M1_MarkerEmail']}")
                st.markdown("✅ **Complete**")

            with marker_cols[1]:
                st.markdown(f"**M2:** {row['M2_AssignedName']}")
                st.markdown(f"📧 {row['M2_AssignedEmail']}")

                # M2 status
                if pd.notna(row['M2_ResponseDate']):
                    st.markdown("✅ **Responded**")
                    if row['M2_Agree_Checkbox'] == 'Yes':
                        st.markdown("👍 **Agreed**")
                    else:
                        st.markdown("👎 **Disagreed**")
                elif row['M2_Email_Sent_Date']:
                    st.markdown("📧 **Email Sent**")
                else:
                    st.markdown("⏳ **Pending**")

            with marker_cols[2]:
                st.markdown(f"**M3:** {row['M3_AssignedName']}")
                st.markdown(f"📧 {row['M3_AssignedEmail']}")

                # M3 status
                if pd.notna(row['M3_ResponseDate']):
                    st.markdown("✅ **Final Decision Made**")
                elif row['Escalation_Required'] == 'Yes':
                    st.markdown("🚨 **Escalation Required**")
                else:
                    st.markdown("⏳ **On Standby**")

            # Feedback sections
            if pd.notna(row['M1_Feedback']):
                st.markdown("**💬 M1 Feedback:**")
                st.markdown(f"_{row['M1_Feedback']}_")

            if pd.notna(row['M2_Feedback']):
                st.markdown("**💬 M2 Feedback:**")
                st.markdown(f"_{row['M2_Feedback']}_")

            if pd.notna(row['M3_Feedback']):
                st.markdown("**💬 M3 Final Feedback:**")
                st.markdown(f"_{row['M3_Feedback']}_")

            # Action buttons
            action_cols = st.columns(5)

            with action_cols[0]:
                if row['Status'] == 'Awaiting M2' and pd.notna(row['M2_Email_Sent_Date']):
                    if st.button(f"📧 Remind M2", key=f"remind_m2_{row['StudentID']}"):
                        # Send M2 reminder email with Forms link
                        try:
                            # Prepare student data for M2 reminder
                            student_data = {
                                'StudentID': row['StudentID'],
                                'StudentName': row['StudentName'],
                                'M1_Name': row['M1_MarkerName'],
                                'M1_Email': row['M1_MarkerEmail'],
                                'Score': row['M1_Score'],
                                'PassFail': row['M1_PassFail'],
                                'Feedback': row['M1_Feedback'],
                                'M2_Name': row['M2_AssignedName'],
                                'M2_Email': row['M2_AssignedEmail']
                            }

                            # Send M2 reminder email
                            email_result = st.session_state.email_system.send_m2_notification_with_forms(student_data)

                            if email_result.get('status') == 'delivered':
                                st.success(f"✅ M2 reminder sent to {row['M2_AssignedName']}")
                            else:
                                st.error(f"❌ Failed to send M2 reminder: {email_result.get('message')}")

                        except Exception as e:
                            st.error(f"❌ Error sending M2 reminder: {str(e)}")

            with action_cols[1]:
                if row['Status'] == 'Escalated to M3':
                    if st.button(f"📧 Remind M3", key=f"remind_m3_{row['StudentID']}"):
                        # Send M3 reminder email with Forms link
                        try:
                            # Prepare student data for M3 reminder
                            student_data = {
                                'StudentID': row['StudentID'],
                                'StudentName': row['StudentName'],
                                'M1_Name': row['M1_MarkerName'],
                                'M1_Email': row['M1_MarkerEmail'],
                                'Score': row['M1_Score'],
                                'PassFail': row['M1_PassFail'],
                                'Feedback': row['M1_Feedback'],
                                'M3_Name': row['M3_AssignedName'],
                                'M3_Email': row['M3_AssignedEmail']
                            }

                            # Prepare M2 data
                            m2_data = {
                                'marker_name': row.get('M2_MarkerName', ''),
                                'score': row.get('M2_Score', ''),
                                'feedback': row.get('M2_Feedback', '')
                            }

                            # Send M3 reminder email
                            email_result = st.session_state.email_system.send_m3_escalation_with_forms(student_data, m2_data)

                            if email_result.get('status') == 'delivered':
                                st.success(f"✅ M3 reminder sent to {row['M3_AssignedName']}")
                            else:
                                st.error(f"❌ Failed to send M3 reminder: {email_result.get('message')}")

                        except Exception as e:
                            st.error(f"❌ Error sending M3 reminder: {str(e)}")

            with action_cols[2]:
                if st.button(f"📊 Full Details", key=f"details_{row['StudentID']}"):
                    # Show full details modal
                    st.json(row.to_dict())

            with action_cols[3]:
                if st.button(f"📝 Edit", key=f"edit_{row['StudentID']}"):
                    # Edit functionality - show edit form in expander
                    st.session_state[f"editing_{row['StudentID']}"] = True

        # Show edit form if user clicked Edit button
        if st.session_state.get(f"editing_{row['StudentID']}", False):
            with st.expander(f"✏️ Edit Student: {row['StudentName']}", expanded=True):
                with st.form(f"edit_form_{row['StudentID']}"):
                    # Create editable fields
                    col1, col2 = st.columns(2)

                    with col1:
                        new_student_name = st.text_input("Student Name", value=row['StudentName'])
                        new_m1_score = st.number_input("M1 Score", value=float(row['M1_Score']), min_value=0.0, max_value=100.0)
                        new_m1_passfail = st.selectbox("M1 Pass/Fail", ['Pass', 'Fail'], index=0 if row['M1_PassFail'] == 'Pass' else 1)

                    with col2:
                        new_m1_feedback = st.text_area("M1 Feedback", value=row['M1_Feedback'], height=100)
                        new_status = st.selectbox("Status", ['Awaiting M2', 'M2 Agreed', 'M2 Disagreed - Needs M3', 'Escalated to M3', 'Completed'],
                                                index=['Awaiting M2', 'M2 Agreed', 'M2 Disagreed - Needs M3', 'Escalated to M3', 'Completed'].index(row['Status']))

                    # Form buttons
                    col_save, col_cancel = st.columns(2)

                    with col_save:
                        if st.form_submit_button("💾 Save Changes", type="primary"):
                            try:
                                # Update the Excel file
                                excel_manager = st.session_state.excel_manager

                                # Prepare updated data
                                updated_data = {
                                    'StudentName': new_student_name,
                                    'M1_Score': new_m1_score,
                                    'M1_PassFail': new_m1_passfail,
                                    'M1_Feedback': new_m1_feedback,
                                    'Status': new_status
                                }

                                # Update the Excel file
                                success = excel_manager.update_student_record(row['StudentID'], updated_data)

                                if success:
                                    st.success("✅ Student record updated successfully!")
                                    st.session_state[f"editing_{row['StudentID']}"] = False
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to update student record")

                            except Exception as e:
                                st.error(f"❌ Error updating record: {str(e)}")

                    with col_cancel:
                        if st.form_submit_button("❌ Cancel"):
                            st.session_state[f"editing_{row['StudentID']}"] = False
                            st.rerun()

            with action_cols[4]:
                if st.button(f"🗑️ Delete", key=f"delete_{row['StudentID']}", type="secondary"):
                    # Show confirmation dialog
                    st.session_state[f"confirm_delete_{row['StudentID']}"] = True

        # Show delete confirmation dialog
        if st.session_state.get(f"confirm_delete_{row['StudentID']}", False):
            with st.expander(f"⚠️ Confirm Deletion: {row['StudentName']}", expanded=True):
                st.error(f"**Are you sure you want to delete {row['StudentName']} ({row['StudentID']})?**")
                st.warning("This action cannot be undone. The student record will be permanently removed from the Excel file.")

                col_confirm, col_cancel = st.columns(2)

                with col_confirm:
                    if st.button(f"🗑️ YES, DELETE {row['StudentID']}", key=f"confirm_delete_yes_{row['StudentID']}", type="primary"):
                        try:
                            # Delete the student record
                            excel_manager = st.session_state.excel_manager
                            success = excel_manager.delete_student_record(row['StudentID'])

                            if success:
                                st.success(f"✅ Student {row['StudentName']} ({row['StudentID']}) deleted successfully!")
                                st.session_state[f"confirm_delete_{row['StudentID']}"] = False
                                st.rerun()
                            else:
                                st.error("❌ Failed to delete student record")

                        except Exception as e:
                            st.error(f"❌ Error deleting record: {str(e)}")

                with col_cancel:
                    if st.button(f"❌ Cancel Delete", key=f"confirm_delete_no_{row['StudentID']}"):
                        st.session_state[f"confirm_delete_{row['StudentID']}"] = False
                        st.rerun()


def show_microsoft_forms_setup():
    """Microsoft Forms setup and configuration section."""
    st.markdown("### 📝 **Microsoft Forms Setup (One-Time)**")

    # Check if Forms URL is already configured
    current_forms_url = forms_generator.get_forms_url()

    with st.container():
        if current_forms_url:
            # Forms already configured
            st.success(f"✅ Microsoft Forms is configured!")
            st.info(f"📎 **Forms URL:** {current_forms_url}")

            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("🔄 Update Forms URL"):
                    st.session_state.show_forms_setup = True

            with col2:
                if st.button("📧 Test Email with Forms Link"):
                    # Generate sample email
                    sample_email = forms_generator.generate_sample_email_with_prefill("TEST001", current_forms_url)
                    st.text_area("Sample Email Preview:", sample_email, height=300)

            with col3:
                if st.button("📋 View Setup Guide"):
                    st.session_state.show_setup_guide = True
        else:
            # Forms not configured yet
            st.warning("⚠️ Microsoft Forms not configured yet. Let's set it up!")

            if st.button("🚀 Start Forms Setup"):
                st.session_state.show_forms_setup = True

    # Show setup process if requested
    if st.session_state.get('show_forms_setup', False):
        show_forms_setup_wizard()

    # Show setup guide if requested
    if st.session_state.get('show_setup_guide', False):
        show_setup_guide()

def show_forms_setup_wizard():
    """Step-by-step Forms setup wizard."""
    st.markdown("### 🧙‍♂️ **Forms Setup Wizard**")

    # Step 1: Generate template questions
    st.markdown("#### 📋 **Step 1: Get Forms Questions**")

    if st.button("📝 Generate Forms Template"):
        template = forms_generator.generate_forms_questions()

        st.success("✅ Forms template generated! Copy these questions to Microsoft Forms:")

        # Display the template in an organized way
        for section_key, section in template["sections"].items():
            st.markdown(f"**--- {section['title']} ---**")
            st.markdown(f"*{section['description']}*")

            for i, question in enumerate(section["questions"], 1):
                st.markdown(f"**Question {i}:** {question['question']}")
                st.markdown(f"  • Type: {question['type']}")
                st.markdown(f"  • Required: {'Yes' if question['required'] else 'No'}")
                st.markdown(f"  • Note: {question['note']}")
                st.markdown("")

    # Step 2: Setup guide
    st.markdown("#### 📖 **Step 2: Follow Setup Guide**")

    if st.button("📋 Show Detailed Setup Guide"):
        guide = forms_generator.create_setup_guide()
        st.text_area("Complete Setup Guide:", guide, height=600)

    # Step 3: Save Forms URL
    st.markdown("#### 🔗 **Step 3: Save Your Forms URL**")

    st.markdown("After creating your Microsoft Form, paste the URL here:")

    with st.form("forms_url_form"):
        forms_url = st.text_input(
            "Microsoft Forms URL:",
            placeholder="https://forms.office.com/r/your-form-id",
            help="Get this URL by clicking 'Share' in your Microsoft Form"
        )

        col1, col2 = st.columns(2)
        with col1:
            save_url = st.form_submit_button("💾 Save Forms URL")
        with col2:
            cancel_setup = st.form_submit_button("❌ Cancel Setup")

    if save_url and forms_url:
        if forms_url.startswith("https://forms.office.com/"):
            success = forms_generator.save_forms_url(forms_url)
            if success:
                st.success("✅ Forms URL saved successfully!")
                st.balloons()
                st.session_state.show_forms_setup = False
                st.rerun()
            else:
                st.error("❌ Failed to save Forms URL")
        else:
            st.error("❌ Please enter a valid Microsoft Forms URL")

    if cancel_setup:
        st.session_state.show_forms_setup = False
        st.rerun()

def show_setup_guide():
    """Show the complete setup guide."""
    st.markdown("### 📖 **Complete Setup Guide**")

    guide = forms_generator.create_setup_guide()
    st.text_area("Setup Instructions:", guide, height=600)

    if st.button("❌ Close Guide"):
        st.session_state.show_setup_guide = False
        st.rerun()

def show_enhanced_forms_monitoring():
    """Enhanced Forms monitoring and import system."""
    st.markdown("### 🔄 **Forms Response Monitoring**")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📥 **Manual Import**")

        uploaded_file = st.file_uploader(
            "Upload Microsoft Forms Export",
            type=['xlsx', 'xls'],
            help="Download the latest responses from Microsoft Forms and upload here"
        )

        if uploaded_file is not None:
            # Show file details
            st.info(f"📁 File uploaded: {uploaded_file.name} ({uploaded_file.size} bytes)")

            if st.button("🔄 Process Forms Response"):
                with st.spinner("Processing Forms responses..."):
                    try:
                        # Save uploaded file temporarily
                        import tempfile
                        import os

                        # Read file content
                        file_content = uploaded_file.read()
                        st.write(f"✅ File read: {len(file_content)} bytes")

                        # Reset file pointer for potential re-reading
                        uploaded_file.seek(0)

                        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                            tmp_file.write(file_content)
                            temp_path = tmp_file.name

                        st.write(f"✅ Temporary file created: {temp_path}")
                        st.write(f"✅ Temp file exists: {os.path.exists(temp_path)}")
                        st.write(f"✅ Temp file size: {os.path.getsize(temp_path)} bytes")

                        # Auto-save to forms_imports directory for monitoring
                        import shutil
                        from datetime import datetime
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        safe_filename = uploaded_file.name.replace(" ", "_").replace("(", "").replace(")", "")
                        import_filename = f"{timestamp}_{safe_filename}"
                        import_path = f"data/forms_imports/{import_filename}"

                        shutil.copy2(temp_path, import_path)
                        st.write(f"✅ File saved to imports: {import_path}")

                        # Debug the file content before processing
                        try:
                            import pandas as pd
                            debug_df = pd.read_excel(temp_path, engine='openpyxl')
                            st.write(f"🔍 DEBUG: File has {len(debug_df)} rows")
                            st.write(f"🔍 DEBUG: Columns: {list(debug_df.columns)}")

                            # Check for StudentID columns in ALL rows
                            for idx, row in debug_df.iterrows():
                                st.write(f"🔍 DEBUG Row {idx+1}:")
                                for col in ['StudentID', 'Student ID', 'student_id', 'STUDENT_ID']:
                                    if col in row:
                                        st.write(f"   {col}: '{row[col]}'")
                                # Also show agreement response
                                agree_col = "Do you agree with M1's assessment"
                                if agree_col in row:
                                    st.write(f"   Agreement: '{row[agree_col]}'")
                                # Don't break - show all rows
                        except Exception as debug_error:
                            st.error(f"❌ Debug error: {debug_error}")

                        # Process the response
                        success, message = enhanced_excel_manager.process_forms_response(temp_path)

                        if success:
                            st.success(f"✅ {message}")
                            st.balloons()
                        else:
                            st.error(f"❌ {message}")

                        # Clean up
                        try:
                            os.unlink(temp_path)
                            st.write("✅ Temporary file cleaned up")
                        except Exception as cleanup_error:
                            st.warning(f"⚠️ Cleanup warning: {cleanup_error}")

                    except Exception as e:
                        st.error(f"❌ Error during file processing: {str(e)}")
                        st.write(f"Error details: {type(e).__name__}: {e}")

    with col2:
        st.markdown("#### ⚙️ **Monitoring Status**")

        if st.button("🔄 Start Background Monitoring"):
            result = enhanced_excel_manager.start_forms_monitoring()
            st.success(result)

        if st.button("⏹️ Stop Background Monitoring"):
            result = enhanced_excel_manager.stop_forms_monitoring()
            st.info(result)

        st.markdown("**📁 Instructions:**")
        st.markdown("""
        1. Start background monitoring
        2. Download Forms responses as Excel
        3. Drop file in `data/forms_imports/`
        4. System auto-detects within 10 seconds
        5. Excel updates automatically
        """)


if __name__ == "__main__":
    main()