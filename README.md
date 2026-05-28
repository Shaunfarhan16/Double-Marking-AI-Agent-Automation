# 🎓 Double-Marking AI Agent Automation

An advanced intelligent workflow coordinator that automates the three-marker double-marking process for Keele University's Computer Science department. This system features comprehensive marker management, seamless Microsoft Forms integration with auto-import functionality, real-time automated email delivery, and sophisticated workflow coordination across three markers (M1 → M2 → M3).

## 🎯 Features

### Enhanced Marker Management System
- **Pre-Registered Marker Database**: Local JSON storage with CRUD operations for marker management
- **Dropdown Marker Selection**: M1 efficiently selects M2 and M3 from pre-populated lists
- **Demo/Production Modes**: Toggle between test markers and live production markers
- **Three-Marker Workflow**: Complete M1 → M2 → M3 workflow with automatic assignments
- **Intelligent Agreement Detection**: Multi-signal detection of marker agreement/disagreement
- **Real-Time Status Monitoring**: Live workflow status tracking across all three markers

### Enhanced Microsoft Forms Integration with Pre-filled URLs
- **Pre-filled Forms URLs**: Student details automatically populate in Microsoft Forms links sent to M2/M3
- **Step-by-Step Setup Wizard**: Complete guide for creating Microsoft Forms with exact questions
- **✅ FIXED: Auto-Import System**: Background monitoring imports M2/M3 responses every 10 seconds with correct column mapping
- **✅ FIXED: Real-time Workflow Updates**: Automatic status tracking and M3 escalation triggers now work properly
- **No Graph API Required**: File-based integration works with any Microsoft Forms setup
- **Complete Template System**: Auto-generates Forms templates with 14 pre-defined questions
- **Forms URL Management**: Easy configuration and testing of Microsoft Forms integration
- **Workflow Status Dashboard**: Live metrics and pending response tracking

### Advanced Real-Time Email Automation with Forms Integration
- **✅ FIXED: Clickable Forms Links**: Microsoft Forms URLs are now properly clickable in all emails (HTML formatted)
- **✅ FIXED: Pre-filled Forms Data**: Student and M1 details automatically populate in Microsoft Forms using correct parameter names
- **✅ FIXED: M1 Escalation Notifications**: M1 now receives immediate notification when M2 disagrees with assessment
- **✅ FIXED: Agreement Detection Bug**: System correctly detects disagreement vs agreement (critical bug fixed)
- **✅ FIXED: Cumulative Forms Processing**: Handles Microsoft Forms exports with old + new data, filters duplicates automatically
- **Enhanced Email System**: M2/M3 emails include pre-filled Microsoft Forms links for easy response
- **Automatic M3 Escalation**: When M2 disagrees, M3 receives escalation email with Forms link automatically
- **🆕 M3 Final Decision Notifications**: Automatic notifications to M1, M2, and Student when M3 completes final assessment
- **🆕 Complete Email Workflow**: M1 and M3 both get immediate notifications on M2 disagreement
- **Gmail SMTP Integration**: Automated email delivery via smtp.gmail.com (no manual intervention)
- **Ultra-Fast Delivery**: Emails delivered within 5 seconds of workflow triggers
- **Three-Marker Support**: Automatic routing to assigned M2 and M3 markers from M1's selections
- **Cross-Provider Compatibility**: Gmail agent seamlessly emails Keele University Outlook accounts
- **Keele University Integration**: Professional templates with university branding and context
- **Comprehensive Delivery Tracking**: Detailed success/failure status monitoring with timestamps

