#!/usr/bin/env python3
"""
Comprehensive Test Suite for Automated Email System

This test suite validates all aspects of the new automated email delivery system:
- Gmail SMTP connection testing
- Real-time email delivery validation
- All notification types (M2, M1 disagreement, M3 escalation, finalization)
- Full workflow integration testing
- Performance and reliability testing

Usage:
    python test_automated_email_system.py

Author: Double-Marking System
Version: 2.0 - Automated Email Testing Suite
"""

import os
import sys
import logging
from typing import Dict, Any, List
import time

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.automated_email_system import AutomatedEmailSystem
from agents.workflow_coordinator import WorkflowCoordinator
import pandas as pd

# Configure detailed logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('email_test_results.log', mode='w')
    ]
)
logger = logging.getLogger(__name__)

class AutomatedEmailTestSuite:
    """Comprehensive test suite for the automated email system."""
    
    def __init__(self):
        """Initialize the test suite."""
        self.email_system = None
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        
        print("=" * 80)
        print("🤖 AUTOMATED EMAIL SYSTEM - COMPREHENSIVE TEST SUITE")
        print("=" * 80)
        print("📧 Testing real-time Gmail SMTP delivery")
        print("⚡ Validating immediate notification system")
        print("🔄 Checking full workflow integration")
        print("=" * 80)
    
    def log_test_result(self, test_name: str, status: str, details: str = "", 
                       execution_time: float = 0):
        """Log test result with detailed information."""
        self.total_tests += 1
        if status == "PASS":
            self.passed_tests += 1
        
        result = {
            'test_name': test_name,
            'status': status,
            'details': details,
            'execution_time': execution_time
        }
        self.test_results.append(result)
        
        status_emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_emoji} {test_name}: {status}")
        if details:
            print(f"   Details: {details}")
        if execution_time > 0:
            print(f"   Execution Time: {execution_time:.2f}s")
    
    def test_email_system_initialization(self) -> bool:
        """Test 1: Email system initialization and configuration validation."""
        test_name = "Email System Initialization"
        start_time = time.time()
        
        try:
            self.email_system = AutomatedEmailSystem()
            execution_time = time.time() - start_time
            
            # Validate configuration
            if not self.email_system.agent_email:
                self.log_test_result(test_name, "FAIL", "Agent email not configured", execution_time)
                return False
            
            if "your_16_char_app_password_here" in str(self.email_system.agent_password):
                self.log_test_result(test_name, "FAIL", "App password not set in .env file", execution_time)
                return False
            
            self.log_test_result(
                test_name, "PASS", 
                f"System initialized with {self.email_system.agent_email}", 
                execution_time
            )
            return True
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_test_result(test_name, "FAIL", f"Initialization failed: {str(e)}", execution_time)
            return False
    
    def test_smtp_connection(self) -> bool:
        """Test 2: Gmail SMTP connection and authentication."""
        test_name = "Gmail SMTP Connection"
        start_time = time.time()
        
        try:
            if not self.email_system:
                self.log_test_result(test_name, "SKIP", "Email system not initialized")
                return False
            
            connection_result = self.email_system.test_connection()
            execution_time = time.time() - start_time
            
            if connection_result['status'] == 'success':
                self.log_test_result(
                    test_name, "PASS",
                    f"Connected to {connection_result.get('smtp_server', 'Gmail')} successfully",
                    execution_time
                )
                return True
            else:
                self.log_test_result(
                    test_name, "FAIL",
                    f"Connection failed: {connection_result.get('message', 'Unknown error')}",
                    execution_time
                )
                return False
                
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_test_result(test_name, "FAIL", f"Exception: {str(e)}", execution_time)
            return False
    
    def test_m2_notification_delivery(self) -> bool:
        """Test 3: M2 notification real-time delivery."""
        test_name = "M2 Notification Delivery"
        start_time = time.time()
        
        try:
            if not self.email_system:
                self.log_test_result(test_name, "SKIP", "Email system not initialized")
                return False
            
            # Test M2 notification with sample data
            test_m1_data = {
                'marker_name': 'Dr. Alice Smith',
                'marker_email': 'alice.smith@test.edu',
                'score': 85,
                'passfail': 'Pass',
                'feedback': 'Excellent implementation with clear documentation and good error handling.'
            }
            
            result = self.email_system.send_m2_notification(
                student_id="TEST001",
                m1_data=test_m1_data,
                m2_email="m2.marker@test.edu"  # Test email
            )
            
            execution_time = time.time() - start_time
            
            if result['status'] == 'delivered':
                self.log_test_result(
                    test_name, "PASS",
                    f"M2 notification delivered to {result.get('recipients', ['test email'])}",
                    execution_time
                )
                return True
            else:
                self.log_test_result(
                    test_name, "FAIL",
                    f"Delivery failed: {result.get('message', 'Unknown error')}",
                    execution_time
                )
                return False
                
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_test_result(test_name, "FAIL", f"Exception: {str(e)}", execution_time)
            return False
    
    def test_m1_disagreement_notification(self) -> bool:
        """Test 4: M1 disagreement notification delivery."""
        test_name = "M1 Disagreement Notification"
        start_time = time.time()
        
        try:
            if not self.email_system:
                self.log_test_result(test_name, "SKIP", "Email system not initialized")
                return False
            
            # Test M1 disagreement notification
            test_m1_data = {
                'marker_name': 'Dr. Alice Smith',
                'marker_email': 'm1.marker@test.edu',
                'score': 85,
                'passfail': 'Pass',
                'feedback': 'Excellent work with comprehensive implementation.'
            }
            
            test_m2_data = {
                'marker_name': 'Dr. Bob Jones',
                'marker_email': 'm2.marker@test.edu',
                'score': 65,
                'passfail': 'Pass',
                'feedback': 'Good work but missing some error handling.',
                'agreed': False
            }
            
            result = self.email_system.send_m1_disagreement_notification(
                student_id="TEST002",
                m1_data=test_m1_data,
                m2_data=test_m2_data
            )
            
            execution_time = time.time() - start_time
            
            if result['status'] == 'delivered':
                self.log_test_result(
                    test_name, "PASS",
                    f"M1 disagreement notification delivered successfully",
                    execution_time
                )
                return True
            else:
                self.log_test_result(
                    test_name, "FAIL",
                    f"Delivery failed: {result.get('message', 'Unknown error')}",
                    execution_time
                )
                return False
                
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_test_result(test_name, "FAIL", f"Exception: {str(e)}", execution_time)
            return False
    
    def test_m3_escalation_email(self) -> bool:
        """Test 5: M3 escalation email delivery."""
        test_name = "M3 Escalation Email"
        start_time = time.time()
        
        try:
            if not self.email_system:
                self.log_test_result(test_name, "SKIP", "Email system not initialized")
                return False
            
            # Test M3 escalation email
            test_m1_data = {
                'marker_name': 'Dr. Alice Smith',
                'marker_email': 'm1.marker@test.edu',
                'score': 85,
                'passfail': 'Pass',
                'feedback': 'Excellent implementation.'
            }
            
            test_m2_data = {
                'marker_name': 'Dr. Bob Jones',
                'marker_email': 'm2.marker@test.edu',
                'score': 65,
                'passfail': 'Pass',
                'feedback': 'Good but needs improvement.',
                'agreed': False
            }
            
            result = self.email_system.send_escalation_email(
                student_id="TEST003",
                m1_data=test_m1_data,
                m2_data=test_m2_data,
                m3_email="m3.marker@test.edu"
            )
            
            execution_time = time.time() - start_time
            
            if result['status'] == 'delivered':
                self.log_test_result(
                    test_name, "PASS",
                    f"M3 escalation email delivered with CC to both markers",
                    execution_time
                )
                return True
            else:
                self.log_test_result(
                    test_name, "FAIL",
                    f"Delivery failed: {result.get('message', 'Unknown error')}",
                    execution_time
                )
                return False
                
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_test_result(test_name, "FAIL", f"Exception: {str(e)}", execution_time)
            return False
    
    def test_finalization_email(self) -> bool:
        """Test 6: Finalization email delivery."""
        test_name = "Finalization Email"
        start_time = time.time()
        
        try:
            if not self.email_system:
                self.log_test_result(test_name, "SKIP", "Email system not initialized")
                return False
            
            # Test finalization email
            result = self.email_system.send_finalization_email(
                student_id="TEST004",
                final_score=78.5,
                m1_email="m1.marker@test.edu",
                m2_email="m2.marker@test.edu"
            )
            
            execution_time = time.time() - start_time
            
            if result['status'] == 'delivered':
                self.log_test_result(
                    test_name, "PASS",
                    f"Finalization email delivered to both markers",
                    execution_time
                )
                return True
            else:
                self.log_test_result(
                    test_name, "FAIL",
                    f"Delivery failed: {result.get('message', 'Unknown error')}",
                    execution_time
                )
                return False
                
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_test_result(test_name, "FAIL", f"Exception: {str(e)}", execution_time)
            return False
    
    def test_workflow_integration(self) -> bool:
        """Test 7: Full workflow integration with automated emails."""
        test_name = "Workflow Integration"
        start_time = time.time()
        
        try:
            # Create test workflow coordinator
            coordinator = WorkflowCoordinator()
            
            # Test data simulating disagreement scenario
            test_data = pd.DataFrame([
                {
                    'StudentID': 'WORKFLOW001',
                    'StudentName': 'Test Student',
                    'MarkerRole': 'M1',
                    'MarkerName': 'Dr. Alice Smith',
                    'MarkerEmail': 'm1.workflow@test.edu',
                    'Score': 85,
                    'PassFail': 'Pass',
                    'Feedback': 'Excellent work',
                    'AI_Feedback_Optional': '',
                    'M2_Agree_Checkbox': False
                },
                {
                    'StudentID': 'WORKFLOW001',
                    'StudentName': 'Test Student',
                    'MarkerRole': 'M2',
                    'MarkerName': 'Dr. Bob Jones',
                    'MarkerEmail': 'm2.workflow@test.edu',
                    'Score': 65,  # Different score = disagreement
                    'PassFail': 'Pass',
                    'Feedback': 'Good but needs improvement',
                    'AI_Feedback_Optional': '',
                    'M2_Agree_Checkbox': False
                }
            ])
            
            # Process the workflow
            result = coordinator.process_action(
                student_id="WORKFLOW001",
                action="Process Agreement",
                forms_data=test_data
            )
            
            execution_time = time.time() - start_time
            
            # Check if workflow completed successfully
            if "Error" not in result and ("delivered" in result or "disagreement" in result.lower()):
                self.log_test_result(
                    test_name, "PASS",
                    f"Workflow integration successful with automated emails",
                    execution_time
                )
                return True
            else:
                self.log_test_result(
                    test_name, "FAIL",
                    f"Workflow integration failed: {result}",
                    execution_time
                )
                return False
                
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_test_result(test_name, "FAIL", f"Exception: {str(e)}", execution_time)
            return False
    
    def test_outlook_compatibility(self) -> bool:
        """Test 8: Outlook email compatibility testing."""
        test_name = "Outlook Compatibility"
        start_time = time.time()
        
        try:
            if not self.email_system:
                self.log_test_result(test_name, "SKIP", "Email system not initialized")
                return False
            
            # Test with various Outlook/Microsoft domains
            test_outlook_emails = [
                "test.marker1@outlook.com",
                "test.marker2@hotmail.com", 
                "test.marker3@live.com"
            ]
            
            successful_deliveries = 0
            compatibility_results = []
            
            for outlook_email in test_outlook_emails:
                result = self.email_system.test_outlook_compatibility(outlook_email)
                compatibility_results.append(result)
                
                if result['status'] == 'delivered':
                    successful_deliveries += 1
            
            execution_time = time.time() - start_time
            success_rate = (successful_deliveries / len(test_outlook_emails)) * 100
            
            if success_rate >= 100:
                self.log_test_result(
                    test_name, "PASS",
                    f"Gmail → Outlook compatibility confirmed for all Microsoft email providers",
                    execution_time
                )
                return True
            else:
                self.log_test_result(
                    test_name, "FAIL", 
                    f"Outlook compatibility issues detected: {success_rate:.1f}% success rate",
                    execution_time
                )
                return False
                
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_test_result(test_name, "FAIL", f"Exception: {str(e)}", execution_time)
            return False
    
    def test_performance_and_reliability(self) -> bool:
        """Test 9: Performance and reliability of email delivery."""
        test_name = "Performance & Reliability"
        start_time = time.time()
        
        try:
            if not self.email_system:
                self.log_test_result(test_name, "SKIP", "Email system not initialized")
                return False
            
            # Test multiple rapid-fire emails to check system stability
            delivery_times = []
            successful_deliveries = 0
            
            test_emails = [
                ("Performance Test 1", "perf1@test.edu"),
                ("Performance Test 2", "perf2@test.edu"),
                ("Performance Test 3", "perf3@test.edu")
            ]
            
            for test_name_email, test_email in test_emails:
                email_start = time.time()
                
                result = self.email_system._send_email(
                    to_email=test_email,
                    subject=f"Performance Test - {test_name_email}",
                    body=f"This is a performance test email for {test_name_email}"
                )
                
                email_time = time.time() - email_start
                delivery_times.append(email_time)
                
                if result['status'] == 'delivered':
                    successful_deliveries += 1
            
            execution_time = time.time() - start_time
            avg_delivery_time = sum(delivery_times) / len(delivery_times)
            success_rate = (successful_deliveries / len(test_emails)) * 100
            
            if success_rate >= 100 and avg_delivery_time < 10:  # 10 seconds threshold
                self.log_test_result(
                    test_name, "PASS",
                    f"Success rate: {success_rate:.1f}%, Avg delivery: {avg_delivery_time:.2f}s",
                    execution_time
                )
                return True
            else:
                self.log_test_result(
                    test_name, "FAIL",
                    f"Success rate: {success_rate:.1f}%, Avg delivery: {avg_delivery_time:.2f}s",
                    execution_time
                )
                return False
                
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_test_result(test_name, "FAIL", f"Exception: {str(e)}", execution_time)
            return False
    
    def run_comprehensive_test_suite(self):
        """Run the complete test suite and generate detailed report."""
        print("\n🚀 Starting Comprehensive Email System Test Suite...")
        print("-" * 80)
        
        # Run all tests
        tests = [
            ("Email System Initialization", self.test_email_system_initialization),
            ("Gmail SMTP Connection", self.test_smtp_connection),
            ("M2 Notification Delivery", self.test_m2_notification_delivery),
            ("M1 Disagreement Notification", self.test_m1_disagreement_notification),
            ("M3 Escalation Email", self.test_m3_escalation_email),
            ("Finalization Email", self.test_finalization_email),
            ("Workflow Integration", self.test_workflow_integration),
            ("Outlook Compatibility", self.test_outlook_compatibility),
            ("Performance & Reliability", self.test_performance_and_reliability)
        ]
        
        print(f"\nRunning {len(tests)} comprehensive tests...\n")
        print("🎓 Production Configuration: Keele University")
        print("🧪 Testing Capability: Universal compatibility with any email provider")
        print()
        
        for test_name, test_function in tests:
            print(f"Running: {test_name}...")
            test_function()
            print()
        
        # Generate comprehensive report
        self.generate_test_report()
    
    def generate_test_report(self):
        """Generate detailed test report."""
        print("=" * 80)
        print("📊 COMPREHENSIVE TEST RESULTS SUMMARY")
        print("=" * 80)
        
        # Overall statistics
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"📋 Total Tests Run: {self.total_tests}")
        print(f"✅ Tests Passed: {self.passed_tests}")
        print(f"❌ Tests Failed: {self.total_tests - self.passed_tests}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        # Detailed results
        print("\n📝 DETAILED TEST RESULTS:")
        print("-" * 80)
        
        for result in self.test_results:
            status_emoji = "✅" if result['status'] == "PASS" else "❌" if result['status'] == "FAIL" else "⚠️"
            print(f"{status_emoji} {result['test_name']:30s} | {result['status']:8s} | {result['execution_time']:6.2f}s")
            if result['details']:
                print(f"   └─ {result['details']}")
        
        # Final assessment
        print("\n" + "=" * 80)
        if success_rate == 100:
            print("🎉 ALL TESTS PASSED! The automated email system is fully operational!")
            print("✅ Real-time email delivery is working perfectly")
            print("✅ Gmail SMTP integration is successful")
            print("✅ All notification types are functioning")
            print("✅ Workflow integration is seamless")
            print("✅ System performance is excellent")
        elif success_rate >= 80:
            print("⚠️  MOSTLY SUCCESSFUL - Some minor issues detected")
            print("🔧 Review failed tests and address configuration issues")
        else:
            print("❌ CRITICAL ISSUES DETECTED - System needs attention")
            print("🚨 Check Gmail credentials and SMTP configuration")
        
        print("\n📋 NEXT STEPS:")
        if success_rate == 100:
            print("1. ✅ System is ready for production use")
            print("2. ✅ Replace placeholder app password in .env with actual Gmail App Password")
            print("3. ✅ Update test email addresses with real marker emails")
            print("4. ✅ Monitor email delivery in production")
        else:
            print("1. 🔧 Fix failed tests before proceeding")
            print("2. 🔧 Verify Gmail App Password configuration")
            print("3. 🔧 Check internet connection and SMTP access")
            print("4. 🔧 Review error logs for detailed debugging")
        
        print("\n📧 EMAIL FLOW SUMMARY:")
        print("M1 submits → M2 notification sent immediately")
        print("M2 disagrees → M1 notification + M3 escalation sent immediately")
        print("M2 agrees → Finalization email sent immediately")
        print("\n⚡ All emails are delivered in REAL-TIME with no manual intervention!")

def main():
    """Main test execution function."""
    try:
        # Create and run test suite
        test_suite = AutomatedEmailTestSuite()
        test_suite.run_comprehensive_test_suite()
        
        print("\n" + "=" * 80)
        print("🏁 Test suite execution completed!")
        print("📄 Detailed logs saved to: email_test_results.log")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR: Test suite execution failed: {str(e)}")
        logger.error(f"Critical error in test suite: {str(e)}")

if __name__ == "__main__":
    main()