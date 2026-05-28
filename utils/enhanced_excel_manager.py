#!/usr/bin/env python3
"""
Enhanced Excel Manager - NO API Required
Handles all Excel operations for the double-marking workflow system.

Features:
- Auto-populate Excel when M1 submits assessment
- Real-time Excel updates from Microsoft Forms responses
- Complete workflow tracking in single Excel file (39 columns)
- No Microsoft API permissions required
- Fixed agreement detection bug (critical)
- Cumulative Forms processing with duplicate filtering
- M1 escalation notification tracking

Author: Double-Marking System
Version: 6.0 - Critical Bug Fixes & Complete Email System (2024-09-17)
"""

import pandas as pd
import os
import logging
from datetime import datetime
import threading
import time
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Email system will be imported when needed to avoid circular imports
EMAIL_SYSTEM_AVAILABLE = True

class NoAPIExcelManager:
    """
    Enhanced Excel Manager that requires no APIs.
    Handles complete workflow from M1 submission to M3 resolution.
    """

    def __init__(self):
        """Initialize Excel Manager with file paths and monitoring."""
        self.master_file = "data/master_workflow.xlsx"
        self.import_folder = "data/forms_imports"
        self.export_folder = "data/forms_exports"
        self.config_file = "data/excel_config.json"

        # Ensure directories exist
        self._ensure_directories()

        # Initialize Excel file if it doesn't exist
        self._initialize_master_excel()

        # Forms monitoring
        self.monitoring_active = False
        self.monitor_thread = None
        self.processed_files = set()

        logger.info("Enhanced Excel Manager initialized successfully (NO API)")

    def _ensure_directories(self):
        """Create necessary directories."""
        for directory in ["data", self.import_folder, self.export_folder]:
            os.makedirs(directory, exist_ok=True)
            logger.info(f"Directory ensured: {directory}")

    def _initialize_master_excel(self):
        """Initialize master Excel file with all required columns."""
        if not os.path.exists(self.master_file):
            self.create_empty_master_excel()
            logger.info("Master Excel file created")

    def create_empty_master_excel(self) -> str:
        """Create empty Excel file with all 34 columns for the workflow."""

        columns = [
            # Student Information (3)
            'StudentID', 'StudentName', 'Submission_Date',

            # M1 Assessment (6)
            'M1_MarkerName', 'M1_MarkerEmail', 'M1_Score', 'M1_PassFail', 'M1_Feedback', 'AI_Feedback_Optional',

            # M2/M3 Assignments (4)
            'M2_AssignedName', 'M2_AssignedEmail', 'M3_AssignedName', 'M3_AssignedEmail',

            # M2 Response Fields (7)
            'M2_ResponseDate', 'M2_MarkerName', 'M2_Agree_Checkbox', 'M2_Score', 'M2_PassFail', 'M2_Feedback', 'M2_Comments',

            # M3 Response Fields (6)
            'M3_ResponseDate', 'M3_MarkerName', 'M3_Score', 'M3_PassFail', 'M3_Feedback', 'M3_Comments',

            # Final Results & Status (6)
            'Final_Score', 'Final_PassFail', 'Status', 'Escalation_Required', 'Completion_Date', 'Last_Updated',

            # System Tracking (7)
            'Forms_Link_Sent', 'M2_Email_Sent_Date', 'M3_Email_Sent_Date', 'M1_Escalation_Notification_Sent', 'M1_Finalization_Sent', 'M2_Finalization_Sent', 'Processing_Notes'
        ]

        # Create empty DataFrame with columns
        df = pd.DataFrame(columns=columns)

        # Save to Excel
        df.to_excel(self.master_file, index=False, engine='openpyxl')

        logger.info(f"Empty master Excel created with {len(columns)} columns")
        return self.master_file

    def auto_populate_m1_assessment(self, assessment_data: Dict) -> Tuple[bool, str]:
        """
        AUTO-POPULATE EXCEL when M1 submits assessment.
        This is Step 1 of the automated workflow.
        """
        try:
            # Load existing Excel
            if os.path.exists(self.master_file):
                df = pd.read_excel(self.master_file, engine='openpyxl')
            else:
                df = self.create_empty_dataframe()

            # Check if student already exists
            student_id = assessment_data['StudentID']
            if student_id in df['StudentID'].values:
                return False, f"Student {student_id} already exists in the system"

            # Create new row with M1 assessment data
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            new_row = {
                # Student Information
                'StudentID': student_id,
                'StudentName': assessment_data['StudentName'],
                'Submission_Date': current_time,

                # M1 Assessment (from UI form)
                'M1_MarkerName': assessment_data['M1_Name'],
                'M1_MarkerEmail': assessment_data['M1_Email'],
                'M1_Score': assessment_data['Score'],
                'M1_PassFail': assessment_data['PassFail'],
                'M1_Feedback': assessment_data['Feedback'],
                'AI_Feedback_Optional': assessment_data.get('AI_Feedback_Optional', ''),

                # M2/M3 Assignments (from UI form)
                'M2_AssignedName': assessment_data['M2_Name'],
                'M2_AssignedEmail': assessment_data['M2_Email'],
                'M3_AssignedName': assessment_data['M3_Name'],
                'M3_AssignedEmail': assessment_data['M3_Email'],

                # Initial Status
                'Status': 'Awaiting M2',
                'Escalation_Required': 'No',
                'Forms_Link_Sent': 'No',
                'Last_Updated': current_time,
                'Processing_Notes': 'M1 assessment submitted',

                # Empty fields for M2 response (will be filled when M2 responds)
                'M2_ResponseDate': '',
                'M2_MarkerName': '',
                'M2_Agree_Checkbox': '',
                'M2_Score': '',
                'M2_PassFail': '',
                'M2_Feedback': '',
                'M2_Comments': '',

                # Empty fields for M3 response (will be filled if escalated)
                'M3_ResponseDate': '',
                'M3_MarkerName': '',
                'M3_Score': '',
                'M3_PassFail': '',
                'M3_Feedback': '',
                'M3_Comments': '',

                # Final results (will be determined later)
                'Final_Score': '',
                'Final_PassFail': '',
                'Completion_Date': '',
                'M2_Email_Sent_Date': '',
                'M3_Email_Sent_Date': ''
            }

            # Add new row to DataFrame
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

            # Save to Excel file
            df.to_excel(self.master_file, index=False, engine='openpyxl')

            logger.info(f"AUTO-POPULATED: {student_id} added to master Excel")
            return True, f"SUCCESS: {student_id} successfully added to Excel with all M1 data"

        except Exception as e:
            error_msg = f"Error auto-populating Excel: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

    def create_empty_dataframe(self) -> pd.DataFrame:
        """Create empty DataFrame with correct columns."""
        columns = [
            'StudentID', 'StudentName', 'Submission_Date',
            'M1_MarkerName', 'M1_MarkerEmail', 'M1_Score', 'M1_PassFail', 'M1_Feedback', 'AI_Feedback_Optional',
            'M2_AssignedName', 'M2_AssignedEmail', 'M3_AssignedName', 'M3_AssignedEmail',
            'M2_ResponseDate', 'M2_MarkerName', 'M2_Agree_Checkbox', 'M2_Score', 'M2_PassFail', 'M2_Feedback', 'M2_Comments',
            'M3_ResponseDate', 'M3_MarkerName', 'M3_Score', 'M3_PassFail', 'M3_Feedback', 'M3_Comments',
            'Final_Score', 'Final_PassFail', 'Status', 'Escalation_Required', 'Completion_Date', 'Last_Updated',
            'Forms_Link_Sent', 'M2_Email_Sent_Date', 'M3_Email_Sent_Date', 'Processing_Notes'
        ]
        return pd.DataFrame(columns=columns)

    def get_all_submissions(self) -> pd.DataFrame:
        """Get all submissions from master Excel for dashboard display."""
        try:
            if os.path.exists(self.master_file):
                df = pd.read_excel(self.master_file, engine='openpyxl')
                return df
            else:
                return self.create_empty_dataframe()
        except Exception as e:
            logger.error(f"Error loading submissions: {e}")
            return self.create_empty_dataframe()

    def get_workflow_statistics(self) -> Dict:
        """Get real-time workflow statistics for dashboard."""
        try:
            df = self.get_all_submissions()

            if df.empty:
                return {
                    'total_submissions': 0,
                    'awaiting_m2': 0,
                    'm2_agreed': 0,
                    'm2_disagreed': 0,
                    'escalated_to_m3': 0,
                    'completed': 0,
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }

            stats = {
                'total_submissions': len(df),
                'awaiting_m2': len(df[df['Status'] == 'Awaiting M2']),
                'm2_agreed': len(df[df['Status'] == 'Completed - M2 Agreed']),
                'm2_disagreed': len(df[df['Status'] == 'Escalated to M3']),
                'escalated_to_m3': len(df[df['Escalation_Required'] == 'Yes']),
                'completed': len(df[df['Status'].str.contains('Completed', na=False)]),
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            return stats

        except Exception as e:
            logger.error(f"Error calculating statistics: {e}")
            return {'error': str(e)}

    def start_forms_monitoring(self) -> str:
        """Start background monitoring for Microsoft Forms responses."""
        if self.monitoring_active:
            return "⚠️ Forms monitoring is already active"

        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._forms_monitor_loop, daemon=True)
        self.monitor_thread.start()

        logger.info("Forms response monitoring started")
        return f"Forms monitoring started - watching {self.import_folder}/"

    def stop_forms_monitoring(self) -> str:
        """Stop background monitoring."""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)

        logger.info("Forms response monitoring stopped")
        return "Forms monitoring stopped"

    def _forms_monitor_loop(self):
        """Background monitoring loop for Forms responses."""
        logger.info("Forms monitoring loop started")

        while self.monitoring_active:
            try:
                # Check for new Excel files in import folder
                if os.path.exists(self.import_folder):
                    for file_name in os.listdir(self.import_folder):
                        if file_name.endswith(('.xlsx', '.xls')) and file_name not in self.processed_files:

                            file_path = os.path.join(self.import_folder, file_name)
                            logger.info(f"New Forms file detected: {file_name}")

                            # Process the Forms response
                            success, message = self.process_forms_response(file_path)

                            if success:
                                logger.info(f"Processed: {message}")
                                self.processed_files.add(file_name)
                            else:
                                logger.error(f"Failed: {message}")

                # Check every 10 seconds
                time.sleep(10)

            except Exception as e:
                logger.error(f"Error in Forms monitoring loop: {e}")
                time.sleep(30)  # Wait longer on error

    def process_forms_response(self, forms_file_path: str) -> Tuple[bool, str]:
        """
        Process Microsoft Forms response and auto-update Excel.
        This is Step 3 of the automated workflow.
        """
        try:
            # Read Forms export file
            forms_df = pd.read_excel(forms_file_path, engine='openpyxl')
            logger.info(f"Processing Forms file with {len(forms_df)} responses")
            logger.info(f"Forms file columns: {list(forms_df.columns)}")

            # Log first few rows for debugging
            for idx, row in forms_df.iterrows():
                logger.info(f"Row {idx}: Student ID columns check")
                for col_name in ['StudentID', 'Student ID', 'student_id', 'STUDENT_ID']:
                    if col_name in row:
                        logger.info(f"  {col_name}: {row[col_name]}")
                break  # Just log first row

            # Load master Excel
            master_df = pd.read_excel(self.master_file, engine='openpyxl')

            updates_count = 0

            # Process each Forms response
            for _, response in forms_df.iterrows():
                # Handle multiple StudentID column name formats
                student_id = ''
                for col_name in ['StudentID', 'Student ID', 'student_id', 'STUDENT_ID']:
                    if col_name in response and pd.notna(response[col_name]):
                        student_id = str(response[col_name]).strip()
                        break

                # Skip empty or sample rows
                if not student_id or student_id.startswith('SAMPLE') or student_id == 'StudentID':
                    logger.info(f"Skipping row - empty/sample StudentID: '{student_id}'")
                    continue

                logger.info(f"Processing student: {student_id}")

                # Check if this student exists in our system
                if student_id in master_df['StudentID'].values:
                    logger.info(f"Student {student_id} found in master Excel")

                    # Get current student status for debugging
                    student_row = master_df[master_df['StudentID'] == student_id].iloc[0]
                    current_status = student_row['Status']
                    m2_response_date = student_row.get('M2_ResponseDate', 'Not set')
                    logger.info(f"Student {student_id} - Status: {current_status}, M2_ResponseDate: {m2_response_date}")

                    success = self._update_excel_with_forms_response(student_id, response)
                    if success:
                        updates_count += 1
                        logger.info(f"Successfully updated Excel with response for {student_id}")
                    else:
                        logger.warning(f"Failed to update Excel for student {student_id} - likely already processed or wrong status")
                else:
                    logger.warning(f"Student {student_id} NOT FOUND in master Excel")
                    logger.info(f"Available students: {list(master_df['StudentID'])}")

            logger.info(f"Total updates completed: {updates_count}")

            if updates_count > 0:
                return True, f"Successfully processed {updates_count} Forms responses"
            else:
                return False, "No valid responses found in Forms file"

        except Exception as e:
            error_msg = f"Error processing Forms response: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

    def _update_excel_with_forms_response(self, student_id: str, response: pd.Series) -> bool:
        """Update master Excel with M2/M3 Forms response."""
        try:
            # Load current Excel
            df = pd.read_excel(self.master_file, engine='openpyxl')

            # Find the student row
            student_mask = df['StudentID'] == student_id
            if not student_mask.any():
                logger.warning(f"Student {student_id} not found in Excel")
                return False

            student_idx = df[student_mask].index[0]
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Determine if this is M2 or M3 response and check for duplicates
            current_status = df.loc[student_idx, 'Status']

            # Check if this is a new M2 response (student in "Awaiting M2" status and no M2_ResponseDate)
            if current_status == 'Awaiting M2' and pd.isna(df.loc[student_idx, 'M2_ResponseDate']):
                logger.info(f"Processing new M2 response for {student_id}")
                self._process_m2_response(df, student_idx, response, current_time)

                # Save updated Excel
                df.to_excel(self.master_file, index=False, engine='openpyxl')
                return True

            # Check if this is a new M3 response (student in "Escalated to M3" status and no M3_ResponseDate)
            elif current_status == 'Escalated to M3' and pd.isna(df.loc[student_idx, 'M3_ResponseDate']):
                logger.info(f"Processing new M3 response for {student_id}")
                self._process_m3_response(df, student_idx, response, current_time)

                # Save updated Excel
                df.to_excel(self.master_file, index=False, engine='openpyxl')
                return True

            else:
                # Response already processed or student not in correct status
                logger.info(f"Skipping {student_id} - already processed or incorrect status. Current status: {current_status}, M2_ResponseDate: {df.loc[student_idx, 'M2_ResponseDate']}")
                return False

        except Exception as e:
            logger.error(f"Error updating Excel with Forms response: {e}")
            return False

    def _process_m2_response(self, df: pd.DataFrame, student_idx: int, response: pd.Series, current_time: str):
        """Process M2 response from Forms."""

        # Extract marker information from form response (handle multiple possible column names)
        submitted_name = ''
        for col_name in ['Your Name', 'Name', 'Marker Name', 'your name']:
            if col_name in response and pd.notna(response[col_name]):
                submitted_name = str(response[col_name]).strip()
                break

        submitted_email = ''
        for col_name in ['Your Email', 'Email', 'Marker Email', 'your email']:
            if col_name in response and pd.notna(response[col_name]):
                submitted_email = str(response[col_name]).strip()
                break

        # Get assigned M2 information from Excel
        assigned_m2_name = str(df.loc[student_idx, 'M2_AssignedName']).strip()
        assigned_m2_email = str(df.loc[student_idx, 'M2_AssignedEmail']).strip()

        # Validate marker identity (check if submitted name/email matches assigned M2)
        name_match = (submitted_name.lower() in assigned_m2_name.lower() or
                     assigned_m2_name.lower() in submitted_name.lower())
        email_match = (submitted_email.lower() == assigned_m2_email.lower())

        # Log validation results
        if not (name_match or email_match):
            logger.warning(f"M2 marker validation warning for {df.loc[student_idx, 'StudentID']}: "
                         f"Submitted: {submitted_name} <{submitted_email}>, "
                         f"Assigned: {assigned_m2_name} <{assigned_m2_email}>")

        # Update M2 response fields (use submitted info but log discrepancies)
        df.loc[student_idx, 'M2_ResponseDate'] = str(current_time)
        df.loc[student_idx, 'M2_MarkerName'] = submitted_name
        df.loc[student_idx, 'M2_MarkerEmail'] = submitted_email

        # Add validation status
        validation_status = "Validated" if (name_match or email_match) else "Warning: Identity mismatch"
        df.loc[student_idx, 'M2_Validation_Status'] = validation_status

        # Check if M2 agrees (handle multiple possible column names)
        agree_response = ''
        for col_name in ["Do you agree with M1's assessment?", "Do you agree with M1's assessment"]:
            if col_name in response and pd.notna(response[col_name]):
                agree_response = str(response[col_name]).lower()
                break

        # Fix agreement detection - check for positive agreement, not just presence of 'agree'
        agreed = (
            'yes - i agree' in agree_response or
            'yes, i agree' in agree_response or
            agree_response.startswith('yes') or
            'true' in agree_response
        ) and 'disagree' not in agree_response and 'no -' not in agree_response

        df.loc[student_idx, 'M2_Agree_Checkbox'] = str('Yes' if agreed else 'No')

        if agreed:
            # M2 agrees - assessment is complete
            df.loc[student_idx, 'Status'] = str('Completed - M2 Agreed')
            df.loc[student_idx, 'Final_Score'] = df.loc[student_idx, 'M1_Score']
            df.loc[student_idx, 'Final_PassFail'] = str(df.loc[student_idx, 'M1_PassFail'])
            df.loc[student_idx, 'Completion_Date'] = str(current_time)
            df.loc[student_idx, 'Processing_Notes'] = str('M2 agreed with M1 assessment')

            # Send finalization emails to M1 and M2 when M2 agrees
            if EMAIL_SYSTEM_AVAILABLE:
                try:
                    # Import email system dynamically to avoid circular imports
                    from utils.enhanced_email_system import enhanced_email_system

                    # Prepare student data for finalization emails
                    student_data = {
                        'StudentID': df.loc[student_idx, 'StudentID'],
                        'StudentName': df.loc[student_idx, 'StudentName'],
                        'M1_Name': df.loc[student_idx, 'M1_MarkerName'],
                        'M1_Email': df.loc[student_idx, 'M1_MarkerEmail'],
                        'M2_Name': submitted_name,
                        'M2_Email': submitted_email,
                        'Score': df.loc[student_idx, 'M1_Score'],
                        'PassFail': df.loc[student_idx, 'M1_PassFail'],
                        'Feedback': df.loc[student_idx, 'M1_Feedback']
                    }

                    # Send finalization emails to both M1 and M2
                    finalization_result = enhanced_email_system.send_m2_agreement_finalization_emails(student_data)

                    # Track email delivery in Excel
                    if finalization_result.get('M1_notification', {}).get('status') == 'delivered':
                        df.loc[student_idx, 'M1_Finalization_Sent'] = current_time
                        logger.info(f"M1 finalization email sent successfully for {student_data['StudentID']}")

                    if finalization_result.get('M2_notification', {}).get('status') == 'delivered':
                        df.loc[student_idx, 'M2_Finalization_Sent'] = current_time
                        logger.info(f"M2 finalization email sent successfully for {student_data['StudentID']}")

                    if finalization_result.get('total_sent', 0) > 0:
                        logger.info(f"Finalization emails sent: {finalization_result.get('total_sent', 0)} successful, {finalization_result.get('total_failed', 0)} failed")
                    else:
                        logger.error(f"Failed to send finalization emails: {finalization_result.get('message', 'Unknown error')}")

                except Exception as e:
                    logger.error(f"Error sending finalization emails: {e}")
            else:
                logger.warning("Email system not available - finalization emails not sent")

        else:
            # M2 disagrees - escalate to M3
            df.loc[student_idx, 'Status'] = str('Escalated to M3')
            df.loc[student_idx, 'Escalation_Required'] = str('Yes')
            # Handle M2 score with possible column name variations
            m2_score = ''
            for col_name in ['If No, what score would you give?', "If No, what score would you give?\n"]:
                if col_name in response and pd.notna(response[col_name]):
                    m2_score = str(response[col_name])
                    break

            # Handle M2 feedback with possible column name variations
            m2_feedback = ''
            for col_name in ['If No, what is your feedback?', "If No, what is your feedback?\n"]:
                if col_name in response and pd.notna(response[col_name]):
                    m2_feedback = str(response[col_name])
                    break

            df.loc[student_idx, 'M2_Score'] = m2_score
            df.loc[student_idx, 'M2_Feedback'] = m2_feedback
            df.loc[student_idx, 'Processing_Notes'] = 'M2 disagreed - escalated to M3'

            # Send M3 escalation email with Forms link
            if EMAIL_SYSTEM_AVAILABLE:
                try:
                    # Import email system dynamically to avoid circular imports
                    from utils.enhanced_email_system import enhanced_email_system

                    # Prepare student data for M3 escalation
                    student_data = {
                        'StudentID': df.loc[student_idx, 'StudentID'],
                        'StudentName': df.loc[student_idx, 'StudentName'],
                        'M1_Name': df.loc[student_idx, 'M1_MarkerName'],
                        'M1_Email': df.loc[student_idx, 'M1_MarkerEmail'],
                        'Score': df.loc[student_idx, 'M1_Score'],
                        'PassFail': df.loc[student_idx, 'M1_PassFail'],
                        'Feedback': df.loc[student_idx, 'M1_Feedback'],
                        'M3_Name': df.loc[student_idx, 'M3_AssignedName'],
                        'M3_Email': df.loc[student_idx, 'M3_AssignedEmail']
                    }

                    # Prepare M2 data for escalation
                    m2_data = {
                        'marker_name': submitted_name,
                        'score': m2_score,
                        'feedback': m2_feedback
                    }

                    # Send M3 escalation email
                    email_result = enhanced_email_system.send_m3_escalation_with_forms(student_data, m2_data)

                    if email_result.get('status') == 'delivered':
                        df.loc[student_idx, 'M3_Email_Sent_Date'] = current_time
                        logger.info(f"M3 escalation email sent successfully for {student_data['StudentID']}")
                    else:
                        logger.error(f"Failed to send M3 escalation email: {email_result.get('message')}")

                    # Send M1 escalation notification when M2 disagrees
                    m1_notification_result = enhanced_email_system.send_m1_escalation_notification(student_data, m2_data)

                    if m1_notification_result.get('status') == 'delivered':
                        df.loc[student_idx, 'M1_Escalation_Notification_Sent'] = current_time
                        logger.info(f"M1 escalation notification sent successfully for {student_data['StudentID']}")
                    else:
                        logger.error(f"Failed to send M1 escalation notification: {m1_notification_result.get('message')}")

                except Exception as e:
                    logger.error(f"Error sending M3 escalation email: {e}")
            else:
                logger.warning("Email system not available - M3 escalation email not sent")

        df.loc[student_idx, 'M2_Comments'] = str(response.get('Additional Comments', ''))
        df.loc[student_idx, 'Last_Updated'] = current_time

    def _process_m3_response(self, df: pd.DataFrame, student_idx: int, response: pd.Series, current_time: str):
        """Process M3 response from Forms."""

        # Extract marker information from form response (handle multiple possible column names)
        submitted_name = ''
        for col_name in ['Your Name', 'Name', 'Marker Name', 'your name']:
            if col_name in response and pd.notna(response[col_name]):
                submitted_name = str(response[col_name]).strip()
                break

        submitted_email = ''
        for col_name in ['Your Email', 'Email', 'Marker Email', 'your email']:
            if col_name in response and pd.notna(response[col_name]):
                submitted_email = str(response[col_name]).strip()
                break

        # Get assigned M3 information from Excel
        assigned_m3_name = str(df.loc[student_idx, 'M3_AssignedName']).strip()
        assigned_m3_email = str(df.loc[student_idx, 'M3_AssignedEmail']).strip()

        # Validate marker identity (check if submitted name/email matches assigned M3)
        name_match = (submitted_name.lower() in assigned_m3_name.lower() or
                     assigned_m3_name.lower() in submitted_name.lower())
        email_match = (submitted_email.lower() == assigned_m3_email.lower())

        # Log validation results
        if not (name_match or email_match):
            logger.warning(f"M3 marker validation warning for {df.loc[student_idx, 'StudentID']}: "
                         f"Submitted: {submitted_name} <{submitted_email}>, "
                         f"Assigned: {assigned_m3_name} <{assigned_m3_email}>")

        # Update M3 response fields (use submitted info but log discrepancies)
        df.loc[student_idx, 'M3_ResponseDate'] = current_time
        df.loc[student_idx, 'M3_MarkerName'] = submitted_name
        df.loc[student_idx, 'M3_MarkerEmail'] = submitted_email
        df.loc[student_idx, 'M3_Score'] = response.get('Final Score', '')
        df.loc[student_idx, 'M3_PassFail'] = response.get('Final Pass/Fail', '')
        df.loc[student_idx, 'M3_Feedback'] = response.get('M3 Final Feedback', '')
        df.loc[student_idx, 'M3_Comments'] = response.get('M3 Comments', '')

        # Add validation status
        validation_status = "Validated" if (name_match or email_match) else "Warning: Identity mismatch"
        df.loc[student_idx, 'M3_Validation_Status'] = validation_status

        # M3 decision is final
        df.loc[student_idx, 'Status'] = 'Completed - M3 Final Decision'
        df.loc[student_idx, 'Final_Score'] = response.get('Final Score', '')
        df.loc[student_idx, 'Final_PassFail'] = response.get('Final Pass/Fail', '')
        df.loc[student_idx, 'Completion_Date'] = current_time
        df.loc[student_idx, 'Processing_Notes'] = 'M3 made final decision'
        df.loc[student_idx, 'Last_Updated'] = current_time

        # Send M3 final decision notifications to M1, M2, and Student
        if EMAIL_SYSTEM_AVAILABLE:
            try:
                from utils.enhanced_email_system import enhanced_email_system

                # Get student row data for notifications
                student_row = df.iloc[student_idx]

                # Prepare student data for notifications
                student_data = {
                    'StudentID': student_row['StudentID'],
                    'StudentName': student_row['StudentName'],
                    'M1_Name': student_row['M1_MarkerName'],
                    'M1_Email': student_row['M1_MarkerEmail'],
                    'Score': student_row['M1_Score'],
                    'PassFail': student_row['M1_PassFail'],
                    'Feedback': student_row['M1_Feedback'],
                    'M2_Name': student_row['M2_AssignedName'],
                    'M2_Email': student_row['M2_AssignedEmail'],
                    'StudentEmail': student_row.get('StudentEmail', '')  # Optional student email
                }

                # Prepare M3 data for notifications
                m3_data = {
                    'final_score': response.get('Final Score', 'N/A'),
                    'final_passfail': response.get('Final Pass/Fail', 'N/A'),
                    'final_feedback': response.get('M3 Final Feedback', 'No additional feedback provided.'),
                    'm3_name': response.get('Your Name', 'Third Marker')
                }

                # Send notifications
                notification_result = enhanced_email_system.send_m3_final_decision_notifications(student_data, m3_data)

                if notification_result.get('total_sent', 0) > 0:
                    logger.info(f"M3 final decision notifications sent for {student_data['StudentID']}: {notification_result['total_sent']} successful")

                if notification_result.get('total_failed', 0) > 0:
                    logger.warning(f"Some M3 final decision notifications failed for {student_data['StudentID']}: {notification_result['total_failed']} failed")

            except Exception as e:
                logger.error(f"Error sending M3 final decision notifications: {e}")
        else:
            logger.warning("Email system not available - M3 final decision notifications not sent")

    def update_email_sent_status(self, student_id: str, email_type: str) -> bool:
        """Update Excel when emails are sent."""
        try:
            df = pd.read_excel(self.master_file, engine='openpyxl')

            student_mask = df['StudentID'] == student_id
            if student_mask.any():
                student_idx = df[student_mask].index[0]
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                if email_type == 'M2':
                    df.loc[student_idx, 'M2_Email_Sent_Date'] = current_time
                    df.loc[student_idx, 'Forms_Link_Sent'] = 'Yes'
                elif email_type == 'M3':
                    df.loc[student_idx, 'M3_Email_Sent_Date'] = current_time

                df.loc[student_idx, 'Last_Updated'] = current_time

                df.to_excel(self.master_file, index=False, engine='openpyxl')
                return True

            return False

        except Exception as e:
            logger.error(f"Error updating email status: {e}")
            return False

    def update_student_record(self, student_id: str, updated_data: Dict) -> bool:
        """Update student record with new data from edit form."""
        try:
            df = pd.read_excel(self.master_file, engine='openpyxl')

            student_mask = df['StudentID'] == student_id
            if student_mask.any():
                student_idx = df[student_mask].index[0]
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Update the specified fields
                for field, value in updated_data.items():
                    if field in df.columns:
                        df.loc[student_idx, field] = value

                # Always update the last modified timestamp
                df.loc[student_idx, 'Last_Updated'] = current_time

                # Save the Excel file
                df.to_excel(self.master_file, index=False, engine='openpyxl')
                logger.info(f"Updated student record for {student_id}")
                return True

            else:
                logger.warning(f"Student {student_id} not found in Excel file")
                return False

        except Exception as e:
            logger.error(f"Error updating student record: {e}")
            return False

    def delete_student_record(self, student_id: str) -> bool:
        """Delete student record from Excel file."""
        try:
            df = pd.read_excel(self.master_file, engine='openpyxl')

            student_mask = df['StudentID'] == student_id
            if student_mask.any():
                # Remove the student row
                df = df[~student_mask]

                # Save the updated Excel file
                df.to_excel(self.master_file, index=False, engine='openpyxl')
                logger.info(f"Deleted student record for {student_id}")
                return True

            else:
                logger.warning(f"Student {student_id} not found in Excel file")
                return False

        except Exception as e:
            logger.error(f"Error deleting student record: {e}")
            return False

    def export_excel_for_download(self, filter_status: Optional[str] = None) -> Tuple[bool, str, bytes]:
        """Export Excel data for download with optional filtering."""
        try:
            df = self.get_all_submissions()

            # Apply filter if specified
            if filter_status and filter_status != "All":
                df = df[df['Status'] == filter_status]

            # Create Excel bytes for download
            from io import BytesIO
            excel_buffer = BytesIO()

            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Workflow Data', index=False)

            excel_bytes = excel_buffer.getvalue()
            filename = f"Workflow_Export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

            return True, filename, excel_bytes

        except Exception as e:
            error_msg = f"Error exporting Excel: {str(e)}"
            logger.error(error_msg)
            return False, error_msg, b""

    def get_pending_m2_responses(self) -> List[Dict]:
        """Get list of submissions awaiting M2 responses."""
        try:
            df = self.get_all_submissions()
            pending_m2 = df[df['Status'] == 'Awaiting M2']

            pending_list = []
            for _, row in pending_m2.iterrows():
                # Calculate days pending
                try:
                    submit_date = pd.to_datetime(row['Submission_Date'])
                    days_pending = (datetime.now() - submit_date).days
                except:
                    days_pending = 0

                pending_list.append({
                    'StudentID': row['StudentID'],
                    'StudentName': row['StudentName'],
                    'M2_AssignedName': row['M2_AssignedName'],
                    'M2_AssignedEmail': row['M2_AssignedEmail'],
                    'Submission_Date': row['Submission_Date'],
                    'Days_Pending': days_pending
                })

            return pending_list

        except Exception as e:
            logger.error(f"Error getting pending M2 responses: {e}")
            return []

# Global instance
enhanced_excel_manager = NoAPIExcelManager()