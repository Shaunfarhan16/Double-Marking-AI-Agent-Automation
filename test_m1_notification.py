#!/usr/bin/env python3
"""
Test script for the new M1 disagreement notification functionality.
"""

import os
import sys
import logging
from typing import Dict, Any

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.automated_email_system import AutomatedEmailSystem
from agents.workflow_coordinator import WorkflowCoordinator
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_m1_disagreement_notification():
    """Test the new M1 disagreement notification functionality."""
    logger.info("Testing M1 disagreement notification...")
    
    try:
        # Initialize automated email system
        email_system = AutomatedEmailSystem()
        
        # Test data for M1 and M2
        test_m1_data = {
            'marker_name': 'Dr. Alice Smith',
            'marker_email': 'alice.smith@university.edu',
            'score': 85,
            'passfail': 'Pass',
            'feedback': 'Excellent work on the algorithm implementation. Clear code structure and good documentation.'
        }
        
        test_m2_data = {
            'marker_name': 'Dr. Bob Jones', 
            'marker_email': 'bob.jones@university.edu',
            'score': 65,
            'passfail': 'Pass',
            'feedback': 'Good implementation but lacks error handling and some edge cases are not covered.',
            'agreed': False
        }
        
        # Test the M1 disagreement notification
        result = email_system.send_m1_disagreement_notification(
            student_id="CS2024001",
            m1_data=test_m1_data,
            m2_data=test_m2_data
        )
        
        if "Error" not in result:
            print("✅ PASS - M1 disagreement notification created successfully")
            print(f"   Result: {result}")
            print("   📧 Email should now be displayed in Outlook for review")
            return True
        else:
            print("❌ FAIL - M1 disagreement notification failed")
            print(f"   Error: {result}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR - Exception in M1 notification test: {str(e)}")
        return False

def test_full_disagreement_workflow():
    """Test the complete disagreement workflow including M1 notification."""
    logger.info("Testing full disagreement workflow...")
    
    try:
        # Create test forms data with disagreement scenario
        test_data = pd.DataFrame([
            {
                'StudentID': 'TEST001',
                'StudentName': 'Test Student',
                'MarkerRole': 'M1',
                'MarkerName': 'Dr. Alice Smith',
                'MarkerEmail': 'alice.smith@university.edu',
                'Score': 85,
                'PassFail': 'Pass',
                'Feedback': 'Excellent work',
                'AI_Feedback_Optional': '',
                'M2_Agree_Checkbox': False
            },
            {
                'StudentID': 'TEST001',
                'StudentName': 'Test Student', 
                'MarkerRole': 'M2',
                'MarkerName': 'Dr. Bob Jones',
                'MarkerEmail': 'bob.jones@university.edu',
                'Score': 65,  # Different score = disagreement
                'PassFail': 'Pass',
                'Feedback': 'Good but needs improvement',
                'AI_Feedback_Optional': '',
                'M2_Agree_Checkbox': False  # Explicit disagreement
            }
        ])
        
        # Initialize workflow coordinator
        coordinator = WorkflowCoordinator()
        
        # Process the disagreement
        result = coordinator.process_action(
            student_id="TEST001",
            action="Process Agreement", 
            forms_data=test_data
        )
        
        if "Error" not in result and "disagreement" in result.lower():
            print("✅ PASS - Full disagreement workflow executed successfully")
            print(f"   Result: {result}")
            print("   📧 Both M1 disagreement and M3 escalation emails should be displayed")
            return True
        else:
            print("❌ FAIL - Full disagreement workflow failed")
            print(f"   Result: {result}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR - Exception in workflow test: {str(e)}")
        return False

def test_outlook_connection():
    """Test basic Outlook connection."""
    logger.info("Testing Outlook connection...")
    
    try:
        outlook = OutlookAutomation()
        result = outlook.test_connection()
        
        if result['status'] == 'success':
            print("✅ PASS - Outlook connection successful")
            print(f"   Details: {result['message']}")
            return True
        else:
            print("❌ FAIL - Outlook connection failed")
            print(f"   Error: {result['message']}")
            if 'suggestion' in result:
                print(f"   Suggestion: {result['suggestion']}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR - Exception in Outlook test: {str(e)}")
        return False

def run_m1_notification_test_suite():
    """Run complete test suite for M1 notification functionality."""
    print("=" * 70)
    print("M1 Disagreement Notification Test Suite")
    print("=" * 70)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Outlook Connection
    print("\n1. Testing Outlook Connection...")
    if test_outlook_connection():
        tests_passed += 1
    
    # Test 2: M1 Disagreement Notification
    print("\n2. Testing M1 Disagreement Notification...")
    if test_m1_disagreement_notification():
        tests_passed += 1
    
    # Test 3: Full Disagreement Workflow
    print("\n3. Testing Full Disagreement Workflow...")
    if test_full_disagreement_workflow():
        tests_passed += 1
    
    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Tests Passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED - M1 disagreement notification is working!")
    else:
        print("⚠️  SOME TESTS FAILED - Check the errors above")
    
    print("\nExpected Behavior:")
    print("1. When M2 disagrees with M1:")
    print("   → M1 receives disagreement notification email")
    print("   → M3 receives escalation email with both assessments")
    print("2. When M2 agrees with M1:")
    print("   → Both M1 and M2 receive finalization email")
    print("3. Email flow sequence:")
    print("   M1 submits → M2 gets notification → M2 disagrees → M1 gets disagreement notice + M3 gets escalation")

if __name__ == "__main__":
    run_m1_notification_test_suite()