### Enhanced AI Feedback System
- **🚀 Advanced Document Processing**: Multi-engine extraction supporting PDF (with tables/figures), DOCX (with metadata), ZIP archives (multi-file analysis)
- **🔧 Multiple Processing Engines**: Automatic fallback system with pdfplumber, PyMuPDF, PyPDF2, and OCR support for scanned documents
- **📊 Intelligent Content Analysis**: Automatic detection of academic sections, tables, figures, code structure, and references
- **💻 Multi-Language Code Support**: Comprehensive analysis for Python, Java, C++, JavaScript, and other programming languages
- **🎯 RAG-Powered Analysis**: Uses Claude API with retrieval-augmented generation for context-aware feedback
- **📋 Rubric Integration**: Incorporates marking rubrics for precise, criteria-based feedback generation
- **🔄 Robust Error Handling**: Graceful degradation with multiple extraction method fallbacks
- **📈 Performance Optimized**: Memory-efficient processing for large files with automatic content chunking
- **🎓 Reference Only**: AI feedback never stored as official marks - human markers maintain full authority

### Enhanced User Interface
- **Futuristic Streamlit GUI**: Advanced web interface with glassmorphism design and gradient styling
- **Marker Management Dashboard**: Comprehensive marker CRUD operations with real-time statistics
- **Student Assessment Form**: Enhanced form with dropdown marker selection from database
- **Demo/Production Toggle**: Easy switching between test and live marker sets
- **Real-Time Updates**: Live status monitoring across all three markers
- **Advanced File Management**: Drag-and-drop uploads with enhanced validation and processing
- **🆕 Enhanced Excel Management**: Complete CRUD operations for student submissions with working action buttons:
  - **📧 Remind M2/M3**: Send actual reminder emails with clickable Forms links
  - **📝 Edit**: Full edit form with real-time Excel updates and validation
  - **🗑️ Delete**: Safe deletion with confirmation dialog and Excel integration
  - **📊 Full Details**: Complete record view with JSON formatting

## 🏗️ Architecture

```
agent/
├── app/
│   └── main.py                 # Enhanced Streamlit application with Forms integration
├── agents/
│   └── workflow_coordinator.py # Enhanced LangGraph workflow with three-marker support
├── utils/
│   ├── enhanced_excel_manager.py    # NEW: NO-API Excel automation with 36-column workflow
│   ├── enhanced_email_system.py     # NEW: Email system with pre-filled Forms URLs
│   ├── forms_template_generator.py  # NEW: Microsoft Forms template generator with setup wizard
│   ├── marker_database.py           # Marker management with local JSON storage
│   ├── forms_integration.py         # Enhanced Microsoft Forms integration with auto-import
│   ├── forms_parser.py              # Enhanced with three-marker assignment parsing
│   └── automated_email_system.py    # Base email system with Gmail SMTP
├── rag/
│   └── feedback_generator.py   # Optional AI feedback system with Claude API
├── data/
│   ├── markers.json            # Local marker database storage
│   ├── forms_config.json       # Microsoft Forms URL configuration
│   ├── forms_imports/          # Auto-import directory for M2/M3 responses
│   └── forms_exports/          # Export directory for Excel files
├── docs/                       # Enhanced documentation
└── requirements.txt            # Updated Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Gmail account for automated agent (doublemarking.agent@gmail.com configured)
- Gmail App Password (16-character authentication: cnbz fqwh qtyx aqiv)
- Keele University email integration configured
- Windows OS (recommended) or Linux/macOS

### Installation

1. **Clone and Setup**
```bash
cd "C:\MSc Project\agent"
pip install -r requirements.txt
```

2. **Email System Setup (Required)**
```bash
# Create .env file with Gmail credentials (Keele University Configuration)
echo "AGENT_EMAIL=doublemarking.agent@gmail.com" > .env
echo "AGENT_APP_PASSWORD=cnbz fqwh qtyx aqiv" >> .env
echo "SMTP_SERVER=smtp.gmail.com" >> .env
echo "SMTP_PORT=587" >> .env
echo "UNIVERSITY_NAME=Keele University" >> .env
```

3. **Optional: AI Feedback Setup**
```bash
# Add Claude API key to .env file
echo "ANTHROPIC_API_KEY=your-claude-api-key-here" >> .env
```

4. **Enhanced Microsoft Forms Setup with Step-by-Step Wizard**
Use the application's built-in setup wizard:
- Go to the Dashboard → **Microsoft Forms Setup Wizard**
- **Step 1**: Review the auto-generated Forms template with 14 questions
- **Step 2**: Follow the detailed setup guide to create your Microsoft Form
- **Step 3**: Save your Forms URL in the system for pre-filled integration

**Forms Template Includes 14 Questions Across 3 Sections:**
- **Section 1 - Student Information (Pre-filled)**: `Student ID`, `Student Name`, `Assignment Title`
- **Section 2 - M1 Assessment (Pre-filled)**: `M1 Marker Name`, `M1 Score`, `M1 Pass/Fail`, `M1 Feedback`
- **Section 3 - Your Response**: `Your Name`, `Your Email`, `Do you agree?`, `If No - Score/Feedback`, `Additional Comments`

**Key Benefits:**
- **Pre-filled URLs**: Student details automatically populate in Forms links
- **Automatic M3 Escalation**: When M2 disagrees, M3 gets escalation email with Forms link
- **Real-time Processing**: Forms responses auto-import and update Excel within 10 seconds

### Running the Application

**Method 1: Using the Unified Launcher (Recommended)**
```bash
# Double-click or run from command line
run_agent.bat
```
This will give you options for:
- Local Access (individual use)
- Network Access (department deployment)  
- Legacy Mode (compatibility)

**Method 2: Direct Command Line**
```bash
# Enhanced application with Microsoft Forms integration
python -m streamlit run app/main.py --server.port 8501
```

The application will open in your default web browser at `http://localhost:8501`

