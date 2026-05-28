#!/usr/bin/env python3
"""
Enhanced Email System with Microsoft Forms Integration
Sends emails with pre-filled Forms links to M2/M3 markers.

Version 6.0 - Critical Bug Fixes & Complete Email System (2024-09-17)
- Added M1 escalation notification system for M2 disagreements
- Complete email workflow: M1 notifications + M3 escalations on disagreement
- Professional email templates with assessment comparisons
- Comprehensive error handling and delivery tracking
"""

import logging
from typing import Dict, Tuple
from urllib.parse import urlencode
from utils.automated_email_system import AutomatedEmailSystem
from utils.forms_template_generator import forms_generator

logger = logging.getLogger(__name__)

class EnhancedEmailSystem:
    """Enhanced email system with Forms integration."""

    def __init__(self):
        try:
            self.base_email_system = AutomatedEmailSystem()
            self.email_available = getattr(self.base_email_system, 'configured', False)
        except Exception as e:
            logger.warning(f"Email system could not be initialized: {e}")
            self.base_email_system = None
            self.email_available = False
        self.forms_url = forms_generator.get_forms_url()

    def build_prefilled_forms_url(self, student_data: Dict) -> str:
        """Build Microsoft Forms URL with pre-filled student data."""

        if not self.forms_url:
            logger.warning("No Forms URL configured")
            return "https://forms.office.com/r/YOUR_FORM_ID"

        # URL parameters for pre-filling (match exact Microsoft Forms question titles)
        params = {
            'Student ID': student_data.get('StudentID', ''),
            'Student Name': student_data.get('StudentName', ''),
            'Assignment Title': 'Computer Science Assessment',
            'M1 Marker Name': student_data.get('M1_Name', ''),
            'M1 Score': str(student_data.get('Score', '')),
            'M1 Pass/Fail': student_data.get('PassFail', ''),
            'M1 Feedback': student_data.get('Feedback', '')[:200]  # Limit for URL
        }

        # Build query string
        query_string = urlencode(params)

        # Combine base URL with parameters
        if '?' in self.forms_url:
            return f"{self.forms_url}&{query_string}"
        else:
            return f"{self.forms_url}?{query_string}"

    def send_m2_notification_with_forms(self, student_data: Dict) -> Dict:
        """Send M2 notification email with Forms link."""

        if not self.email_available or not self.base_email_system:
            forms_link = self.build_prefilled_forms_url(student_data)
            return {
                'status': 'failed',
                'message': 'Email system not configured. Set AGENT_EMAIL and AGENT_APP_PASSWORD in Streamlit secrets.',
                'forms_link': forms_link
            }

        try:
            # Build pre-filled Forms URL
            forms_link = self.build_prefilled_forms_url(student_data)

            # Create email content
            subject = f"Assessment Review Required: {student_data.get('StudentName')} ({student_data.get('StudentID')})"

            body = f"""Dear {student_data.get('M2_Name')},

You have been assigned as the second marker for the following assessment:

📋 STUDENT DETAILS:
• Student: {student_data.get('StudentName')}
• Student ID: {student_data.get('StudentID')}
• Assignment: Computer Science Assessment

📊 M1 ASSESSMENT:
• First Marker: {student_data.get('M1_Name')}
• Score: {student_data.get('Score')}/100
• Pass/Fail: {student_data.get('PassFail')}
• Feedback: {student_data.get('Feedback')}

🎯 YOUR TASK:
Please click the link below to submit your review. The form is pre-filled with student details:

👉 CLICK HERE TO RESPOND:
{forms_link}

⏰ Please complete your review within 3 working days.

INSTRUCTIONS:
• If you agree with M1's assessment, simply select "Yes"
• If you disagree, provide your own score and detailed feedback
• The form will guide you through the process

Thank you,
Double-Marking System
Keele University

---
This is an automated message from the Double-Marking AI Agent System.
If you have any questions, please contact the system administrator.
"""

            # Send email using base system
            result = self.base_email_system._send_email(
                to_email=student_data.get('M2_Email'),
                subject=subject,
                body=body
            )

            # Add Forms link to result
            result['forms_link'] = forms_link

            logger.info(f"M2 notification sent to {student_data.get('M2_Email')} with Forms link")
            return result

        except Exception as e:
            logger.error(f"Error sending M2 notification with Forms: {e}")
            return {
                'status': 'error',
                'message': f'Failed to send M2 notification: {str(e)}',
                'forms_link': ''
            }

    def send_m3_escalation_with_forms(self, student_data: Dict, m2_data: Dict) -> Dict:
        """Send M3 escalation email with Forms link."""

        if not self.email_available or not self.base_email_system:
            forms_link = self.build_prefilled_forms_url(student_data)
            return {
                'status': 'failed',
                'message': 'Email system not configured. Set AGENT_EMAIL and AGENT_APP_PASSWORD in Streamlit secrets.',
                'forms_link': forms_link
            }

        try:
            # Build pre-filled Forms URL (with M1 and M2 data)
            escalation_data = student_data.copy()
            escalation_data.update({
                'M2_Response': f"M2 disagreed - Score: {m2_data.get('score', 'N/A')}, Feedback: {m2_data.get('feedback', 'N/A')}"
            })

            forms_link = self.build_prefilled_forms_url(escalation_data)

            # Create escalation email content
            subject = f"ESCALATION: {student_data.get('StudentName')} ({student_data.get('StudentID')}) - Third Marker Required"

            body = f"""Dear {student_data.get('M3_Name')},

A disagreement between markers requires your attention as the third marker:

📋 STUDENT DETAILS:
• Student: {student_data.get('StudentName')}
• Student ID: {student_data.get('StudentID')}
• Assignment: Computer Science Assessment

📊 MARKING DISAGREEMENT:
• M1 (First Marker): {student_data.get('M1_Name')}
  - Score: {student_data.get('Score')}/100
  - Result: {student_data.get('PassFail')}
  - Feedback: {student_data.get('Feedback')}

• M2 (Second Marker): {m2_data.get('marker_name', 'N/A')}
  - Score: {m2_data.get('score', 'N/A')}/100
  - Feedback: {m2_data.get('feedback', 'N/A')}

🎯 YOUR TASK AS M3:
As the third marker, please make the final determination by clicking the link below:

👉 CLICK HERE FOR FINAL DECISION: {forms_link}

⏰ Please provide your final decision within 2 working days.

INSTRUCTIONS:
• Review both M1 and M2 assessments carefully
• Provide your final score and pass/fail determination
• Your decision will be the final result for this student

Thank you,
Double-Marking System
Keele University

---
This is an automated escalation from the Double-Marking AI Agent System.
Your response is required to complete the assessment process.
"""

            # Send email using base system
            result = self.base_email_system._send_email(
                to_email=student_data.get('M3_Email'),
                subject=subject,
                body=body
            )

            # Add Forms link to result
            result['forms_link'] = forms_link

            logger.info(f"M3 escalation sent to {student_data.get('M3_Email')} with Forms link")
            return result

        except Exception as e:
            logger.error(f"Error sending M3 escalation with Forms: {e}")
            return {
                'status': 'error',
                'message': f'Failed to send M3 escalation: {str(e)}',
                'forms_link': ''
            }

    def send_m1_escalation_notification(self, student_data: Dict, m2_data: Dict) -> Dict:
        """Send M1 escalation notification when M2 disagrees."""

        try:
            # Create M1 escalation email content
            subject = f"ESCALATION NOTICE: {student_data.get('StudentName')} ({student_data.get('StudentID')}) - M2 Disagreement"

            body = f"""Dear {student_data.get('M1_Name')},

This is to inform you that the second marker (M2) has disagreed with your assessment:

📋 STUDENT DETAILS:
• Student: {student_data.get('StudentName')}
• Student ID: {student_data.get('StudentID')}
• Assignment: Computer Science Assessment

📊 ASSESSMENT COMPARISON:
• Your Assessment (M1):
  - Score: {student_data.get('Score')}/100
  - Result: {student_data.get('PassFail')}
  - Feedback: {student_data.get('Feedback')}

• M2 Assessment:
  - Marker: {m2_data.get('marker_name', 'N/A')}
  - Score: {m2_data.get('score', 'N/A')}/100
  - Feedback: {m2_data.get('feedback', 'N/A')}

🎯 NEXT STEPS:
This assessment has been automatically escalated to a third marker (M3) for final decision. You will receive notification of the final outcome once M3 completes their assessment.

⏰ The M3 marker has been notified and will provide the final decision within 2 working days.

ℹ️ No action is required from you at this time. This is purely an informational notice as part of our double-marking quality assurance process.

Thank you for your participation in maintaining assessment standards.

Best regards,
Double-Marking System
Keele University

---
This is an automated escalation notice from the Double-Marking AI Agent System.
"""

            # Send email using base system
            result = self.base_email_system._send_email(
                to_email=student_data.get('M1_Email'),
                subject=subject,
                body=body
            )

            logger.info(f"M1 escalation notification sent to {student_data.get('M1_Email')}")
            return result

        except Exception as e:
            logger.error(f"Error sending M1 escalation notification: {e}")
            return {
                'status': 'error',
                'message': f'Failed to send M1 escalation notification: {str(e)}'
            }

    def test_forms_integration(self, test_email: str) -> Dict:
        """Test Forms integration with a sample email."""

        # Sample student data for testing
        test_data = {
            'StudentID': 'TEST001',
            'StudentName': 'Alice Test Student',
            'Score': 85,
            'PassFail': 'Pass',
            'Feedback': 'Excellent work with good understanding of concepts.',
            'M1_Name': 'Dr. Test Marker',
            'M2_Name': 'Test Recipient',
            'M2_Email': test_email
        }

        # Generate Forms URL
        forms_link = self.build_prefilled_forms_url(test_data)

        # Create test email
        subject = "TEST: Forms Integration - Double-Marking System"

        body = f"""This is a TEST email for Forms integration.

📋 TEST STUDENT: {test_data['StudentName']} ({test_data['StudentID']})

🎯 TEST FORMS LINK:
{forms_link}

✅ If you can see this email and the link works, the integration is successful!

This is a test message from the Double-Marking System.
"""

        # Send test email
        result = self.base_email_system._send_email(
            to_email=test_email,
            subject=subject,
            body=body
        )

        result['forms_link'] = forms_link
        return result

    def send_m3_final_decision_notifications(self, student_data: Dict, m3_data: Dict) -> Dict:
        """Send final decision notifications to M1, M2, and Student when M3 completes assessment."""

        notifications_sent = {
            'M1_notification': {'status': 'not_sent', 'message': ''},
            'M2_notification': {'status': 'not_sent', 'message': ''},
            'student_notification': {'status': 'not_sent', 'message': ''},
            'total_sent': 0,
            'total_failed': 0
        }

        try:
            # Extract M3 final decision data
            final_score = m3_data.get('final_score', 'N/A')
            final_passfail = m3_data.get('final_passfail', 'N/A')
            final_feedback = m3_data.get('final_feedback', 'No additional feedback provided.')
            m3_name = m3_data.get('m3_name', 'Third Marker')

            # 1. Send M1 notification
            try:
                m1_subject = f"M3 Final Decision: {student_data.get('StudentName')} ({student_data.get('StudentID')})"

                m1_body = f"""Dear {student_data.get('M1_Name')},

The third marker has completed the final assessment for the student below:

📋 STUDENT DETAILS:
• Student: {student_data.get('StudentName')}
• Student ID: {student_data.get('StudentID')}
• Assignment: Computer Science Assessment

🎯 M3 FINAL DECISION:
• Third Marker: {m3_name}
• Final Score: {final_score}/100
• Final Result: {final_passfail}
• Final Feedback: {final_feedback}

📊 ASSESSMENT SUMMARY:
• Your Original Assessment (M1): {student_data.get('Score')}/100 - {student_data.get('PassFail')}
• M2 Assessment: Disagreed with your assessment
• M3 Final Decision: {final_score}/100 - {final_passfail}

✅ This assessment is now complete. The M3 decision is final.

Thank you for your participation in the double-marking process.

Best regards,
Double-Marking System
Keele University

---
This is an automated notification from the Double-Marking AI Agent System.
"""

                m1_result = self.base_email_system._send_email(
                    to_email=student_data.get('M1_Email'),
                    subject=m1_subject,
                    body=m1_body
                )

                if m1_result.get('status') == 'delivered':
                    notifications_sent['M1_notification'] = {'status': 'delivered', 'message': 'M1 notified successfully'}
                    notifications_sent['total_sent'] += 1
                else:
                    notifications_sent['M1_notification'] = {'status': 'failed', 'message': m1_result.get('message', 'Unknown error')}
                    notifications_sent['total_failed'] += 1

            except Exception as e:
                notifications_sent['M1_notification'] = {'status': 'error', 'message': f'Error sending M1 notification: {str(e)}'}
                notifications_sent['total_failed'] += 1

            # 2. Send M2 notification
            try:
                m2_subject = f"M3 Final Decision: {student_data.get('StudentName')} ({student_data.get('StudentID')})"

                m2_body = f"""Dear {student_data.get('M2_Name')},

The third marker has resolved the disagreement for the student below:

📋 STUDENT DETAILS:
• Student: {student_data.get('StudentName')}
• Student ID: {student_data.get('StudentID')}
• Assignment: Computer Science Assessment

🎯 M3 FINAL DECISION:
• Third Marker: {m3_name}
• Final Score: {final_score}/100
• Final Result: {final_passfail}
• Final Feedback: {final_feedback}

📊 ASSESSMENT SUMMARY:
• M1 Assessment: {student_data.get('Score')}/100 - {student_data.get('PassFail')}
• Your Assessment (M2): Disagreed with M1
• M3 Final Decision: {final_score}/100 - {final_passfail}

✅ This assessment is now complete. The M3 decision is final.

Thank you for your participation in the double-marking process.

Best regards,
Double-Marking System
Keele University

---
This is an automated notification from the Double-Marking AI Agent System.
"""

                m2_result = self.base_email_system._send_email(
                    to_email=student_data.get('M2_Email'),
                    subject=m2_subject,
                    body=m2_body
                )

                if m2_result.get('status') == 'delivered':
                    notifications_sent['M2_notification'] = {'status': 'delivered', 'message': 'M2 notified successfully'}
                    notifications_sent['total_sent'] += 1
                else:
                    notifications_sent['M2_notification'] = {'status': 'failed', 'message': m2_result.get('message', 'Unknown error')}
                    notifications_sent['total_failed'] += 1

            except Exception as e:
                notifications_sent['M2_notification'] = {'status': 'error', 'message': f'Error sending M2 notification: {str(e)}'}
                notifications_sent['total_failed'] += 1

            # 3. Send Student notification
            try:
                student_subject = f"Assessment Results: {student_data.get('StudentName')} ({student_data.get('StudentID')})"

                student_body = f"""Dear {student_data.get('StudentName')},

Your assessment results are now available:

📋 ASSESSMENT DETAILS:
• Student ID: {student_data.get('StudentID')}
• Assignment: Computer Science Assessment
• Submission Date: {student_data.get('submission_date', 'N/A')}

🎯 FINAL RESULTS:
• Final Score: {final_score}/100
• Final Result: {final_passfail}
• Feedback: {final_feedback}

📊 MARKING PROCESS:
Your assessment went through our double-marking process with three academic markers to ensure fairness and accuracy.

✅ These results are now final and official.

If you have any questions about your results, please contact your course coordinator.

Best regards,
Academic Assessment Team
Keele University

---
This is an automated notification from the Double-Marking Assessment System.
"""

                # Note: Student email would need to be added to student_data
                student_email = student_data.get('StudentEmail')
                if student_email:
                    student_result = self.base_email_system._send_email(
                        to_email=student_email,
                        subject=student_subject,
                        body=student_body
                    )

                    if student_result.get('status') == 'delivered':
                        notifications_sent['student_notification'] = {'status': 'delivered', 'message': 'Student notified successfully'}
                        notifications_sent['total_sent'] += 1
                    else:
                        notifications_sent['student_notification'] = {'status': 'failed', 'message': student_result.get('message', 'Unknown error')}
                        notifications_sent['total_failed'] += 1
                else:
                    notifications_sent['student_notification'] = {'status': 'skipped', 'message': 'Student email not available'}

            except Exception as e:
                notifications_sent['student_notification'] = {'status': 'error', 'message': f'Error sending student notification: {str(e)}'}
                notifications_sent['total_failed'] += 1

            logger.info(f"M3 final decision notifications: {notifications_sent['total_sent']} sent, {notifications_sent['total_failed']} failed")
            return notifications_sent

        except Exception as e:
            logger.error(f"Error sending M3 final decision notifications: {e}")
            return {
                'status': 'error',
                'message': f'Failed to send M3 final decision notifications: {str(e)}',
                'notifications_sent': notifications_sent
            }

    def send_m2_agreement_finalization_emails(self, student_data: Dict) -> Dict:
        """Send finalization emails to M1 and M2 when M2 agrees with M1 assessment."""

        notifications_sent = {
            'M1_notification': {'status': 'not_sent', 'message': ''},
            'M2_notification': {'status': 'not_sent', 'message': ''},
            'total_sent': 0,
            'total_failed': 0
        }

        try:
            final_score = student_data.get('Score', 'N/A')
            final_passfail = student_data.get('PassFail', 'N/A')

            # 1. Send M1 finalization notification
            try:
                m1_subject = f"Assessment Complete: {student_data.get('StudentName')} ({student_data.get('StudentID')})"

                m1_body = f"""Dear {student_data.get('M1_Name')},

The second marker has completed their review and AGREED with your assessment:

📋 STUDENT DETAILS:
• Student: {student_data.get('StudentName')}
• Student ID: {student_data.get('StudentID')}
• Assignment: Computer Science Assessment

🎯 FINAL RESULTS:
• Final Score: {final_score}/100
• Final Result: {final_passfail}
• Your Feedback: {student_data.get('Feedback', 'N/A')}

✅ ASSESSMENT COMPLETE:
The second marker (M2) has reviewed your assessment and confirmed agreement with your scoring and feedback. This assessment is now complete and finalized.

📊 PROCESS SUMMARY:
• Your Assessment (M1): {final_score}/100 - {final_passfail}
• M2 Review: AGREED with your assessment
• Status: COMPLETED - No further action required

Thank you for your thorough assessment and participation in the double-marking process.

Best regards,
Double-Marking System
Keele University

---
This is an automated completion notification from the Double-Marking AI Agent System.
"""

                m1_result = self.base_email_system._send_email(
                    to_email=student_data.get('M1_Email'),
                    subject=m1_subject,
                    body=m1_body
                )

                if m1_result.get('status') == 'delivered':
                    notifications_sent['M1_notification'] = {'status': 'delivered', 'message': 'M1 finalization notification sent successfully'}
                    notifications_sent['total_sent'] += 1
                else:
                    notifications_sent['M1_notification'] = {'status': 'failed', 'message': m1_result.get('message', 'Unknown error')}
                    notifications_sent['total_failed'] += 1

            except Exception as e:
                notifications_sent['M1_notification'] = {'status': 'error', 'message': f'Error sending M1 finalization: {str(e)}'}
                notifications_sent['total_failed'] += 1

            # 2. Send M2 finalization notification
            try:
                m2_subject = f"Assessment Complete: {student_data.get('StudentName')} ({student_data.get('StudentID')})"

                m2_body = f"""Dear {student_data.get('M2_Name')},

Thank you for completing your review. Your agreement has been processed and the assessment is now finalized:

📋 STUDENT DETAILS:
• Student: {student_data.get('StudentName')}
• Student ID: {student_data.get('StudentID')}
• Assignment: Computer Science Assessment

🎯 FINAL RESULTS:
• Final Score: {final_score}/100
• Final Result: {final_passfail}
• M1 Feedback: {student_data.get('Feedback', 'N/A')}

✅ YOUR AGREEMENT CONFIRMED:
You have successfully agreed with the M1 assessment. The double-marking process is now complete for this student.

📊 PROCESS SUMMARY:
• M1 Assessment: {final_score}/100 - {final_passfail}
• Your Review (M2): AGREED with M1 assessment
• Status: COMPLETED - Assessment finalized

Thank you for your participation in maintaining our assessment quality standards.

Best regards,
Double-Marking System
Keele University

---
This is an automated completion notification from the Double-Marking AI Agent System.
"""

                m2_result = self.base_email_system._send_email(
                    to_email=student_data.get('M2_Email'),
                    subject=m2_subject,
                    body=m2_body
                )

                if m2_result.get('status') == 'delivered':
                    notifications_sent['M2_notification'] = {'status': 'delivered', 'message': 'M2 finalization notification sent successfully'}
                    notifications_sent['total_sent'] += 1
                else:
                    notifications_sent['M2_notification'] = {'status': 'failed', 'message': m2_result.get('message', 'Unknown error')}
                    notifications_sent['total_failed'] += 1

            except Exception as e:
                notifications_sent['M2_notification'] = {'status': 'error', 'message': f'Error sending M2 finalization: {str(e)}'}
                notifications_sent['total_failed'] += 1

            logger.info(f"M2 agreement finalization notifications: {notifications_sent['total_sent']} sent, {notifications_sent['total_failed']} failed")
            return notifications_sent

        except Exception as e:
            logger.error(f"Error sending M2 agreement finalization notifications: {e}")
            return {
                'status': 'error',
                'message': f'Failed to send finalization notifications: {str(e)}',
                'notifications_sent': notifications_sent
            }

    def send_test_email(self, test_recipient: str) -> Dict:
        """Send a test email to verify the system is working."""
        if not self.email_available or not self.base_email_system:
            return {
                'status': 'failed',
                'message': 'Email system not configured. Set AGENT_EMAIL and AGENT_APP_PASSWORD in Streamlit secrets.'
            }
        return self.base_email_system.send_test_email(test_recipient)


# Global instance
enhanced_email_system = EnhancedEmailSystem()