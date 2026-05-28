# 📚 API Reference - Double-Marking Workflow System

This document provides comprehensive API reference documentation for all external services, modules, classes, and functions in the Double-Marking Workflow System.

## 🌐 External API Integration

### Claude API (Anthropic)

The system now uses Anthropic's Claude API for high-quality AI feedback generation.

#### Setup & Authentication
```bash
# Set environment variable
export ANTHROPIC_API_KEY="your-api-key-here"
```

```python
# Or initialize programmatically
from rag.feedback_generator import FeedbackGenerator
generator = FeedbackGenerator(api_key="your-api-key-here")
```

#### API Endpoints Used

**Base URL:** `https://api.anthropic.com/v1/`

##### Messages API
- **Endpoint:** `/messages`
- **Method:** POST
- **Model:** `claude-3-5-sonnet-20241022`

**Request Structure:**
```python
{
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 1500,
    "temperature": 0.7,
    "messages": [
        {
            "role": "user",
            "content": "Your prompt here"
        }
    ]
}
```

**Response Structure:**
```python
{
    "id": "msg_...",
    "type": "message",
    "role": "assistant", 
    "content": [
        {
            "type": "text",
            "text": "Generated feedback response"
        }
    ],
    "model": "claude-3-5-sonnet-20241022",
    "stop_reason": "end_turn",
    "usage": {
        "input_tokens": 1234,
        "output_tokens": 567
    }
}
```

#### Rate Limits & Pricing
- **Tier 1:** 5 requests/min, 25,000 tokens/min
- **Tier 2:** 50 requests/min, 40,000 tokens/min  
- **Tier 3:** 1,000 requests/min, 80,000 tokens/min

**Input Tokens:** $3.00 per million tokens
**Output Tokens:** $15.00 per million tokens

#### Error Handling
```python
# Standard error response
{
    "error": {
        "type": "invalid_request_error",
        "message": "Invalid API key provided"
    }
}
```

**Common Error Codes:**
- `400` - Invalid request format
- `401` - Invalid API key
- `403` - Forbidden request
- `429` - Rate limit exceeded
- `500` - Internal server error

### Microsoft Forms API

Microsoft Forms serves as the data source. The system processes Excel/CSV exports.

#### Required Form Schema
```python
REQUIRED_COLUMNS = {
    "StudentID": "Text (required)",
    "StudentName": "Text (required)", 
    "MarkerRole": "Choice (M1/M2/M3)",
    "MarkerName": "Text (required)",
    "MarkerEmail": "Email (required)",
    "Score": "Number (0-100)",
    "PassFail": "Choice (Pass/Fail)",
    "Feedback": "Long text",
    "AI_Feedback_Optional": "Long text",
    "M2_Agree_Checkbox": "Yes/No"
}
```

#### Export Formats Supported
- **Excel (.xlsx)** - Primary format
- **CSV (.csv)** - Alternative format  
- **TSV (.tsv)** - Tab-separated

### Microsoft Outlook COM API

Uses Windows COM interface for email automation.

#### Prerequisites
- Windows OS
- Microsoft Outlook Desktop installed
- Python `pywin32` package

#### COM Object Access
```python
import win32com.client
outlook = win32com.client.Dispatch("Outlook.Application")
```

#### Methods Used
- `CreateItem(0)` - Create email item
- `Send()` - Send email
- `GetNamespace("MAPI")` - Access MAPI namespace

This document provides detailed API reference for all modules, classes, and functions in the Double-Marking Workflow System.

## 📂 Module Structure

```
agent/
├── app/main.py                 # Streamlit GUI application
├── agents/workflow_coordinator.py  # Workflow orchestration
├── utils/
│   ├── forms_parser.py        # Microsoft Forms data processing
│   ├── outlook_automation.py  # Email automation
│   └── file_handler.py        # File processing utilities
└── rag/feedback_generator.py  # AI feedback generation
```

## 🖥️ GUI Application (app/main.py)

### Main Functions

#### `main()`
Primary Streamlit application entry point.

**Returns:**
- None

**Usage:**
```python
streamlit run app/main.py
```

#### `show_dashboard()`
Displays the main dashboard with file upload and statistics.

**Features:**
- Forms data upload and parsing
- Workflow statistics display
- Recent submissions overview

#### `show_process_submission()`
Handles manual and automatic submission processing.

**Features:**
- Individual submission processing
- Batch processing capabilities
- Action execution and results display

#### `show_ai_feedback()`
Interface for AI-powered feedback generation.

