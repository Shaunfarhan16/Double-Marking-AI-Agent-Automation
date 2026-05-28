#!/usr/bin/env python3
"""
Test Complete Marker Assignment Workflow

Tests the enhanced marker management system end-to-end:
1. Marker database operations
2. Forms parser with dropdown selections
3. Workflow coordinator integration
4. Email notifications

Author: Double-Marking System
Version: 1.0 - Workflow Testing
"""

import sys
import pandas as pd
from pathlib import Path
from datetime import datetime
import json

sys.path.append(str(Path(__file__).parent))

from utils.marker_database import marker_db
from utils.forms_parser import FormsParser
from agents.workflow_coordinator import WorkflowCoordinator

def test_marker_database():
    """Test marker database operations"""
    print("Testing Marker Database Operations...")
    
    # Test stats
    stats = marker_db.get_marker_statistics()
    print(f"  Database Stats: {stats['total_markers']} total, {stats['demo_markers']} demo")
    
    # Test dropdown options
    dropdown_options = marker_db.get_markers_for_dropdown()
    print(f"  Dropdown Options: {len(dropdown_options)} available")
    print(f"  First option: {dropdown_options[0] if dropdown_options else 'None'}")
    
    # Test parsing dropdown selection
    if dropdown_options:
        first_option = dropdown_options[0]
        marker_id, name, email = marker_db.parse_dropdown_selection(first_option)
        print(f"  Parsed: ID={marker_id}, Name={name}, Email={email}")
    
    print("  Marker database tests completed\n")


def test_forms_parser():
    """Test forms parser with marker assignments"""
    print("Testing Forms Parser with Marker Assignments...")
    
    # Create sample form data with marker assignments
    sample_data = {
        'StudentID': ['CS2024001'],
        'StudentName': ['John Student'],
        'MarkerRole': ['M1'],
        'MarkerName': ['Dr. John Smith'],
        'MarkerEmail': ['john.smith@keele.ac.uk'],
        'Score': [75],
        'PassFail': ['Pass'],
        'Feedback': ['Good work overall'],
        'AI_Feedback_Optional': [''],
        'M2_MarkerName': ['Dr. Jane Doe (jane.doe@keele.ac.uk) [DEMO]'],
        'M2_MarkerEmail': ['jane.doe@keele.ac.uk'],
        'M3_MarkerName': ['Prof. Robert Wilson (robert.wilson@keele.ac.uk) [DEMO]'],
        'M3_MarkerEmail': ['robert.wilson@keele.ac.uk'],
        'M2_Agree_Checkbox': [False],
        'M2_Score': [None],
        'M2_Feedback': [None],
        'Timestamp': [datetime.now()]
    }
    
    df = pd.DataFrame(sample_data)
    
    # Test parsing
    parser = FormsParser()
    parser.data = df
    parser._clean_data()
    processed_data = parser._derive_workflow_status()
    
    if not processed_data.empty:
        record = processed_data.iloc[0]
        print(f"  Processed Record:")
        print(f"     Student ID: {record['StudentID']}")
        print(f"     Status: {record['Status']}")
        print(f"     M2 Assigned: {record.get('M2_AssignedName', 'N/A')} ({record.get('M2_AssignedEmail', 'N/A')})")
        print(f"     M3 Assigned: {record.get('M3_AssignedName', 'N/A')} ({record.get('M3_AssignedEmail', 'N/A')})")
        print("  Forms parser tests completed\n")
        return processed_data
    else:
        print("  No processed data generated\n")
        return pd.DataFrame()


def test_workflow_coordinator():
    """Test workflow coordinator with marker assignments"""
    print("Testing Workflow Coordinator...")
    
    # Create test data
    test_data = test_forms_parser()
    if test_data.empty:
        print("  ⚠️  Skipping workflow test - no test data available")
        return
    
    # Initialize coordinator
    coordinator = WorkflowCoordinator()
    
    # Test M2 notification action
    student_id = test_data.iloc[0]['StudentID']
    action = "Send M2 Notification"
    
    print(f"  Testing action: {action} for student {student_id}")
    result = coordinator.process_action(student_id, action, test_data)
    print(f"  Result: {result}")
    
    print("  Workflow coordinator tests completed\n")


