# Setup Guide - Double-Marking AI Agent Automation

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Microsoft Forms Configuration](#microsoft-forms-configuration)
4. [Outlook Setup](#outlook-setup)
5. [AI Features Setup (Optional)](#ai-features-setup-optional)
6. [Configuration](#configuration)
7. [Testing Your Installation](#testing-your-installation)
8. [Running the Application](#running-the-application)
9. [Troubleshooting](#troubleshooting)
10. [Security Considerations](#security-considerations)

## Prerequisites

### System Requirements
- **Operating System**: Windows 10/11 (required for Outlook automation)
- **Python**: 3.12 or higher
- **Microsoft Outlook**: Desktop version installed and configured
- **Memory**: Minimum 4GB RAM (8GB recommended for AI features)
- **Storage**: 2GB free space (additional space needed for AI models)

### Required Software
- **Python 3.12+**: Download from [python.org](https://www.python.org/downloads/)
- **Microsoft Outlook Desktop**: Part of Microsoft Office suite
- **Git**: For cloning the repository (optional)
- **Text Editor**: VS Code, Notepad++, or similar

### Optional Requirements (for AI Features)
- **Anthropic API Key**: Sign up at [anthropic.com](https://www.anthropic.com/)
- **Internet Connection**: Required for Claude API calls and downloading AI models

## Installation

### Step 1: Download the Project

**Option A: Download ZIP**
1. Download the project files to `C:\MSc Project\agent`
2. Extract all files maintaining the directory structure

**Option B: Git Clone (if available)**
```bash
git clone <repository-url> "C:\MSc Project\agent"
cd "C:\MSc Project\agent"
```

### Step 2: Verify Directory Structure
Ensure your directory structure matches:
```
C:\MSc Project\agent\
├── app/
│   ├── enhanced_main.py       # NEW: Enhanced application with marker management
│   └── main.py               # Legacy application (preserved)
├── agents/
│   └── workflow_coordinator.py # Enhanced with three-marker support
├── utils/
│   ├── marker_database.py     # NEW: Marker management system
│   ├── forms_parser.py        # Enhanced with three-marker parsing
│   ├── automated_email_system.py # NEW: Gmail SMTP automation
│   └── file_handler.py
├── rag/
│   └── feedback_generator.py
├── data/
│   └── markers.json          # NEW: Marker database storage
├── docs/
│   ├── API_REFERENCE.md
│   ├── SYSTEM_ARCHITECTURE.md
│   ├── THREE_MARKER_WORKFLOW.md # NEW: Three-marker documentation
│   ├── KEELE_UNIVERSITY_CONFIGURATION.md # NEW: University integration
│   └── SETUP_GUIDE.md (this file)
├── requirements.txt
├── test_marker_workflow.py   # NEW: Complete workflow testing
├── run_agent.bat
└── README.md
```

### Step 3: Create Python Virtual Environment (Recommended)

**Open Command Prompt as Administrator**
```bash
cd "C:\MSc Project\agent"
python -m venv venv
venv\Scripts\activate
```

### Step 4: Install Python Dependencies

**Core Dependencies (Required)**
```bash
pip install streamlit>=1.32.0
pip install pandas>=2.0.0
pip install pywin32>=306
pip install openpyxl>=3.1.0
pip install langgraph>=0.2.0
pip install langchain>=0.2.0
pip install langchain-core>=0.2.0
```

**Complete Installation (Recommended)**
```bash
pip install -r requirements.txt
```

### Step 5: Configure pywin32
After installing pywin32, run the post-install script:
```bash
python venv\Scripts\pywin32_postinstall.py -install
```

## Microsoft Forms Configuration

### Step 1: Create Microsoft Form

1. **Access Microsoft Forms**
   - Go to [forms.microsoft.com](https://forms.microsoft.com)
   - Sign in with your institutional account

2. **Create New Form**
   - Click "New Form"
   - Title: "Double-Marking Assessment Form"
   - Description: "Academic assessment form for double-marking process"

### Step 2: Add Required Fields

Add the following fields **in this exact order**:

#### Basic Information Fields
1. **StudentID** (Text)
   - Question: "Student ID"
   - Required: Yes
   - Format: Short answer

2. **StudentName** (Text)
   - Question: "Student Name"
   - Required: Yes
   - Format: Short answer

#### Marker Information Fields
3. **MarkerRole** (Choice)
   - Question: "Marker Role"
   - Required: Yes
   - Options: "M1", "M2", "M3"
   - Format: Drop-down

4. **MarkerName** (Text)
   - Question: "Marker Name"
   - Required: Yes
   - Format: Short answer

5. **MarkerEmail** (Text)
   - Question: "Marker Email"
   - Required: Yes
   - Format: Short answer

#### Assessment Fields
6. **Score** (Number)
   - Question: "Score (0-100)"
   - Required: Yes
   - Restrictions: Between 0 and 100

7. **PassFail** (Choice)
   - Question: "Pass/Fail (Optional - will be auto-determined if blank)"
   - Required: No
   - Options: "Pass", "Fail"
   - Format: Drop-down

8. **Feedback** (Long Text)
   - Question: "Feedback"
   - Required: No
   - Format: Long answer

9. **AI_Feedback_Optional** (Long Text)
   - Question: "AI Feedback (Reference Only)"
   - Required: No
   - Format: Long answer

#### Agreement Field (Critical)
10. **M2_Agree_Checkbox** (Yes/No)
    - Question: "I agree with M1's mark (M2 markers only)"
    - Required: No
    - Format: Yes/No choice

### Step 3: Form Settings Configuration

1. **Settings → Responses**
   - ✅ Accept responses: On
   - ✅ Allow multiple responses per person
   - ✅ Record name: On

2. **Settings → Who can fill out this form**
   - Select: "Only people in my organization"

3. **Settings → Response receipts**
   - ✅ Send receipt: On (optional)

### Step 4: Test Your Form

1. **Submit Test Data**
   ```
   StudentID: TEST001
   StudentName: Test Student
   MarkerRole: M1
   MarkerName: Test Marker
   MarkerEmail: test@university.edu
   Score: 75
   PassFail: (leave blank)
   Feedback: Test feedback
   AI_Feedback_Optional: (leave blank)
   M2_Agree_Checkbox: (leave blank)
   ```

2. **Export Test Data**
   - Go to "Responses" tab
   - Click "Open in Excel"
   - Save as Excel file for testing

## Automated Email System Setup

### Step 1: Gmail Account Setup (Required)

1. **Create Agent Gmail Account**
   - Create dedicated Gmail account: `doublemarking-agent@gmail.com`
   - Use strong password and enable 2-Factor Authentication
   - This account will send all automated notifications

2. **Generate Gmail App Password**
   - Go to Gmail Account → Security → 2-Step Verification
   - Click "App passwords" 
   - Select "Mail" and "Windows Computer"
   - Copy the 16-character app password (e.g., `abcd efgh ijkl mnop`)
   - **Save securely** - you won't see it again

3. **Verify SMTP Access**
   ```python
   # Test SMTP connection
   import smtplib
   server = smtplib.SMTP('smtp.gmail.com', 587)
   server.starttls()
   print("✅ Gmail SMTP accessible")
   ```

### Step 2: Configure Email Credentials

1. **Update .env File**
   Open `C:\MSc Project\agent\.env` and add:
   ```env
   # Gmail SMTP Configuration for Automated Agent
   AGENT_EMAIL=doublemarking-agent@gmail.com
   AGENT_APP_PASSWORD=your_16_char_app_password_here
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   
   # Email Display Settings
   EMAIL_FROM_NAME=Double-Marking System
   DEPARTMENT_NAME=Computer Science Department
   UNIVERSITY_NAME=Your University Name
   ```

2. **Test Automated Email System**
   ```python
   # Run this test script
   from utils.automated_email_system import AutomatedEmailSystem
   
   try:
       email_system = AutomatedEmailSystem()
       result = email_system.test_connection()
       if result['status'] == 'success':
           print("✅ Automated email system working")
           print(f"Connected as: {result['agent_email']}")
       else:
           print(f"❌ Connection failed: {result['message']}")
   except Exception as e:
       print(f"❌ Error: {e}")
   ```

### Step 3: Configure Default Recipients

The system uses these default Keele University email addresses (configurable in .env):
- **M3 Email**: `moderator@keele.ac.uk`
- **Admin Email**: `admin@keele.ac.uk`

Production configuration (already set):
```env
# Default Recipients for Production (Keele University)
DEFAULT_M3_EMAIL=moderator@keele.ac.uk
DEFAULT_ADMIN_EMAIL=admin@keele.ac.uk
```

## AI Features Setup (Optional)

### Step 1: Get Anthropic API Key

1. **Create Anthropic Account**
   - Go to [console.anthropic.com](https://console.anthropic.com)
   - Sign up for an account
   - Verify your email

2. **Generate API Key**
   - Go to "API Keys" section
   - Click "Create Key"
   - Copy the key (starts with `sk-ant-api03-`)
   - **Important**: Save this key securely - you won't see it again

### Step 2: Configure API Key

**Option A: Environment Variable (Recommended)**
```bash
# Windows Command Prompt
set ANTHROPIC_API_KEY=your-api-key-here

# PowerShell
$env:ANTHROPIC_API_KEY="your-api-key-here"

# Make permanent in Windows
setx ANTHROPIC_API_KEY "your-api-key-here"
```

**Option B: .env File**
1. Create `.env` file in the project root:
   ```
   ANTHROPIC_API_KEY=your-api-key-here
   ```
2. Add to `.gitignore` if using version control:
   ```
   .env
   ```

### Step 3: Install Enhanced AI Dependencies

**Enhanced AI Feedback System Dependencies:**
```bash
# Core AI and ML libraries
pip install anthropic>=0.7.0
pip install sentence-transformers>=2.2.0
pip install faiss-cpu>=1.7.0
pip install torch>=2.0.0
pip install transformers>=4.30.0
pip install numpy>=1.24.0

# Enhanced document processing (multi-engine support)
pip install pypdf2>=3.0.0           # PDF processing (fallback)
pip install pdfplumber>=0.9.0       # Advanced PDF extraction (primary)
pip install pymupdf>=1.23.0         # Complex PDF layouts (secondary)
pip install python-docx>=1.1.0      # DOCX document processing

# OCR and image processing
pip install pytesseract>=0.3.10     # OCR for scanned documents
pip install pillow>=9.0.0           # Image processing support
```

**Note**: The enhanced system provides multi-engine document processing with automatic fallback. If any advanced dependencies fail to install, the system will gracefully degrade to available engines.

### Step 4: Test AI Setup

Run the included test script:
```bash
python test_claude_integration.py
```

Expected output:
```
✅ PASS - Claude API connection successful
✅ PASS - Embedding model loaded successfully
✅ PASS - Feedback generation successful
```

## Configuration

### Step 1: Application Settings

When you first run the application, configure these settings:

#### Email Configuration
- **Default M3 Email**: Email for escalation notifications
- **Department Email**: Administrative notifications
- **Email Timeout**: Seconds to wait for email operations (default: 30)

#### AI Configuration
- **Claude Model**: `claude-3-5-sonnet-20241022` (fixed)
- **Max Tokens**: Maximum response length (default: 1500)
- **Temperature**: Creativity level 0.0-1.0 (default: 0.7)

#### Marking Configuration
- **Pass Threshold**: Score above which = Pass (default: 50)
- **Auto-determine Pass/Fail**: Automatically set based on score
- **Allow Manual Override**: Let markers manually set Pass/Fail

### Step 2: File Paths Configuration

Ensure these paths are accessible:
- **Forms Data**: Where you'll upload Microsoft Forms exports
- **Student Submissions**: Where AI feedback files are stored
- **Temp Directory**: System temporary files (auto-managed)

## Testing Your Installation

### Step 1: Basic System Test

```bash
cd "C:\MSc Project\agent"
python -c "
import pandas as pd
import streamlit as st
print('✅ Core dependencies working')
"
```

### Step 2: Forms Parser Test

```bash
python -c "
from utils.forms_parser import FormsParser
parser = FormsParser()
print('✅ Forms parser working')
"
```

### Step 3: Outlook Test

```bash
python -c "
from utils.outlook_automation import OutlookAutomation
outlook = OutlookAutomation()
result = outlook.test_connection()
print(f'Outlook status: {result}')
"
```

### Step 4: AI Features Test (if configured)

```bash
python test_simple.py
```

### Step 5: Complete Integration Test

```bash
python test_claude_integration.py
```

## Running the Application

### Method 1: Batch File (Recommended)

Double-click `run_agent.bat` or run from command prompt:
```bash
run_agent.bat
```

### Method 2: Command Line

```bash
cd "C:\MSc Project\agent"
streamlit run app/main.py
```

### Method 3: Python Direct

```bash
cd "C:\MSc Project\agent"
python -m streamlit run app/main.py
```

### Accessing the Application

1. **Automatic Browser Opening**: Application should open automatically
2. **Manual Access**: Navigate to `http://localhost:8501`
3. **Network Access**: Use `http://your-computer-ip:8501` for network access

## Troubleshooting

### Common Issues and Solutions

#### Installation Issues

**Problem**: `pip install` fails with permission errors
```bash
# Solution: Use --user flag or run as administrator
pip install --user -r requirements.txt
```

**Problem**: Python not found
```bash
# Solution: Add Python to PATH or use full path
C:\Users\YourName\AppData\Local\Programs\Python\Python312\python.exe -m pip install streamlit
```

#### Outlook Issues

**Problem**: "Outlook not available" error
- **Solution 1**: Ensure Outlook Desktop is installed (not web version)
- **Solution 2**: Open Outlook and keep it running
- **Solution 3**: Run as administrator

**Problem**: COM object errors
```bash
# Solution: Reinstall pywin32
pip uninstall pywin32
pip install pywin32
python venv\Scripts\pywin32_postinstall.py -install
```

#### Microsoft Forms Issues

**Problem**: "Missing required columns" error
- **Solution**: Verify form field names match exactly:
  - `StudentID`, `StudentName`, `MarkerRole`, `MarkerName`, `MarkerEmail`
  - `Score`, `PassFail`, `Feedback`, `AI_Feedback_Optional`, `M2_Agree_Checkbox`

**Problem**: Data type conversion errors
- **Solution**: Ensure Score field is set to "Number" type in Forms
- **Solution**: Check M2_Agree_Checkbox is "Yes/No" choice type

#### AI Features Issues

**Problem**: "RAG dependencies not available" warning
```bash
# Solution: Install AI dependencies
pip install anthropic sentence-transformers faiss-cpu
```

**Problem**: "Invalid API key" error
- **Solution 1**: Verify API key is correct and active
- **Solution 2**: Check environment variable is set
- **Solution 3**: Restart command prompt after setting environment variable

**Problem**: Claude API rate limiting
- **Solution**: Wait and retry, or upgrade API plan

#### Application Issues

**Problem**: Streamlit won't start
```bash
# Solution: Check port availability
netstat -an | find "8501"
# If port is busy, specify different port
streamlit run app/main.py --server.port 8502
```

**Problem**: "Module not found" errors
- **Solution**: Ensure you're in the correct directory and virtual environment is activated
```bash
cd "C:\MSc Project\agent"
venv\Scripts\activate
```

### Debugging Tools

#### Enable Debug Logging
Add to your Python startup:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### Check System Status
```bash
# Test all components
python -c "
from utils.forms_parser import FormsParser
from utils.outlook_automation import OutlookAutomation
from rag.feedback_generator import FeedbackGenerator

print('Forms Parser:', 'OK' if FormsParser() else 'FAIL')
outlook = OutlookAutomation()
print('Outlook:', outlook.test_connection()['status'])
print('AI Features:', 'OK' if FeedbackGenerator().rag_system else 'DISABLED')
"
```

#### Log Files Location
Check these locations for error logs:
- Application logs: Console output
- Streamlit logs: `~/.streamlit/logs/`
- Windows Event Viewer: Application logs

## Security Considerations

### Data Protection

1. **Local Processing**
   - All workflow data processed locally
   - No cloud storage of sensitive academic data
   - Temporary files automatically cleaned up

2. **API Key Security**
   - Store API keys in environment variables, not code
   - Use .env file for development only
   - Never commit API keys to version control

3. **Email Security**
   - Uses existing Outlook authentication
   - No email credentials stored in application
   - Emails displayed for review before sending

### Access Control

1. **Microsoft Forms**
   - Set to "Organization only" access
   - Configure appropriate sharing permissions
   - Regular review of form responses

2. **Application Access**
   - Runs on localhost by default (secure)
   - For network access, consider firewall rules
   - Implement organizational access policies

### Privacy Compliance

1. **Student Data**
   - Ensure compliance with FERPA/GDPR requirements
   - Document data processing procedures
   - Implement data retention policies

2. **AI Processing**
   - AI feedback clearly marked as reference-only
   - Consider data residency requirements for Claude API
   - Maintain audit logs of AI interactions

## Performance Optimization

### System Performance

1. **Memory Management**
   - Close unnecessary applications
   - Monitor memory usage during AI processing
   - Consider RAM upgrade for heavy AI usage

2. **Storage Optimization**
   - Regular cleanup of temporary files
   - Archive old forms data periodically
   - Monitor disk space usage

### Application Performance

1. **Streamlit Optimization**
   - Use caching for expensive operations
   - Limit concurrent users if needed
   - Monitor browser memory usage

2. **AI Processing**
   - Batch process multiple submissions
   - Cache embedding models
   - Consider local AI alternatives for offline use

## Maintenance

### Regular Tasks

1. **Weekly**
   - Check application logs for errors
   - Verify Outlook connection
   - Test email notifications

2. **Monthly**
   - Update Python dependencies
   - Archive completed assessments
   - Review AI feedback quality

3. **Quarterly**
   - Security review of API keys
   - Performance optimization review
   - User training updates

### Updates

1. **Dependency Updates**
   ```bash
   pip list --outdated
   pip install --upgrade package-name
   ```

2. **Application Updates**
   - Backup current configuration
   - Test updates in development environment
   - Document changes and rollback procedures

### Backup Procedures

1. **Configuration Backup**
   - Save .env file securely
   - Export application settings
   - Document custom modifications

2. **Data Backup**
   - Regular exports of Microsoft Forms data
   - Archive processed assessments
   - Backup custom email templates

---

## Quick Start Checklist

### ✅ Pre-Installation
- [ ] Windows 10/11 system
- [ ] Python 3.12+ installed
- [ ] Microsoft Outlook Desktop installed and configured
- [ ] Administrator access available

### ✅ Installation
- [ ] Project files extracted to `C:\MSc Project\agent`
- [ ] Virtual environment created and activated
- [ ] Dependencies installed from requirements.txt
- [ ] pywin32 post-install configuration completed

### ✅ Microsoft Forms
- [ ] Form created with exact field names
- [ ] All 10 required fields added in correct order
- [ ] Form settings configured for organization access
- [ ] Test submission completed and exported

### ✅ Outlook Setup
- [ ] Outlook Desktop running and configured
- [ ] COM automation test successful
- [ ] Default email addresses configured
- [ ] Test email creation successful

### ✅ AI Features (Optional)
- [ ] Anthropic API key obtained
- [ ] API key configured in environment variable
- [ ] AI dependencies installed
- [ ] Claude API test successful

### ✅ Testing
- [ ] Basic system test passed
- [ ] Forms parser test passed
- [ ] Outlook automation test passed
- [ ] AI features test passed (if enabled)
- [ ] Complete integration test passed

### ✅ First Run
- [ ] Application starts successfully
- [ ] Dashboard loads without errors
- [ ] File upload works
- [ ] Settings accessible and configurable

---

## Support Resources

### Documentation
- **System Architecture**: `docs/SYSTEM_ARCHITECTURE.md`
- **API Reference**: `docs/API_REFERENCE.md`
- **README**: Root level overview and features

### Test Scripts
- **`test_claude_integration.py`**: Comprehensive AI testing
- **`test_simple.py`**: Quick Claude API test
- **`test_direct.py`**: Direct API key testing

### Community Resources
- **Streamlit Documentation**: [docs.streamlit.io](https://docs.streamlit.io)
- **Anthropic API Docs**: [docs.anthropic.com](https://docs.anthropic.com)
- **Microsoft Forms Help**: [support.microsoft.com](https://support.microsoft.com/en-us/office/microsoft-forms)

### Getting Help

If you encounter issues not covered in this guide:

1. **Check the logs** for specific error messages
2. **Run the test scripts** to identify component failures
3. **Review the troubleshooting section** for common solutions
4. **Consult the system architecture documentation** for technical details
5. **Contact your system administrator** for institutional support

---

*This setup guide provides complete installation and configuration instructions for the Agentic AI Double-Marking Workflow System. Follow the steps sequentially for the best results.*