**Features:**
- File upload (PDF, DOCX, ZIP)
- Rubric integration
- Feedback generation and display

#### `show_workflow_status()`
Displays detailed workflow status and filtering options.

**Features:**
- Status filtering and search
- Data export functionality
- Real-time status updates

#### `show_settings()`
Configuration interface for system settings.

**Features:**
- Email configuration
- AI model parameters
- Connection testing

## 🔄 Workflow Coordination (agents/workflow_coordinator.py)

### WorkflowState Class

TypedDict defining the state object passed between workflow nodes.

**Fields:**
```python
student_id: str                 # Student identifier
action: str                     # Action to perform
forms_data: pd.DataFrame        # Current forms data
current_status: str             # Current workflow status
m1_data: Optional[Dict]         # M1 marker data
m2_data: Optional[Dict]         # M2 marker data
notification_sent: bool         # Email notification status
escalation_required: bool       # Escalation flag
final_score: Optional[float]    # Final agreed score
messages: List[str]             # Processing messages
error: Optional[str]            # Error information
```

### WorkflowCoordinator Class

Main workflow orchestration class using LangGraph.

#### `__init__()`
Initialize the workflow coordinator and build the graph.

#### `process_action(student_id: str, action: str, forms_data: pd.DataFrame) -> str`
Process a single workflow action for a student.

**Parameters:**
- `student_id`: Student identifier
- `action`: Action to perform ("Send M2 Notification", "Process Agreement", etc.)
- `forms_data`: Current forms data DataFrame

**Returns:**
- `str`: Result message

**Example:**
```python
coordinator = WorkflowCoordinator()
result = coordinator.process_action(
    student_id="CS2024001", 
    action="Send M2 Notification", 
    forms_data=df
)
```

#### `process_all_pending(forms_data: pd.DataFrame) -> List[Dict]`
Process all pending submissions automatically.

**Parameters:**
- `forms_data`: Current forms data DataFrame

**Returns:**
- `List[Dict]`: Results for each processed submission

### Workflow Nodes

#### `_intake_node(state: WorkflowState) -> WorkflowState`
Initial intake node - analyzes current submission status.

#### `_handoff_node(state: WorkflowState) -> WorkflowState`
Handoff node - manages marker transitions.

#### `_agreement_check_node(state: WorkflowState) -> WorkflowState`
Agreement check node - determines if M2 agrees with M1.

#### `_escalation_node(state: WorkflowState) -> WorkflowState`
Escalation node - prepares third marker notification.

#### `_finalization_node(state: WorkflowState) -> WorkflowState`
Finalization node - finalizes agreed marks.

#### `_notification_node(state: WorkflowState) -> WorkflowState`
Notification node - sends appropriate email notifications.

## 📊 Forms Data Processing (utils/forms_parser.py)

### FormsParser Class

Parses Microsoft Forms export data and derives workflow status.

#### Constants
```python
REQUIRED_COLUMNS = [
    'StudentID', 'StudentName', 'MarkerRole', 'MarkerName', 
    'MarkerEmail', 'Score', 'PassFail', 'Feedback', 
    'AI_Feedback_Optional', 'M2_Agree_Checkbox'
]
```

#### `__init__()`
Initialize the parser.

#### `parse_forms_data(uploaded_file) -> pd.DataFrame`
Parse uploaded Forms data and derive workflow status.

**Parameters:**
- `uploaded_file`: Streamlit uploaded file object (Excel or CSV)

**Returns:**
- `pd.DataFrame`: Processed data with derived status columns

**Example:**
```python
parser = FormsParser()
data = parser.parse_forms_data(uploaded_file)
print(f"Processed {len(data)} submissions")
```

#### `get_pending_notifications() -> List[Dict]`
Get list of submissions requiring notifications.

**Returns:**
- `List[Dict]`: Records requiring notifications

#### `get_summary_stats() -> Dict`
Get summary statistics for the dashboard.

**Returns:**
- `Dict`: Summary statistics including counts by status

### Private Methods

#### `_validate_columns()`
Validate that all required columns are present.

#### `_clean_data()`
Clean and standardize the data types and formats.

#### `_derive_workflow_status() -> pd.DataFrame`
Derive workflow status for each student based on submission patterns.

#### `_analyze_student_submissions(student_id: str, group: pd.DataFrame) -> List[Dict]`
Analyze submissions for a single student and determine workflow status.

#### `_determine_agreement_status(m1_record: pd.Series, m2_record: pd.Series) -> str`
Determine if M2 agrees with M1 and derive appropriate status.

