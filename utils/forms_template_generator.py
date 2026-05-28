#!/usr/bin/env python3
"""
Microsoft Forms Template Generator
Generates exact questions and structure for M2/M3 response forms.
Super simple - just copy and paste!
"""

import json
import os
from datetime import datetime
from typing import Dict, List

class FormsTemplateGenerator:
    """Generate Microsoft Forms template with exact questions."""

    def __init__(self):
        self.config_file = "data/forms_config.json"
        self.ensure_data_dir()

    def ensure_data_dir(self):
        """Make sure data directory exists."""
        os.makedirs("data", exist_ok=True)

    def generate_forms_questions(self) -> Dict:
        """Generate all the questions you need to put in Microsoft Forms."""

        forms_template = {
            "form_title": "Double-Marking Assessment Response Form",
            "form_description": "Please review the student assessment and provide your response.",

            "sections": {
                "1_student_info": {
                    "title": "Student Information (Pre-filled)",
                    "description": "This information will be automatically filled from the email link",
                    "questions": [
                        {
                            "question": "Student ID",
                            "type": "Short answer",
                            "required": True,
                            "note": "This will be pre-filled from email link"
                        },
                        {
                            "question": "Student Name",
                            "type": "Short answer",
                            "required": True,
                            "note": "This will be pre-filled from email link"
                        },
                        {
                            "question": "Assignment Title",
                            "type": "Short answer",
                            "required": False,
                            "note": "Optional - can be pre-filled"
                        }
                    ]
                },

                "2_m1_assessment": {
                    "title": "M1 Assessment Details (Pre-filled)",
                    "description": "The first marker's assessment details",
                    "questions": [
                        {
                            "question": "M1 Marker Name",
                            "type": "Short answer",
                            "required": True,
                            "note": "Pre-filled from email"
                        },
                        {
                            "question": "M1 Score",
                            "type": "Number",
                            "required": True,
                            "note": "Pre-filled - the score M1 gave"
                        },
                        {
                            "question": "M1 Pass/Fail",
                            "type": "Choice (Pass/Fail)",
                            "required": True,
                            "note": "Pre-filled - M1's determination"
                        },
                        {
                            "question": "M1 Feedback",
                            "type": "Long answer",
                            "required": True,
                            "note": "Pre-filled - M1's detailed feedback"
                        }
                    ]
                },

                "3_your_response": {
                    "title": "Your Response (M2/M3 fills this)",
                    "description": "Please provide your assessment response",
                    "questions": [
                        {
                            "question": "Your Name",
                            "type": "Short answer",
                            "required": True,
                            "note": "Type your full name"
                        },
                        {
                            "question": "Your Email",
                            "type": "Short answer",
                            "required": True,
                            "note": "Your university email address"
                        },
                        {
                            "question": "Do you agree with M1's assessment?",
                            "type": "Choice (Yes/No)",
                            "required": True,
                            "note": "IMPORTANT: If Yes, skip the next questions. If No, fill them out."
                        },
                        {
                            "question": "If No, what score would you give?",
                            "type": "Number (0-100)",
                            "required": False,
                            "note": "Only fill if you disagreed above"
                        },
                        {
                            "question": "If No, what is your Pass/Fail determination?",
                            "type": "Choice (Pass/Fail)",
                            "required": False,
                            "note": "Only fill if you disagreed above"
                        },
                        {
                            "question": "If No, what is your feedback?",
                            "type": "Long answer",
                            "required": False,
                            "note": "Detailed feedback if you disagreed"
                        },
                        {
                            "question": "Additional Comments",
                            "type": "Long answer",
                            "required": False,
                            "note": "Any additional comments or notes"
                        }
                    ]
                }
            }
        }

        return forms_template

    def save_forms_url(self, forms_url: str) -> bool:
        """Save the Microsoft Forms URL after you create the form."""
        try:
            config = {
                "forms_url": forms_url,
                "created_date": datetime.now().isoformat(),
                "status": "active"
            }

            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)

            print(f"Forms URL saved successfully: {forms_url}")
            return True

        except Exception as e:
            print(f"Error saving Forms URL: {e}")
            return False

    def get_forms_url(self) -> str:
        """Get the saved Microsoft Forms URL."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                return config.get("forms_url", "")
            return ""
        except:
            return ""

    def create_setup_guide(self) -> str:
        """Create a simple setup guide for creating Microsoft Forms."""

        guide = """