## 📋 Usage Guide

### 1. Enhanced Dashboard with Microsoft Forms Integration
- **Marker Management**: Add, edit, delete markers with real-time statistics
- **Demo/Production Toggle**: Switch between test and live marker sets
- **Microsoft Forms Setup Wizard**: Step-by-step guide to create Forms with 14 questions
- **Forms URL Configuration**: Save and test Microsoft Forms URLs for pre-filled integration
- **Real-time Workflow Status**: Live metrics for submissions, M2 responses, completions
- **Auto-Import Controls**: Start/stop 10-second background monitoring
- **Manual Import**: Upload Forms exports for immediate processing
- **Pending Response Tracking**: Monitor overdue M2 responses with alerts

### 2. Enhanced Assessment Submission with Excel Auto-Population
- **Enhanced Assessment Form**: Submit student details with integrated marker selection
- **Dropdown Marker Selection**: Choose M2 and M3 from pre-populated database
- **Excel Auto-Population**: Submissions automatically populate 36-column Excel workflow
- **Pre-filled Forms Email**: M2 receives email with Forms link containing student details
- **Real-Time Processing**: Workflow initiated and tracking begins automatically

### 3. AI Feedback (Optional)
- Upload student reports (PDF, DOCX, ZIP)
- Upload marking rubric for context
- Generate AI-powered feedback
- Copy feedback to paste into Microsoft Forms

### 4. Enhanced Workflow Status with Real-time Updates
- **Live Dashboard**: Real-time metrics updated every 10 seconds from Forms
- **Auto-Import Status**: Background monitoring of M2/M3 responses
- **Pending Response Alerts**: Automatic detection of overdue submissions
- **Complete Audit Trail**: Track entire workflow from M1 → M2 → M3 with Excel integration
- **Export Capabilities**: Download 36-column Excel files and filtered reports

### 5. Settings and Testing
- Configure email addresses and test email delivery
- Microsoft Forms URL configuration and testing
- Adjust AI model parameters
- Test complete system integration

## 🔄 Enhanced Workflow Logic with Pre-filled Forms Integration

### Complete Automated Flow
1. **M1 Submission (UI)** → **Excel Auto-Population (36 columns)** → **M2 email with pre-filled Forms URL** → **Real-time tracking**
2. **M2 Response (Microsoft Forms)** → **Auto-import within 10 seconds** → **Agreement/Disagreement detection**
3. **If M2 Agrees** → **Mark as completed** → **Excel updated with final results**
4. **If M2 Disagrees** → **Automatic M3 Escalation** → **M3 email with Forms URL containing M1+M2 data**
5. **M3 Resolution** → **Final determination** → **Excel updated** → **Workflow complete**

