#!/usr/bin/env python3
"""
Microsoft Forms Template Generator - Double-Marking AI Agent Automation

Creates a ready-to-upload Excel template with proper field structure for Microsoft Forms.
This template can be directly imported into Microsoft Forms to create the complete form.

Usage: python create_forms_template.py

Author: Double-Marking AI Agent Automation
"""

import pandas as pd
import os
from datetime import datetime
from pathlib import Path

def create_microsoft_forms_template():
    """Create comprehensive Microsoft Forms template with all required fields."""
    
    print("Creating Microsoft Forms Template...")
    print("=" * 60)
    
    # Define the complete column structure with field types and descriptions
    form_structure = [
        # Student Information
        {'name': 'StudentID', 'type': 'Text', 'required': True, 'description': 'Student ID (Pre-filled)'},
        {'name': 'StudentName', 'type': 'Text', 'required': True, 'description': 'Student Name (Pre-filled)'},
        {'name': 'Submission_Date', 'type': 'Date', 'required': False, 'description': 'Submission Date (Pre-filled)'},
        
        # M1 Assessment Data (Pre-filled, Read-only)
        {'name': 'M1_MarkerName', 'type': 'Text', 'required': False, 'description': 'First Marker Name (Pre-filled)'},
        {'name': 'M1_MarkerEmail', 'type': 'Text', 'required': False, 'description': 'First Marker Email (Pre-filled)'},
        {'name': 'M1_Score', 'type': 'Number', 'required': False, 'description': 'First Marker Score (Pre-filled)'},
        {'name': 'M1_PassFail', 'type': 'Choice', 'required': False, 'description': 'First Marker Pass/Fail (Pre-filled)'},
        {'name': 'M1_Feedback', 'type': 'Long Text', 'required': False, 'description': 'First Marker Feedback (Pre-filled)'},
        {'name': 'AI_Feedback_Optional', 'type': 'Long Text', 'required': False, 'description': 'AI Feedback (Pre-filled)'},
        
        # Marker Assignments (Pre-filled)
        {'name': 'M2_AssignedName', 'type': 'Text', 'required': False, 'description': 'Assigned Second Marker (Pre-filled)'},
        {'name': 'M2_AssignedEmail', 'type': 'Text', 'required': False, 'description': 'Second Marker Email (Pre-filled)'},
        {'name': 'M3_AssignedName', 'type': 'Text', 'required': False, 'description': 'Assigned Third Marker (Pre-filled)'},
        {'name': 'M3_AssignedEmail', 'type': 'Text', 'required': False, 'description': 'Third Marker Email (Pre-filled)'},
        
        # M2 Response Fields (Fillable by M2 Markers)
        {'name': 'M2_ResponseDate', 'type': 'Date', 'required': False, 'description': 'M2 Response Date (Auto-filled)'},
        {'name': 'M2_MarkerName', 'type': 'Text', 'required': False, 'description': 'M2 Marker Name (For verification)'},
        {'name': 'M2_Agree_Checkbox', 'type': 'Choice', 'required': True, 'description': 'Do you agree with M1? (Yes/No)', 'options': ['Yes', 'No']},
        {'name': 'M2_Score', 'type': 'Number', 'required': False, 'description': 'Your score (if different from M1)'},
        {'name': 'M2_PassFail', 'type': 'Choice', 'required': False, 'description': 'Your Pass/Fail (if different)', 'options': ['Pass', 'Fail']},
        {'name': 'M2_Feedback', 'type': 'Long Text', 'required': False, 'description': 'Your feedback'},
        {'name': 'M2_Comments', 'type': 'Long Text', 'required': False, 'description': 'Additional comments'},
        
        # M3 Response Fields (Fillable by M3 if escalated)
        {'name': 'M3_ResponseDate', 'type': 'Date', 'required': False, 'description': 'M3 Response Date (Auto-filled)'},
        {'name': 'M3_MarkerName', 'type': 'Text', 'required': False, 'description': 'M3 Marker Name (For verification)'},
        {'name': 'M3_Score', 'type': 'Number', 'required': False, 'description': 'Final score (M3 decision)'},
        {'name': 'M3_PassFail', 'type': 'Choice', 'required': False, 'description': 'Final Pass/Fail', 'options': ['Pass', 'Fail']},
        {'name': 'M3_Feedback', 'type': 'Long Text', 'required': False, 'description': 'Final feedback'},
        {'name': 'M3_Comments', 'type': 'Long Text', 'required': False, 'description': 'Final comments'},
        
        # Workflow Management Fields
        {'name': 'Final_Score', 'type': 'Number', 'required': False, 'description': 'System Final Score (Auto-calculated)'},
        {'name': 'Final_PassFail', 'type': 'Choice', 'required': False, 'description': 'System Final Result', 'options': ['Pass', 'Fail']},
        {'name': 'Status', 'type': 'Choice', 'required': False, 'description': 'Workflow Status', 'options': ['Awaiting M2', 'M2 Agreed', 'M2 Disagreed', 'Escalated to M3', 'Completed']},
        {'name': 'Escalation_Required', 'type': 'Choice', 'required': False, 'description': 'Escalation Flag', 'options': ['Yes', 'No']},
        {'name': 'Completion_Date', 'type': 'Date', 'required': False, 'description': 'Completion Date (Auto-filled)'}
    ]
    
    # Create the Excel template with sample data
    template_data = {}
    
    # Add column headers
    for field in form_structure:
        template_data[field['name']] = []
    
    # Create sample rows for demonstration
    sample_rows = [
        # Sample row 1 - Awaiting M2 response
        {
            'StudentID': 'STU001',
            'StudentName': 'John Smith',
            'Submission_Date': '2025-09-08',
            'M1_MarkerName': 'Dr. Jane Wilson',
            'M1_MarkerEmail': 'jane.wilson@keele.ac.uk',
            'M1_Score': 75,
            'M1_PassFail': 'Pass',
            'M1_Feedback': 'Good understanding of concepts, well-structured code',
            'AI_Feedback_Optional': 'Consider adding more error handling',
            'M2_AssignedName': 'Dr. Robert Brown',
            'M2_AssignedEmail': 'robert.brown@keele.ac.uk',
            'M3_AssignedName': 'Prof. Sarah Davis',
            'M3_AssignedEmail': 'sarah.davis@keele.ac.uk',
            'Status': 'Awaiting M2',
            'Escalation_Required': 'No',
            # All M2/M3 fields empty - to be filled by markers
        },
        
        # Sample row 2 - M2 Agreement example
        {
            'StudentID': 'STU002', 
            'StudentName': 'Alice Johnson',
            'Submission_Date': '2025-09-08',
            'M1_MarkerName': 'Dr. Michael Green',
            'M1_MarkerEmail': 'michael.green@keele.ac.uk',
            'M1_Score': 82,
            'M1_PassFail': 'Pass',
            'M1_Feedback': 'Excellent work with creative solutions',
            'M2_AssignedName': 'Dr. Lisa White',
            'M2_AssignedEmail': 'lisa.white@keele.ac.uk',
            'M3_AssignedName': 'Prof. David Lee',
            'M3_AssignedEmail': 'david.lee@keele.ac.uk',
            'M2_ResponseDate': '2025-09-08',
            'M2_MarkerName': 'Dr. Lisa White',
            'M2_Agree_Checkbox': 'Yes',
            'M2_Comments': 'I agree with the M1 assessment',
            'Final_Score': 82,
            'Final_PassFail': 'Pass',
            'Status': 'Completed',
            'Completion_Date': '2025-09-08'
        },
        
        # Sample row 3 - M2 Disagreement requiring M3
        {
            'StudentID': 'STU003',
            'StudentName': 'Bob Wilson',
            'Submission_Date': '2025-09-08',
            'M1_MarkerName': 'Dr. Emma Taylor',
            'M1_MarkerEmail': 'emma.taylor@keele.ac.uk',
            'M1_Score': 45,
            'M1_PassFail': 'Fail',
            'M1_Feedback': 'Needs significant improvement in logic',
            'M2_AssignedName': 'Dr. John Miller',
            'M2_AssignedEmail': 'john.miller@keele.ac.uk',
            'M3_AssignedName': 'Prof. Karen Black',
            'M3_AssignedEmail': 'karen.black@keele.ac.uk',
            'M2_ResponseDate': '2025-09-08',
            'M2_MarkerName': 'Dr. John Miller',
            'M2_Agree_Checkbox': 'No',
            'M2_Score': 55,
            'M2_PassFail': 'Pass',
            'M2_Feedback': 'I see evidence of understanding, borderline pass',
            'M2_Comments': 'Disagree with M1 - student shows understanding',
            'M3_ResponseDate': '2025-09-08',
            'M3_MarkerName': 'Prof. Karen Black',
            'M3_Score': 52,
            'M3_PassFail': 'Pass',
            'M3_Feedback': 'Final decision: borderline pass, meets minimum requirements',
            'Final_Score': 52,
            'Final_PassFail': 'Pass',
            'Status': 'Completed',
            'Escalation_Required': 'Yes',
            'Completion_Date': '2025-09-08'
        }
    ]
    
    # Populate template with sample data
    for row in sample_rows:
        for field in form_structure:
            field_name = field['name']
            template_data[field_name].append(row.get(field_name, ''))
    
    # Create DataFrame
    df = pd.DataFrame(template_data)
    
    # Ensure output directory exists
    output_dir = Path("data/forms_templates")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create template file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    template_path = output_dir / f"Microsoft_Forms_Complete_Template_{timestamp}.xlsx"
    
    # Save to Excel with proper formatting
    with pd.ExcelWriter(template_path, engine='openpyxl') as writer:
        # Main template sheet
        df.to_excel(writer, sheet_name='Forms_Template', index=False)
        
        # Field configuration sheet
        config_data = []
        for field in form_structure:
            config_data.append({
                'Field_Name': field['name'],
                'Field_Type': field['type'],
                'Required': 'Yes' if field.get('required') else 'No',
                'Description': field['description'],
                'Options': ', '.join(field.get('options', [])) if field.get('options') else ''
            })
        
        config_df = pd.DataFrame(config_data)
        config_df.to_excel(writer, sheet_name='Field_Configuration', index=False)
    
    print(f"SUCCESSFUL: Microsoft Forms template created successfully!")
    print(f"FILE LOCATION: {template_path}")
    print(f"TEMPLATE INCLUDES: {len(form_structure)} fields")
    print(f"SAMPLE DATA: {len(sample_rows)} example rows")
    print("")
    
    # Display field configuration
    print("Field Configuration Summary:")
    print("-" * 60)
    
    key_fields = [f for f in form_structure if f.get('required') or 'M2_' in f['name']]
    for field in key_fields:
        field_type = field['type']
        required = " (REQUIRED)" if field.get('required') else ""
        options = f" | Options: {', '.join(field.get('options', []))}" if field.get('options') else ""
        print(f"• {field['name']}: {field_type}{required}{options}")
    
    print("")
    print("Ready for Microsoft Forms Import:")
    print("1. Open Microsoft Forms")
    print("2. Create new form: 'Double-Marking Workflow'")
    print("3. Import this Excel file")
    print("4. Configure field types as shown in Field_Configuration sheet")
    print("5. Set M2_Agree_Checkbox as required Yes/No choice")
    print("")
    
    return str(template_path)

if __name__ == "__main__":
    template_path = create_microsoft_forms_template()
    print(f"Template ready for download: {template_path}")