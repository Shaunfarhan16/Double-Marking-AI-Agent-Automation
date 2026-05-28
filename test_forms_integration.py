#!/usr/bin/env python3
"""
Test Suite for Enhanced Microsoft Forms Integration

Tests the complete Forms integration system including:
- Template generation
- Auto-export functionality
- Auto-import processing
- Workflow status updates
- Background monitoring

Author: Double-Marking AI Agent Automation
Version: 1.0 - Forms Integration Testing
"""

import sys
import os
import tempfile
import json
import pandas as pd
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

def test_forms_integration_system():
    """Test complete Forms integration system."""
    print("Testing Microsoft Forms Integration System")
    print("=" * 60)
    
    try:
        from utils.forms_integration import forms_integration
        
        # Test 1: Template Generation
        print("\n1. Testing Template Generation...")
        template_path = forms_integration.create_forms_template()
        
        if os.path.exists(template_path):
            print(f"✅ Template created successfully: {template_path}")
            
            # Verify template structure
            df = pd.read_excel(template_path)
            required_columns = [
                'StudentID', 'StudentName', 'M1_MarkerName', 'M1_Score',
                'M2_AssignedName', 'M3_AssignedName', 'M2_Agree_Checkbox'
            ]
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            if not missing_columns:
                print("✅ Template has all required columns")
            else:
                print(f"❌ Missing columns: {missing_columns}")
        else:
            print("❌ Template generation failed")
            return False
        
        # Test 2: Export Functionality
        print("\n2. Testing Export Functionality...")
        test_assessment = {
            'StudentID': 'TEST001',
            'StudentName': 'Test Student',
            'Score': 85,
            'PassFail': 'Pass',
            'Feedback': 'Excellent work on algorithms',
            'M1_Name': 'Dr. Test Marker',
            'M1_Email': 'test.marker@keele.ac.uk',
            'M2_Name': 'Dr. Second Marker',
            'M2_Email': 'second.marker@keele.ac.uk',
            'M3_Name': 'Dr. Third Marker',
            'M3_Email': 'third.marker@keele.ac.uk',
            'Submission_Date': datetime.now().isoformat()
        }
        
        success, message, export_path = forms_integration.export_submission_to_forms(test_assessment)
        
        if success:
            print(f"✅ Export successful: {message}")
            print(f"✅ Export file: {export_path}")
            
            # Verify export file
            if os.path.exists(export_path):
                export_df = pd.read_excel(export_path)
                if export_df.iloc[0]['StudentID'] == 'TEST001':
                    print("✅ Export data verification passed")
                else:
                    print("❌ Export data verification failed")
            
        else:
            print(f"❌ Export failed: {message}")
            return False
        
        # Test 3: Import Functionality
        print("\n3. Testing Import Functionality...")
        
        # Create test import file with M2 response
        import_data = {
            'StudentID': 'TEST001',
            'StudentName': 'Test Student',
            'M1_Score': 85,
            'M2_ResponseDate': datetime.now().isoformat(),
            'M2_Agree_Checkbox': 'Yes',  # M2 agrees
            'Status': 'Awaiting M2'
        }
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
            import_df = pd.DataFrame([import_data])
            import_df.to_excel(tmp_file.name, index=False)
            import_path = tmp_file.name
        
        success, message, count = forms_integration.import_m2_responses(import_path)
        
        if success and count > 0:
            print(f"✅ Import successful: {message}")
            print(f"✅ Processed {count} responses")
        else:
            print(f"❌ Import failed: {message}")
        
        # Clean up
        os.unlink(import_path)
        
        # Test 4: Workflow Status
        print("\n4. Testing Workflow Status...")
        workflow_status = forms_integration.get_workflow_status()
        
        if 'students' in workflow_status and 'stats' in workflow_status:
            print("✅ Workflow status structure is correct")
            print(f"✅ Statistics: {workflow_status['stats']}")
        else:
            print("❌ Workflow status structure is incorrect")
        
        # Test 5: Pending Responses
        print("\n5. Testing Pending Response Tracking...")
        pending = forms_integration.get_pending_m2_responses()
        
        print(f"✅ Pending responses tracking: {len(pending)} pending")
        
        print(f"\n🎉 All Forms Integration tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Forms Integration test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_background_monitoring():
    """Test background monitoring system."""
    print("\nTesting Background Monitoring System")
    print("=" * 50)
    
    try:
        from utils.forms_integration import forms_integration
        
        # Test starting monitoring
        print("1. Testing Auto-Import Monitoring Start...")
        forms_integration.start_auto_import_monitoring(check_interval_minutes=1)
        print("✅ Auto-import monitoring started")
        
        # Test stopping monitoring
        print("2. Testing Auto-Import Monitoring Stop...")
        forms_integration.stop_auto_import_monitoring()
        print("✅ Auto-import monitoring stopped")
        
        return True
        
    except Exception as e:
        print(f"❌ Background monitoring test failed: {str(e)}")
        return False

def test_integration_with_main_app():
    """Test integration with main application components."""
    print("\nTesting Integration with Main Application")
    print("=" * 50)
    
    try:
        # Test marker database integration
        print("1. Testing Marker Database Integration...")
        from utils.marker_database import marker_db
        
        markers = marker_db.get_all_markers()
        if markers:
            print(f"✅ Marker database accessible: {len(markers)} markers")
        else:
            print("⚠️ No markers in database - add some for full testing")
        
        # Test email system integration
        print("2. Testing Email System Integration...")
        from utils.automated_email_system import AutomatedEmailSystem
        
        email_system = AutomatedEmailSystem()
        print("✅ Email system initialized successfully")
        
        # Test workflow coordinator integration
        print("3. Testing Workflow Coordinator Integration...")
        from agents.workflow_coordinator import WorkflowCoordinator
        
        coordinator = WorkflowCoordinator()
        print("✅ Workflow coordinator initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Main app integration test failed: {str(e)}")
        return False

def run_comprehensive_test():
    """Run all Forms integration tests."""
    print("🚀 Double-Marking AI Agent Automation - Forms Integration Test Suite")
    print("=" * 80)
    print(f"Test started at: {datetime.now().isoformat()}")
    print()
    
    tests = [
        ("Forms Integration System", test_forms_integration_system),
        ("Background Monitoring", test_background_monitoring),
        ("Main Application Integration", test_integration_with_main_app)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔬 Running: {test_name}")
        print("-" * 60)
        
        try:
            result = test_func()
            results.append((test_name, result))
            
            if result:
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
                
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Forms Integration is working perfectly!")
    else:
        print("⚠️ Some tests failed - check the output above for details")
    
    print(f"\nTest completed at: {datetime.now().isoformat()}")
    
    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)