### Real-Time Integration Workflow with Enhanced Features
- **M1 Submits in UI** → **Excel populated instantly** → **M2 notified with pre-filled Forms (< 5 seconds)**
- **M2 responds in Microsoft Forms** → **Auto-imported within 10 seconds** → **Status updated in real-time**
- **Agreement detected** → **Excel updated with final results** → **Workflow marked complete**
- **Disagreement detected** → **M3 escalation email sent automatically** → **Forms link includes all M1+M2 details**
- **Disagreement detected** → **M3 escalation triggered immediately** → **All parties notified**

### Pass/Fail Determination
- **Automatic Logic**: Score > 50 = Pass, Score ≤ 50 = Fail
- **Applied When**: Final score is determined (agreed submissions, individual submissions)
- **Manual Override**: Markers can manually set Pass/Fail in Microsoft Forms if needed
- **Clear Display**: Pass/fail results shown in dashboard metrics and workflow status

### Status States
- **Awaiting M2**: M1 completed, waiting for M2
- **Agreed**: M2 agreed with M1's assessment, final Pass/Fail determined
- **Disagreed**: M2 provided different assessment, awaiting M3 resolution
- **Escalated**: Third marker notified for resolution
- **Finalized**: Final score and Pass/Fail result recorded and communicated

### Agreement Detection
The system automatically detects agreement/disagreement by:
- Explicit M2 agreement checkbox
- Score differences between M1 and M2
- Pass/Fail status differences (considering >50 threshold)
- Extensive M2 feedback without agreement

## ⚙️ Configuration

### Email Settings
```env
# Gmail SMTP settings in .env file
AGENT_EMAIL=doublemarking-agent@gmail.com
AGENT_APP_PASSWORD=your_16_char_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Default recipients (Keele University)
DEFAULT_M3_EMAIL=moderator@keele.ac.uk
DEFAULT_ADMIN_EMAIL=admin@keele.ac.uk
EMAIL_FROM_NAME=Double-Marking System
```

### AI Settings
```python
# Claude API configuration in rag/feedback_generator.py
CLAUDE_MODEL = "claude-3-5-sonnet-20241022"
MAX_TOKENS = 1500
TEMPERATURE = 0.7
CHUNK_SIZE = 500
```

## 🔧 Troubleshooting

### Common Issues

**Automated Email System Not Working**
- Verify Gmail credentials in .env file are correct
- Ensure Gmail App Password (not regular password) is used
- Check internet connection and Gmail SMTP access
- Test with: `python test_automated_email_system.py`

**✅ FIXED: Microsoft Forms Links Not Clickable**
- Issue: Forms URLs appeared as plain text in emails
- Solution: Enhanced email system now sends HTML formatted emails with clickable links
- All emails now include properly styled, clickable Microsoft Forms buttons

**✅ FIXED: Pre-filled Forms Data Not Appearing**
- Issue: Student/M1 details not pre-filling in Microsoft Forms
- Solution: Updated URL parameter names to match exact Microsoft Forms question titles
- Use spaces in parameter names: "Student ID" instead of "StudentID"

**✅ FIXED: Forms Auto-Import Not Working**
- Issue: M2/M3 responses not updating UI automatically
- Solution: Fixed column name mapping to match actual Microsoft Forms export format
- Start auto-import monitoring: Click "🔄 Start Auto-Import (10sec)" in Dashboard
- Manual import: Use "📁 Manual Import Forms Export" for immediate processing

**✅ FIXED: Enhanced Excel Management Buttons Not Working**
- Issue: Edit/Delete buttons showed "functionality would go here"
- Solution: Implemented complete CRUD operations with Excel integration
- Added session state initialization for st.session_state.excel_manager
- All buttons now fully functional with real-time Excel updates