=== MICROSOFT FORMS SETUP GUIDE ===

🎯 GOAL: Create a Microsoft Form for M2/M3 responses

⏰ TIME NEEDED: 10-15 minutes (one-time setup)

📋 STEP-BY-STEP INSTRUCTIONS:

STEP 1: Go to Microsoft Forms
  • Open your web browser
  • Go to: https://forms.microsoft.com
  • Sign in with your university account

STEP 2: Create New Form
  • Click "New Form"
  • Title: "Double-Marking Assessment Response Form"
  • Description: "Please review the student assessment and provide your response."

STEP 3: Add Questions (copy exactly as shown below)

--- SECTION 1: Student Information ---
Question 1: "Student ID"
  • Type: Short answer
  • Required: Yes

Question 2: "Student Name"
  • Type: Short answer
  • Required: Yes

Question 3: "Assignment Title"
  • Type: Short answer
  • Required: No

--- SECTION 2: M1 Assessment Details ---
Question 4: "M1 Marker Name"
  • Type: Short answer
  • Required: Yes

Question 5: "M1 Score"
  • Type: Number
  • Required: Yes
  • Restrictions: Between 0 and 100

Question 6: "M1 Pass/Fail"
  • Type: Choice
  • Options: Pass, Fail
  • Required: Yes

Question 7: "M1 Feedback"
  • Type: Long answer
  • Required: Yes

--- SECTION 3: Your Response ---
Question 8: "Your Name"
  • Type: Short answer
  • Required: Yes

Question 9: "Your Email"
  • Type: Short answer
  • Required: Yes

Question 10: "Do you agree with M1's assessment?"
  • Type: Choice
  • Options: Yes, No
  • Required: Yes

Question 11: "If No, what score would you give?"
  • Type: Number
  • Required: No
  • Restrictions: Between 0 and 100

Question 12: "If No, what is your Pass/Fail determination?"
  • Type: Choice
  • Options: Pass, Fail
  • Required: No

Question 13: "If No, what is your feedback?"
  • Type: Long answer
  • Required: No

Question 14: "Additional Comments"
  • Type: Long answer
  • Required: No

STEP 4: Save and Get URL
  • Click "Share"
  • Click "Copy link"
  • This is your Forms URL - save it!

STEP 5: Test the Form
  • Click the link to test it
  • Make sure all questions appear correctly

✅ DONE! Now you have your Microsoft Forms ready!

Next: Save the URL in our system (we'll show you how)
        """

        return guide

    def generate_sample_email_with_prefill(self, student_id: str, forms_url: str) -> str:
        """Generate sample email showing how pre-filled URLs work."""

        # Example pre-filled URL
        prefilled_url = f"{forms_url}?StudentID={student_id}&StudentName=Alice+Test+Student&M1_MarkerName=Dr.+John+Smith&M1_Score=85&M1_PassFail=Pass&M1_Feedback=Excellent+work+overall"

        sample_email = f"""
SAMPLE EMAIL THAT M2 WILL RECEIVE:

Subject: Assessment Review Required: Alice Test Student ({student_id})

Dear Dr. Second Marker,

You have been assigned as the second marker for the following assessment:

📋 STUDENT DETAILS:
• Student: Alice Test Student
• Student ID: {student_id}
• Assignment: Computer Science Project

📊 M1 ASSESSMENT:
• First Marker: Dr. John Smith
• Score: 85/100
• Pass/Fail: Pass
• Feedback: Excellent work overall with good understanding of concepts

🎯 YOUR TASK:
Please click the link below to submit your review. The form is pre-filled with student details:

👉 CLICK HERE TO RESPOND: {prefilled_url}

⏰ Please complete your review within 3 working days.

If you agree with M1's assessment, simply select "Yes" in the form.
If you disagree, please provide your own score and feedback.

Thank you,
Double-Marking System
Keele University
        """

        return sample_email

# Global instance
forms_generator = FormsTemplateGenerator()