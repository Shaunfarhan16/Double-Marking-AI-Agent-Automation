# Microsoft Forms Template Guide - Double-Marking AI Agent Automation

## 📋 Enhanced Template Overview (Version 5.0)

**Template Generator**: Built-in Microsoft Forms Setup Wizard in application
**Purpose**: Step-by-step guide for creating Microsoft Forms with pre-filled URLs
**Excel Columns**: 36 comprehensive fields covering the entire marking process
**Forms Questions**: 14 questions across 3 sections with pre-filled integration

## 🏗️ Template Structure

### Student Information
- **StudentID**: Unique student identifier
- **StudentName**: Student's full name
- **Submission_Date**: When the assessment was submitted

### M1 (First Marker) Data
- **M1_MarkerName**: First marker's name
- **M1_MarkerEmail**: First marker's email
- **M1_Score**: Numerical score given by M1
- **M1_PassFail**: Pass/Fail decision by M1
- **M1_Feedback**: Detailed feedback from M1
- **AI_Feedback_Optional**: AI-generated feedback (optional)

### Marker Assignments
- **M2_AssignedName**: Assigned second marker's name
- **M2_AssignedEmail**: Assigned second marker's email
- **M3_AssignedName**: Assigned third marker's name (for escalation)
- **M3_AssignedEmail**: Assigned third marker's email

### M2 (Second Marker) Response Fields
- **M2_ResponseDate**: When M2 responded
- **M2_MarkerName**: M2's actual name (for verification)
- **M2_Agree_Checkbox**: Yes/No agreement with M1
- **M2_Score**: M2's score (if disagreeing)
- **M2_PassFail**: M2's Pass/Fail (if disagreeing)
- **M2_Feedback**: M2's feedback
- **M2_Comments**: Additional M2 comments

### M3 (Third Marker) Response Fields (If Escalated)
- **M3_ResponseDate**: When M3 responded
- **M3_MarkerName**: M3's actual name
- **M3_Score**: M3's final score
- **M3_PassFail**: M3's final Pass/Fail
- **M3_Feedback**: M3's feedback
- **M3_Comments**: Additional M3 comments

### Workflow Management
- **Final_Score**: System-determined final score
- **Final_PassFail**: System-determined final result
- **Status**: Current workflow status
- **Escalation_Required**: Yes/No escalation flag
- **Completion_Date**: When marking was completed

## 🚀 How to Use This Template

### Step 1: Create Microsoft Form
1. Go to [Microsoft Forms](https://forms.microsoft.com)
2. Click **"New Form"**
3. Give your form a title: "Double-Marking Workflow - M2/M3 Response"

### Step 2: Import Template Structure
1. Click **"More form settings"** (⚙️)
2. Select **"Import from Excel"**
3. Upload the template file: `Microsoft_Forms_Template_20250908.xlsx`
4. Microsoft Forms will create fields for each column

### Step 3: Configure Form Fields

**For M2 Markers (Primary Fields):**
- **M2_Agree_Checkbox**: Choice (Yes/No) - "Do you agree with M1's assessment?"
- **M2_Score**: Number - "Your score (if different from M1)"
- **M2_PassFail**: Choice (Pass/Fail) - "Your Pass/Fail decision"
- **M2_Feedback**: Long text - "Your feedback"
- **M2_Comments**: Long text - "Additional comments"

**For M3 Markers (If Escalated):**
- **M3_Score**: Number - "Final score"
- **M3_PassFail**: Choice (Pass/Fail) - "Final Pass/Fail decision"
- **M3_Feedback**: Long text - "Final feedback"
- **M3_Comments**: Long text - "Final comments"

### Step 4: Form Settings
- **Response options**: Allow one response per person
- **Permissions**: Restricted to your organization
- **Notifications**: Enable email notifications for responses

## 📤 Integration with Double-Marking System

### Auto-Export Process
1. System automatically exports submissions to Excel format
2. Files are saved to `data/forms_exports/`
3. Upload these files to populate your Microsoft Form

### Auto-Import Process  
1. Export responses from Microsoft Forms as Excel
2. Place files in `data/forms_imports/` 
3. System automatically imports M2/M3 responses every 5 minutes
4. Workflow status updates automatically

## 🔄 Workflow Integration

### M2 Process
1. M1 completes assessment → Auto-exported to Forms
2. M2 receives notification email
3. M2 accesses Microsoft Form with pre-populated M1 data
4. M2 reviews and responds using checkbox/fields
5. System auto-imports M2 response

### M3 Escalation Process
1. If M2 disagrees → Automatic escalation triggered
2. M3 receives notification with both M1 and M2 assessments
3. M3 accesses form with all previous data
4. M3 provides final decision
5. System imports final result

## ✅ Template Verification

**Status**: ✅ **VERIFIED COMPATIBLE**
- **Import Test**: Successful
- **Column Mapping**: Complete
- **Data Integrity**: Maintained
- **System Integration**: Functional

## 📁 File Locations

- **Template File**: `data/forms_exports/Microsoft_Forms_Template_20250908.xlsx`
- **Export Directory**: `data/forms_exports/` (outgoing to Forms)
- **Import Directory**: `data/forms_imports/` (incoming from Forms)

## 🛠️ Troubleshooting

### If Template Won't Import
- Ensure Excel file is not corrupted
- Check file format (.xlsx required)
- Verify Microsoft Forms supports your file size

### If Fields Don't Appear Correctly
- Check column header names match exactly
- Ensure no special characters in headers
- Verify data types are compatible

### If Auto-Import Fails
- Check file placement in `data/forms_imports/`
- Ensure exported Forms data matches template structure
- Verify file permissions

## 🎯 Best Practices

1. **Keep Template Updated**: Re-generate if system columns change
2. **Regular Testing**: Test import/export cycle periodically  
3. **Backup Data**: Keep copies of Forms exports
4. **Monitor Workflow**: Check auto-import logs regularly
5. **User Training**: Ensure M2/M3 markers understand the form

---

**🤖 Generated by Double-Marking AI Agent Automation - Template ready for production use!**