**✅ FIXED: Manual Forms Upload "No Valid Responses Found" Error**
- Issue: Manual form uploads were failing with "No valid responses found in Forms file"
- Root Cause: Column name mismatches ("Student ID" vs "StudentID") and duplicate response filtering
- Solution: Enhanced column name detection and proper duplicate filtering implementation
- Status: Completely resolved - manual uploads now work flawlessly

**✅ FIXED: Critical Agreement Detection Bug**
- Issue: "No - I disagree" was incorrectly detected as agreement due to substring matching
- Impact: M2 disagreements were processed as agreements, breaking the workflow
- Solution: Implemented proper positive/negative detection logic with explicit disagreement checks
- Result: System now correctly processes M2 disagreement and triggers M3 escalation

**Forms Data Not Loading**
- Check Excel/CSV file format matches schema
- Ensure all required columns are present
- Verify data types (numbers, booleans, text)
- Check column names match: "Do you agree with M1's assessment?", "If No, what score would you give?"

**AI Feedback Not Available**
- Install optional dependencies: `pip install anthropic sentence-transformers faiss-cpu`
- Set your Claude API key in `.env` file: `ANTHROPIC_API_KEY=your-key-here`
- Check API key is valid and has sufficient credits

**File Upload Issues**
- Ensure file size < 50MB
- Check supported formats: PDF, DOCX, ZIP, TXT
- Verify file is not corrupted

### Testing

**Test Automated Email System**
```python
from utils.automated_email_system import AutomatedEmailSystem
email_system = AutomatedEmailSystem()
result = email_system.test_connection()
print(result)

# Send test email
test_result = email_system.send_test_email("your-email@test.com")
print(test_result)
```

**Test AI Feedback**
```python
from rag.feedback_generator import FeedbackGenerator
generator = FeedbackGenerator()
test_results = generator.test_system()
print(test_results)
```

## 🔒 Security & Privacy

### Data Handling
- **Local Processing**: All data processing occurs locally
- **No Cloud Storage**: No data sent to external services
- **Temporary Files**: Automatically cleaned up after processing
- **Microsoft Forms**: Single source of truth for all official data

### AI Feedback
- **Reference Only**: AI feedback never stored as official marks
- **Cloud-based**: Uses Claude API for high-quality feedback generation
- **Human Oversight**: All final decisions made by human markers
- **Disclaimer**: All AI feedback clearly marked as reference material

### Email Security
- **Gmail SMTP**: Secure TLS-encrypted SMTP connection
- **App Password Authentication**: Uses secure Gmail App Passwords (not regular passwords)
- **Environment Variables**: Credentials stored securely in .env file
- **Professional Templates**: Branded academic email formatting with automated signatures

## 📈 Monitoring & Analytics

### Dashboard Metrics
- Total submissions processed
- Submissions awaiting M2 review
- Agreement rate between markers
- Escalation frequency
- Processing time statistics

### Export Capabilities
- CSV export of all workflow data
- Filtered exports by status or marker
- Summary reports for administrators
- Audit trails for compliance

## 🛠️ Development

### Architecture Decisions
- **LangGraph**: Agent orchestration and workflow management
- **Streamlit**: Rapid GUI development with Python
- **Pandas**: Data processing and analysis
- **smtplib**: Native Python SMTP for email delivery
- **FAISS**: Vector similarity search for RAG
- **Local-First**: No external dependencies for core functionality

### Extending the System
- Add new workflow states in `WorkflowCoordinator`
- Extend file format support in `DocumentProcessor`
- Customize email templates in `AutomatedEmailSystem`
- Add new AI models in `RAGSystem`

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch
3. Install development dependencies
4. Make changes and test
5. Submit pull request

### Code Standards
- Python 3.12+ compatibility
- Type hints for all functions
- Comprehensive error handling
- Logging for all operations
- Documentation for all modules

## 📜 License

This project is developed for the Computer Science department's internal use. All code is provided as-is for educational and operational purposes.

## 🆘 Support

For technical support or questions:
1. Check this documentation
2. Review log files in the application
3. Test system components individually
4. Contact the development team

---

**🤖 Generated with Claude Code** - Streamlining academic workflows through intelligent automation.