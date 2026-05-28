#!/usr/bin/env python3
"""
Test Script for Enhanced Excel Manager
Tests the NO-API enhanced Excel functionality
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from utils.enhanced_excel_manager import enhanced_excel_manager
from datetime import datetime
import pandas as pd

def test_excel_creation():
    """Test creating master Excel file."""
    print("Testing Excel creation...")

    result = enhanced_excel_manager.create_empty_master_excel()
    print(f"Master Excel created: {result}")

def test_m1_assessment():
    """Test auto-populating M1 assessment."""
    print("\nTesting M1 assessment auto-population...")

    test_assessment = {
        'StudentID': 'TEST001',
        'StudentName': 'Alice Test Student',
        'Score': 85,
        'PassFail': 'Pass',
        'Feedback': 'Excellent work with good understanding of concepts.',
        'AI_Feedback_Optional': 'AI suggests focusing on optimization techniques.',
        'M1_Name': 'Dr. Test Marker',
        'M1_Email': 'test.marker@keele.ac.uk',
        'M2_Name': 'Dr. Second Marker',
        'M2_Email': 'second.marker@keele.ac.uk',
        'M3_Name': 'Dr. Third Marker',
        'M3_Email': 'third.marker@keele.ac.uk'
    }

    success, message = enhanced_excel_manager.auto_populate_m1_assessment(test_assessment)

    if success:
        print(f"SUCCESS: {message}")
    else:
        print(f"ERROR: {message}")

def test_statistics():
    """Test workflow statistics."""
    print("\nTesting workflow statistics...")

    stats = enhanced_excel_manager.get_workflow_statistics()
    print("Current Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

def test_submissions_view():
    """Test submissions viewing."""
    print("\nTesting submissions viewing...")

    df = enhanced_excel_manager.get_all_submissions()
    print(f"Total submissions in Excel: {len(df)}")

    if not df.empty:
        print("Columns in Excel:")
        for col in df.columns:
            print(f"  {col}")

def test_excel_export():
    """Test Excel export for download."""
    print("\nTesting Excel export...")

    success, filename, excel_bytes = enhanced_excel_manager.export_excel_for_download()

    if success:
        print(f"Export successful: {filename}")
        print(f"File size: {len(excel_bytes)} bytes")
    else:
        print(f"Export failed: {filename}")

def test_forms_monitoring():
    """Test Forms monitoring setup."""
    print("\nTesting Forms monitoring...")

    # Test starting monitoring
    result = enhanced_excel_manager.start_forms_monitoring()
    print(f"Start monitoring: {result}")

    # Test stopping monitoring
    import time
    time.sleep(2)  # Let it run for 2 seconds

    result = enhanced_excel_manager.stop_forms_monitoring()
    print(f"Stop monitoring: {result}")

def main():
    """Run all tests."""
    print("Enhanced Excel Manager Test Suite")
    print("=" * 50)

    try:
        test_excel_creation()
        test_m1_assessment()
        test_statistics()
        test_submissions_view()
        test_excel_export()
        test_forms_monitoring()

        print("\n" + "=" * 50)
        print("All tests completed successfully!")
        print("Your enhanced Excel system is ready to use!")

        print("\nNext Steps:")
        print("1. Run the main application: python -m streamlit run app/main.py")
        print("2. Go to Dashboard & Markers")
        print("3. Submit a test assessment")
        print("4. Watch Excel auto-populate!")

    except Exception as e:
        print(f"\nTest failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()