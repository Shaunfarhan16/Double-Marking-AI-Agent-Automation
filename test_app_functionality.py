#!/usr/bin/env python3
"""
Quick Functionality Test for Enhanced Double-Marking AI Agent
Tests all core components without running the full Streamlit app
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

def test_marker_database():
    """Test marker database functionality"""
    print("Testing Marker Database...")
    try:
        from utils.marker_database import marker_db
        
        # Test get all markers
        markers = marker_db.get_all_markers()
        print(f"SUCCESS: Loaded {len(markers)} markers")
        
        # Test statistics
        stats = marker_db.get_marker_statistics()
        print(f"SUCCESS: Statistics: {stats}")
        
        # Test dropdown options
        options = marker_db.get_markers_for_dropdown(include_demo=True)
        print(f"SUCCESS: Dropdown options: {len(options)} available")
        
        return True
    except Exception as e:
        print(f"ERROR: Marker Database Error: {e}")
        return False

def test_email_system():
    """Test automated email system"""
    print("\nTesting Email System...")
    try:
        from utils.automated_email_system import AutomatedEmailSystem
        
        email_system = AutomatedEmailSystem()
        print("SUCCESS: Email system initialized successfully")
        print(f"SUCCESS: Agent email configured: {email_system.agent_email}")
        
        return True
    except Exception as e:
        print(f"ERROR: Email System Error: {e}")
        return False

def test_workflow_coordinator():
    """Test workflow coordinator"""
    print("\nTesting Workflow Coordinator...")
    try:
        from agents.workflow_coordinator import WorkflowCoordinator
        
        coordinator = WorkflowCoordinator()
        print("SUCCESS: Workflow coordinator initialized successfully")
        
        return True
    except Exception as e:
        print(f"ERROR: Workflow Coordinator Error: {e}")
        return False

def test_forms_parser():
    """Test forms parser"""
    print("\nTesting Forms Parser...")
    try:
        from utils.forms_parser import FormsParser
        
        parser = FormsParser()
        print("SUCCESS: Forms parser initialized successfully")
        
        return True
    except Exception as e:
        print(f"ERROR: Forms Parser Error: {e}")
        return False

def test_feedback_generator():
    """Test AI feedback generator systems"""
    print("\nTesting AI Feedback Generator Systems...")
    enhanced_success = False
    standard_success = False

    # Test Enhanced Feedback Generator
    try:
        from rag.enhanced_feedback_generator import enhanced_feedback_generator

        print("SUCCESS: Enhanced feedback generator imported successfully")
        print(f"SUCCESS: Claude client available: {enhanced_feedback_generator.claude_client is not None}")
        enhanced_success = True

    except Exception as e:
        print(f"ERROR: Enhanced Feedback Generator Error: {e}")

    # Test Standard Feedback Generator (fallback)
    try:
        from rag.feedback_generator import FeedbackGenerator

        generator = FeedbackGenerator()
        print("SUCCESS: Standard feedback generator initialized successfully")
        print(f"SUCCESS: RAG system available: {generator.rag_system is not None}")
        standard_success = True

    except Exception as e:
        print(f"ERROR: Standard Feedback Generator Error: {e}")

    # At least one should work
    if enhanced_success:
        print("SUCCESS: Enhanced AI feedback system operational")
        return True
    elif standard_success:
        print("SUCCESS: Standard AI feedback system operational (fallback)")
        return True
    else:
        print("ERROR: No AI feedback system available")
        return False

def test_forms_integration():
    """Test Microsoft Forms integration"""
    print("\nTesting Microsoft Forms Integration...")
    try:
        from utils.forms_integration import forms_integration
        
        print("SUCCESS: Forms integration system initialized successfully")
        
        # Test workflow status
        status = forms_integration.get_workflow_status()
        print(f"SUCCESS: Workflow status available: {len(status)} keys")
        
        # Test pending responses
        pending = forms_integration.get_pending_m2_responses()
        print(f"SUCCESS: Pending responses tracking: {len(pending)} items")
        
        return True
    except Exception as e:
        print(f"ERROR: Forms Integration Error: {e}")
        return False

def main():
    """Run all functionality tests"""
    print("Double-Marking AI Agent Automation - Functionality Test\n")
    
    tests = [
        test_marker_database,
        test_email_system, 
        test_workflow_coordinator,
        test_forms_parser,
        test_feedback_generator,
        test_forms_integration
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print(f"\nTest Results:")
    print(f"PASSED: {sum(results)}/{len(results)}")
    print(f"FAILED: {len(results) - sum(results)}/{len(results)}")
    
    if all(results):
        print("\nAll core functionality tests PASSED!")
        print("The Streamlit app should be fully functional")
    else:
        print("\nSome tests failed - check the errors above")
    
    return all(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)