#### `_create_record(m1_record: pd.Series, m2_record: Optional[pd.Series], status: str) -> Dict`
Create a processed record with all relevant information.

## 📧 Automated Email System (utils/automated_email_system.py)

### AutomatedEmailSystem Class

Handles real-time automated email delivery via Gmail SMTP for all workflow notifications.

#### `__init__()`
Initialize automated email system with Gmail SMTP configuration and environment variables.

#### `send_m2_notification(student_id: str, m1_data: Dict, m2_email: Optional[str] = None) -> Dict[str, str]`
Send automated notification to M2 that M1 has completed their marking.

**Parameters:**
- `student_id`: Student identifier
- `m1_data`: M1 marker information and scores
- `m2_email`: M2 email address (optional)

**Returns:**
- `Dict[str, str]`: Delivery status with details

**Example:**
```python
email_system = AutomatedEmailSystem()
result = email_system.send_m2_notification(
    student_id="CS2024001",
    m1_data={'marker_name': 'Dr. Smith', 'score': 85},
    m2_email="marker2@keele.ac.uk"  # Keele University marker
)
# Returns: {'status': 'delivered', 'delivery_time': '2024-01-15 14:30:25', 'recipients': ['marker2@keele.ac.uk']}
```

#### `send_escalation_email(student_id: str, m1_data: Dict, m2_data: Dict, m3_email: str = "moderator@keele.ac.uk") -> str`
Send escalation email to third marker when M1 and M2 disagree.

**Parameters:**
- `student_id`: Student identifier
- `m1_data`: M1 marker information
- `m2_data`: M2 marker information
- `m3_email`: Third marker email

**Returns:**
- `str`: Status message

#### `send_finalization_email(student_id: str, final_score: float, m1_email: str, m2_email: Optional[str] = None) -> str`
Send confirmation email when marking is finalized.

**Parameters:**
- `student_id`: Student identifier
- `final_score`: Final agreed score
- `m1_email`: First marker email
- `m2_email`: Second marker email

**Returns:**
- `str`: Status message

#### `send_m1_disagreement_notification(student_id: str, m1_data: Dict, m2_data: Dict) -> str`
Send notification to M1 that M2 has disagreed with their assessment.

**Parameters:**
- `student_id`: Student identifier
- `m1_data`: M1 marker information and assessment
- `m2_data`: M2 marker information and assessment

**Returns:**
- `str`: Status message

**Example:**
```python
outlook = OutlookAutomation()
result = outlook.send_m1_disagreement_notification(
    student_id="CS2024001",
    m1_data={'marker_name': 'Dr. Smith', 'score': 85, 'marker_email': 'smith@university.edu'},
    m2_data={'marker_name': 'Dr. Jones', 'score': 65}
)
```

#### `send_summary_report(summary_data: List[Dict], admin_email: str = "admin@cs.department.ac.uk") -> str`
Send daily/weekly summary report to administrators.

**Parameters:**
- `summary_data`: List of workflow summaries
- `admin_email`: Administrator email

**Returns:**
- `str`: Status message

#### `test_connection() -> Dict[str, str]`
Test Outlook connection and return status information.

**Returns:**
- `Dict`: Connection status and information

### Private Methods

#### `_initialize_outlook()`
Initialize connection to Outlook Desktop application.

#### `_create_email(to_recipients: str, cc_recipients: str = "", subject: str = "", body: str = "") -> Optional[object]`
Create a new email item.

## 📄 File Handling (utils/file_handler.py)

### FileHandler Class

Handles file uploads, validation, and processing.

#### Constants
```python
SUPPORTED_EXTENSIONS = {
    '.pdf': 'PDF Document',
    '.docx': 'Word Document', 
    '.zip': 'ZIP Archive',
    # ... more formats
}

MAX_FILE_SIZE_MB = 50
```

#### `__init__()`
Initialize the file handler.

#### `validate_file(uploaded_file) -> Tuple[bool, str]`
Validate uploaded file for size and format.

**Parameters:**
- `uploaded_file`: Streamlit uploaded file object

**Returns:**
- `Tuple[bool, str]`: (is_valid, message)

#### `save_temp_file(uploaded_file) -> str`
Save uploaded file to temporary location.

**Parameters:**
- `uploaded_file`: Streamlit uploaded file object

**Returns:**
- `str`: Path to temporary file

#### `analyze_zip_contents(zip_path: str) -> Dict[str, List[str]]`
Analyze contents of ZIP file.

**Parameters:**
- `zip_path`: Path to ZIP file

