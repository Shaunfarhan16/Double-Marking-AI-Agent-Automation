#!/usr/bin/env python3
"""
Create sample M2 response for testing folder-drop automation
"""

import pandas as pd
from datetime import datetime
import os

def create_sample_m2_response():
    """Create a sample M2 response file simulating Microsoft Forms export."""

    # Sample M2 response data (simulating Forms export)
    m2_response_data = {
        # Pre-filled from Forms URL (student info)
        'StudentID': ['TEST001'],
        'StudentName': ['Alice Test Student'],
        'M1_MarkerName': ['Dr. Test Marker'],
        'M1_Score': [85],
        'M1_Feedback': ['Excellent work with good understanding of concepts.'],
        'M1_PassFail': ['Pass'],

        # M2's actual response
        'Your Name': ['Dr. Second Marker'],
        'Your Email': ['second.marker@keele.ac.uk'],
        'Do you agree with M1\'s assessment?': ['Yes'],  # M2 agrees
        'If No, what score would you give?': [''],  # Empty since M2 agreed
        'If No, what is your feedback?': [''],  # Empty since M2 agreed
        'Additional Comments': ['I agree with the assessment. Well done by the student.'],

        # System fields
        'Submission_Date': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    }

    # Create DataFrame
    df = pd.DataFrame(m2_response_data)

    # Save to imports folder
    import_path = "data/forms_imports/M2_Response_TEST001.xlsx"
    df.to_excel(import_path, index=False, engine='openpyxl')

    print(f"Created sample M2 response: {import_path}")
    print("M2 Response Details:")
    print(f"  Student: {m2_response_data['StudentName'][0]}")
    print(f"  M2 Marker: {m2_response_data['Your Name'][0]}")
    print(f"  Agreement: {m2_response_data['Do you agree with M1\'s assessment?'][0]}")
    print(f"  Comments: {m2_response_data['Additional Comments'][0]}")

    return import_path

def create_sample_m2_disagreement():
    """Create a sample M2 disagreement response for escalation demo."""

    # Sample M2 disagreement data
    m2_disagreement_data = {
        # Pre-filled from Forms URL
        'StudentID': ['TEST002'],
        'StudentName': ['Bob Test Student'],
        'M1_MarkerName': ['Dr. Test Marker'],
        'M1_Score': [75],
        'M1_Feedback': ['Good work overall with minor issues.'],
        'M1_PassFail': ['Pass'],

        # M2's disagreement response
        'Your Name': ['Dr. Second Marker'],
        'Your Email': ['second.marker@keele.ac.uk'],
        'Do you agree with M1\'s assessment?': ['No'],  # M2 disagrees
        'If No, what score would you give?': [65],  # Different score
        'If No, what is your feedback?': ['I think the work needs more attention to detail and some concepts are not fully demonstrated.'],
        'Additional Comments': ['Recommend escalation to M3 for final decision.'],

        # System fields
        'Submission_Date': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    }

    # Create DataFrame
    df = pd.DataFrame(m2_disagreement_data)

    # Save to imports folder
    import_path = "data/forms_imports/M2_Disagreement_TEST002.xlsx"
    df.to_excel(import_path, index=False, engine='openpyxl')

    print(f"Created sample M2 disagreement: {import_path}")
    print("M2 Disagreement Details:")
    print(f"  Student: {m2_disagreement_data['StudentName'][0]}")
    print(f"  M1 Score: {m2_disagreement_data['M1_Score'][0]}")
    print(f"  M2 Score: {m2_disagreement_data['If No, what score would you give?'][0]}")
    print(f"  M2 Feedback: {m2_disagreement_data['If No, what is your feedback?'][0]}")

    return import_path

if __name__ == "__main__":
    print("Creating Sample M2 Responses for Folder-Drop Demo")
    print("=" * 60)

    # Create agreement response
    path1 = create_sample_m2_response()

    print("\n" + "-" * 40)

    # Create disagreement response
    path2 = create_sample_m2_disagreement()

    print("\n" + "=" * 60)
    print("Demo Setup Complete!")
    print("\nWhat Will Happen:")
    print("1. Background monitoring will detect these files within 10 seconds")
    print("2. Excel will be automatically updated with M2 responses")
    print("3. Workflow status will change automatically")
    print("4. Dashboard will show real-time updates")

    print("\nWatch for processing in your Streamlit app!")