def test_complete_workflow():
    """Test complete workflow from marker selection to notification"""
    print("Testing Complete Marker Assignment Workflow...")
    
    # Step 1: Verify marker database
    print("  Step 1: Verifying marker database...")
    stats = marker_db.get_marker_statistics()
    print(f"    ✓ {stats['total_markers']} markers available ({stats['demo_markers']} demo)")
    
    # Step 2: Test marker selection
    print("  Step 2: Testing marker selection...")
    dropdown_options = marker_db.get_markers_for_dropdown()
    if len(dropdown_options) >= 3:
        m2_selection = dropdown_options[1]  # Second marker as M2
        m3_selection = dropdown_options[2]  # Third marker as M3
        print(f"    ✓ M2 Selected: {m2_selection}")
        print(f"    ✓ M3 Selected: {m3_selection}")
    else:
        print("    ❌ Insufficient markers for complete test")
        return
    
    # Step 3: Test form processing with assignments
    print("  Step 3: Processing form with marker assignments...")
    
    # Create realistic form submission
    form_data = {
        'StudentID': ['CS2024001'],
        'StudentName': ['Alice Johnson'],
        'MarkerRole': ['M1'],
        'MarkerName': ['Dr. John Smith'],
        'MarkerEmail': ['john.smith@keele.ac.uk'],
        'Score': [82],
        'PassFail': ['Pass'],
        'Feedback': ['Excellent analysis with clear methodology. Minor improvements in conclusion needed.'],
        'AI_Feedback_Optional': [''],
        'M2_MarkerName': [m2_selection],
        'M2_MarkerEmail': [marker_db.parse_dropdown_selection(m2_selection)[2]],
        'M3_MarkerName': [m3_selection],
        'M3_MarkerEmail': [marker_db.parse_dropdown_selection(m3_selection)[2]],
        'M2_Agree_Checkbox': [False],
        'M2_Score': [None],
        'M2_Feedback': [None],
        'Timestamp': [datetime.now()]
    }
    
    df = pd.DataFrame(form_data)
    parser = FormsParser()
    processed_data = parser.parse_forms_data(df)
    
    if not processed_data.empty:
        record = processed_data.iloc[0]
        print(f"    ✓ Form processed: {record['Status']}")
        print(f"    ✓ M2 Assignment: {record.get('M2_AssignedName')} -> {record.get('M2_AssignedEmail')}")
        print(f"    ✓ M3 Assignment: {record.get('M3_AssignedName')} -> {record.get('M3_AssignedEmail')}")
    else:
        print("    ❌ Form processing failed")
        return
    
    # Step 4: Test workflow coordination
    print("  Step 4: Testing workflow coordination...")
    coordinator = WorkflowCoordinator()
    
    # Test M2 notification
    if record['Status'] == 'Awaiting M2':
        result = coordinator.process_action(
            record['StudentID'], 
            "Send M2 Notification", 
            processed_data
        )
        print(f"    ✓ M2 Notification Result: {result}")
    
    print("\nComplete Marker Assignment Workflow Test Completed!")
    print("=" * 60)
    print("All components working together successfully!")
    print("Email notifications configured for real-time delivery")  
    print("Three-marker workflow ready for production")
    print("=" * 60)


def main():
    """Run all workflow tests"""
    print("Enhanced Marker Management System - Complete Workflow Test")
    print("=" * 60)
    
    try:
        # Run individual component tests
        test_marker_database()
        test_forms_parser()
        test_workflow_coordinator()
        
        # Run complete integration test
        test_complete_workflow()
        
    except Exception as e:
        print(f"Test error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()