**Returns:**
- `Dict`: Categorized file contents

#### `get_file_info(uploaded_file) -> Dict[str, any]`
Get comprehensive information about uploaded file.

**Parameters:**
- `uploaded_file`: Streamlit uploaded file object

**Returns:**
- `Dict`: File information including validation status

#### `cleanup_temp_files()`
Clean up all temporary files created during session.

#### `create_file_summary_widget(uploaded_file)`
Create Streamlit widget showing file summary information.

**Parameters:**
- `uploaded_file`: Streamlit uploaded file object

### Utility Functions

#### `create_file_uploader_section(title: str, help_text: str, accepted_types: List[str], key: str) -> Optional[any]`
Create a standardized file uploader section for the Streamlit app.

**Parameters:**
- `title`: Section title
- `help_text`: Help text for users
- `accepted_types`: List of accepted file extensions
- `key`: Unique key for the uploader

**Returns:**
- Uploaded file object or None

## 🚀 Enhanced AI Feedback System (rag/enhanced_feedback_generator.py)

### Overview

The Enhanced AI Feedback System provides advanced multi-engine document processing with comprehensive content analysis and intelligent assessment assistance using Anthropic's Claude API.

### Key Enhanced Features
- 🚀 **Multi-Engine Document Processing**: Advanced PDF extraction with pdfplumber, PyMuPDF, PyPDF2, and OCR support
- 📊 **Comprehensive Format Support**: PDF, DOCX, ZIP archives, and 15+ programming languages
- 🔍 **Intelligent Content Analysis**: Automatic detection of tables, figures, academic sections, and code structure
- 💻 **Multi-Language Code Support**: Comprehensive analysis for Python, Java, C++, JavaScript, and more
- 🔄 **Robust Error Handling**: Graceful degradation with multiple extraction method fallbacks
- 📈 **Performance Optimized**: Memory-efficient processing with automatic content chunking
- 🎯 **Fallback Architecture**: Seamless integration with original system maintained as backup

### EnhancedDocumentProcessor Class

Advanced document processing with multiple extraction engines and intelligent content analysis.

#### `extract_text_from_pdf_advanced(file_path: str) -> Tuple[str, Dict]`
Extract text from PDF using multiple engines with automatic fallback.

**Processing Engines (in order of priority):**
1. **pdfplumber** - Best for tables and structured content
2. **PyMuPDF** - Excellent for complex layouts and figures
3. **PyPDF2** - Reliable fallback method
4. **OCR (Tesseract)** - Last resort for scanned documents

**Returns:**
- `Tuple[str, Dict]`: (extracted_text, metadata_dict)
- Metadata includes: character count, table count, processing method used

#### `extract_text_from_docx_advanced(file_path: str) -> Tuple[str, Dict]`
Enhanced DOCX processing with metadata extraction.

**Features:**
- Complete text extraction including headers/footers
- Table detection and formatting preservation
- Image counting and metadata analysis
- Structure analysis (headings, paragraphs, lists)

#### `extract_text_from_zip_advanced(file_path: str) -> Tuple[str, Dict]`
Multi-file ZIP processing with intelligent categorization.

**Capabilities:**
- Automatic file type detection and categorization
- Programming language-specific code analysis
- Document processing for mixed content archives
- Project structure analysis and documentation

#### `extract_text_from_code_file(file_path: str, language: str) -> str`
Programming language-specific analysis and documentation extraction.

**Supported Languages:**
- Python (.py), Java (.java), C++ (.cpp, .cxx, .cc)
- JavaScript (.js), TypeScript (.ts), C (.c, .h)
- And many more programming languages

### EnhancedFeedbackGenerator Class

Main interface for enhanced AI feedback generation.

#### `__init__(api_key: str = None)`
Initialize enhanced feedback generator with advanced processing capabilities.

#### `generate_enhanced_feedback(submission_file, rubric_file=None) -> str`
Generate comprehensive AI feedback using enhanced document processing.

**Parameters:**
- `submission_file`: Uploaded file object (supports all enhanced formats)
- `rubric_file`: Optional rubric file for context-aware feedback

**Returns:**
- `str`: Comprehensive feedback with structure and content analysis

**Example Usage:**
```python
from rag.enhanced_feedback_generator import enhanced_feedback_generator

# Generate enhanced feedback
feedback = enhanced_feedback_generator.generate_enhanced_feedback(
    submission_file=uploaded_file,
    rubric_file=rubric_file
)
```

## 🧠 AI Feedback System (rag/feedback_generator.py) - Legacy

### DocumentProcessor Class

Static methods for processing different document formats.

#### `extract_text_from_pdf(file_path: str) -> str`
Extract text from PDF file using PyPDF2.

#### `extract_text_from_docx(file_path: str) -> str`
Extract text from DOCX file using python-docx.

#### `extract_text_from_zip(file_path: str) -> Dict[str, str]`
Extract text from ZIP file containing documents.

### RAGSystem Class

Retrieval-Augmented Generation system for feedback generation using Claude API.

#### `__init__(api_key: str = None)`
Initialize the RAG system with Claude API client and embedding model.

**Parameters:**
- `api_key`: Anthropic API key (optional, can use ANTHROPIC_API_KEY env var)

#### `load_rubric(rubric_text: str)`
Load and process marking rubric for context.

#### `generate_feedback(submission_text: str, query: str = None) -> str`
Generate feedback using RAG approach.

**Parameters:**
- `submission_text`: Student submission content
- `query`: Optional specific query for feedback focus

**Returns:**
- `str`: Generated feedback text with disclaimer

#### `retrieve_relevant_context(query: str, k: int = 5) -> List[str]`
Retrieve most relevant document chunks for a query.

**Parameters:**
- `query`: Search query
- `k`: Number of chunks to retrieve

**Returns:**
- `List[str]`: Relevant text chunks

### FeedbackGenerator Class

Main interface for generating AI feedback on student submissions.

#### `__init__(api_key: str = None)`
Initialize feedback generator with RAG system and document processor.

**Parameters:**
- `api_key`: Anthropic API key (optional, can use ANTHROPIC_API_KEY env var)

#### `generate_feedback(submission_file, rubric_file=None) -> str`
Generate AI feedback for a student submission.

**Parameters:**
- `submission_file`: Uploaded submission file (PDF, DOCX, or ZIP)
- `rubric_file`: Optional rubric file for context

**Returns:**
- `str`: Generated feedback text

**Example:**
```python
# Initialize with API key
generator = FeedbackGenerator(api_key="your-claude-api-key")
feedback = generator.generate_feedback(
    submission_file=uploaded_file,
    rubric_file=rubric_file
)

# Or use environment variable
generator = FeedbackGenerator()  # Uses ANTHROPIC_API_KEY
```

#### `test_system() -> Dict[str, Any]`
Test the feedback generation system components.

**Returns:**
- `Dict`: Test results including model status and sample feedback

## 🔗 Integration Examples

### Complete Workflow Processing

```python
# Initialize components
parser = FormsParser()
coordinator = WorkflowCoordinator()
outlook = OutlookAutomation()

# Parse forms data
data = parser.parse_forms_data(forms_export_file)

# Process pending submissions
results = coordinator.process_all_pending(data)

# Generate summary report
stats = parser.get_summary_stats()
outlook.send_summary_report(results)
```

### AI Feedback Integration

```python
# Generate AI feedback
generator = FeedbackGenerator()
feedback = generator.generate_feedback(
    submission_file=student_report,
    rubric_file=marking_rubric
)

# Display in Streamlit
st.text_area("Generated Feedback", feedback, height=300)
```

### Custom Workflow Actions

```python
def custom_workflow_action(student_id: str, data: pd.DataFrame):
    # Custom processing logic
    coordinator = WorkflowCoordinator()
    
    # Execute standard action
    result = coordinator.process_action(
        student_id=student_id,
        action="Process Agreement",
        forms_data=data
    )
    
    # Add custom notifications or processing
    if "agreed" in result.lower():
        # Send custom congratulatory email
        pass
    
    return result
```

## 🚨 Error Handling

All classes implement comprehensive error handling:

- **Exception Logging**: All errors logged with context
- **Graceful Degradation**: System continues operating with reduced functionality
- **User Feedback**: Clear error messages displayed to users
- **Recovery Options**: Suggestions provided for resolving issues

## 🔧 Configuration Options

### Environment Variables
```python
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', 'your-claude-api-key-here')
DEFAULT_M3_EMAIL = os.getenv('DEFAULT_M3_EMAIL', 'moderator@keele.ac.uk')
MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', '50'))
DEBUG_MODE = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
```

### Runtime Configuration
```python
# Modify behavior at runtime
coordinator = WorkflowCoordinator()
coordinator.email_timeout = 60  # seconds
coordinator.auto_finalize = True  # Auto-finalize agreed marks
```

---

📖 **API Reference Complete** - All classes, methods, and integration patterns documented for the Double-Marking Workflow System.