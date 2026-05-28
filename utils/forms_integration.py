#!/usr/bin/env python3
"""
Enhanced Microsoft Forms Integration System

This module provides seamless integration between the UI and Microsoft Forms:
- Auto-export UI submissions to Forms-compatible format
- Auto-import M2 responses from Forms exports
- Real-time workflow status updates
- 5-minute sync cycles for M2 response monitoring

No Microsoft Graph API required - uses file-based operations only.

Author: Double-Marking System
Version: 1.0 - Enhanced Forms Integration
"""

import pandas as pd
import json
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import threading
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FormsIntegration:
    """
    Enhanced Microsoft Forms integration without Graph API.
    Handles export to Forms and import of M2 responses via file operations.
    """
    
    def __init__(self):
        """Initialize Forms integration system."""
        self.forms_export_dir = "data/forms_exports"
        self.forms_import_dir = "data/forms_imports" 
        self.submissions_file = "data/submissions.json"
        self.workflow_status_file = "data/workflow_status.json"
        
        # Ensure directories exist
        self._ensure_directories()
        
        # Initialize submission tracking
        self.submissions = self._load_submissions()
        self.workflow_status = self._load_workflow_status()
        
        # Auto-import monitoring
        self.auto_import_active = False
        self.import_thread = None
        
        logger.info("Forms Integration system initialized successfully")
    
    def _ensure_directories(self):
        """Create necessary directories."""
        for directory in [self.forms_export_dir, self.forms_import_dir, "data"]:
            os.makedirs(directory, exist_ok=True)
    
    def _load_submissions(self) -> Dict:
        """Load existing submissions tracking."""
        try:
            if os.path.exists(self.submissions_file):
                with open(self.submissions_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading submissions: {e}")
        
        return {"submissions": {}, "last_updated": datetime.now().isoformat()}
    
    def _save_submissions(self):
        """Save submissions tracking."""
        try:
            self.submissions["last_updated"] = datetime.now().isoformat()
            with open(self.submissions_file, 'w') as f:
                json.dump(self.submissions, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving submissions: {e}")
    
    def _load_workflow_status(self) -> Dict:
        """Load workflow status tracking."""
        try:
            if os.path.exists(self.workflow_status_file):
                with open(self.workflow_status_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading workflow status: {e}")
        
        return {
            "students": {},
            "stats": {
                "total_submissions": 0,
                "awaiting_m2": 0,
                "m2_agreed": 0,
                "m2_disagreed": 0,
                "escalated_to_m3": 0,
                "completed": 0
            },
            "last_updated": datetime.now().isoformat()
        }
    
    def _save_workflow_status(self):
        """Save workflow status."""
        try:
            self.workflow_status["last_updated"] = datetime.now().isoformat()
            with open(self.workflow_status_file, 'w') as f:
                json.dump(self.workflow_status, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving workflow status: {e}")
    
    def create_forms_template(self) -> str:
        """
        Create Microsoft Forms compatible template with all required columns.
        Returns the file path for manual upload to Microsoft Forms.
        """
        template_columns = [
            # Student Information
            'StudentID',
            'StudentName', 
            'Submission_Date',
            
            # M1 Assessment
            'M1_MarkerName',
            'M1_MarkerEmail',
            'M1_Score',
            'M1_PassFail',
            'M1_Feedback',
            'AI_Feedback_Optional',
            
            # M2 Assignment
            'M2_AssignedName',
            'M2_AssignedEmail',
            
            # M3 Assignment
            'M3_AssignedName', 
            'M3_AssignedEmail',
            
            # M2 Response (to be filled by M2)
            'M2_ResponseDate',
            'M2_MarkerName',
            'M2_Agree_Checkbox',
            'M2_Score',
            'M2_PassFail',
            'M2_Feedback',
            'M2_Comments',
            
            # M3 Response (to be filled by M3 if escalated)
            'M3_ResponseDate',
            'M3_MarkerName', 
            'M3_Score',
            'M3_PassFail',
            'M3_Feedback',
            'M3_Comments',
            
            # Final Results
            'Final_Score',
            'Final_PassFail',
            'Status',
            'Escalation_Required',
            'Completion_Date'
        ]
        
        # Create empty template
        template_df = pd.DataFrame(columns=template_columns)
        
        # Add sample row for reference
        sample_row = {
            'StudentID': 'SAMPLE_ID_DELETE_THIS_ROW',
            'StudentName': 'Sample Student - Delete This Row',
            'M1_MarkerName': 'Dr. Sample Marker',
            'M1_MarkerEmail': 'sample@keele.ac.uk',
            'M1_Score': '75',
            'M1_PassFail': 'Pass',
            'M1_Feedback': 'Sample feedback from M1',
            'M2_AssignedName': 'Dr. Second Marker',
            'M2_AssignedEmail': 'm2@keele.ac.uk',
            'M3_AssignedName': 'Dr. Third Marker',
            'M3_AssignedEmail': 'm3@keele.ac.uk',
            'Status': 'Awaiting M2',
            'Submission_Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        template_df = pd.concat([template_df, pd.DataFrame([sample_row])], ignore_index=True)
        
        # Save template
        template_path = os.path.join(self.forms_export_dir, f"Microsoft_Forms_Template_{datetime.now().strftime('%Y%m%d')}.xlsx")
        template_df.to_excel(template_path, index=False, engine='openpyxl')
        
        logger.info(f"Microsoft Forms template created: {template_path}")
        return template_path
    
    def export_submission_to_forms(self, assessment_data: Dict) -> Tuple[bool, str, str]:
        """
        Export a single UI submission to Microsoft Forms compatible format.
        Returns (success, message, file_path)
        """
        try:
            student_id = assessment_data.get('StudentID')
            
            # Create Forms row
            forms_row = {
                # Student Information
                'StudentID': student_id,
                'StudentName': assessment_data.get('StudentName'),
                'Submission_Date': assessment_data.get('Submission_Date', datetime.now().isoformat()),
                
                # M1 Assessment  
                'M1_MarkerName': assessment_data.get('M1_Name'),
                'M1_MarkerEmail': assessment_data.get('M1_Email'),
                'M1_Score': assessment_data.get('Score'),
                'M1_PassFail': assessment_data.get('PassFail'),
                'M1_Feedback': assessment_data.get('Feedback'),
                'AI_Feedback_Optional': assessment_data.get('AI_Feedback_Optional', ''),
                
                # M2 Assignment
                'M2_AssignedName': assessment_data.get('M2_Name'),
                'M2_AssignedEmail': assessment_data.get('M2_Email'),
                
                # M3 Assignment
                'M3_AssignedName': assessment_data.get('M3_Name'),
                'M3_AssignedEmail': assessment_data.get('M3_Email'),
                
                # Initial Status
                'Status': 'Awaiting M2',
                'Escalation_Required': 'No',
                
                # Empty M2/M3 response fields (to be filled later)
                'M2_ResponseDate': '',
                'M2_MarkerName': '',
                'M2_Agree_Checkbox': '',
                'M2_Score': '',
                'M2_PassFail': '',
                'M2_Feedback': '',
                'M2_Comments': '',
                
                'M3_ResponseDate': '',
                'M3_MarkerName': '',
                'M3_Score': '',
                'M3_PassFail': '',
                'M3_Feedback': '',
                'M3_Comments': '',
                
                'Final_Score': '',
                'Final_PassFail': '',
                'Completion_Date': ''
            }
            
            # Create DataFrame and save
            df = pd.DataFrame([forms_row])
            export_path = os.path.join(
                self.forms_export_dir, 
                f"Forms_Export_{student_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )
            df.to_excel(export_path, index=False, engine='openpyxl')
            
            # Track submission
            self.submissions["submissions"][student_id] = {
                "assessment_data": assessment_data,
                "forms_export_path": export_path,
                "export_date": datetime.now().isoformat(),
                "status": "Exported - Awaiting M2"
            }
            self._save_submissions()
            
            # Update workflow status
            self.workflow_status["students"][student_id] = {
                "student_name": assessment_data.get('StudentName'),
                "status": "Awaiting M2",
                "m1_complete": True,
                "m2_complete": False,
                "m3_complete": False,
                "export_date": datetime.now().isoformat()
            }
            
            self.workflow_status["stats"]["total_submissions"] += 1
            self.workflow_status["stats"]["awaiting_m2"] += 1
            self._save_workflow_status()
            
            logger.info(f"Successfully exported {student_id} to Forms format")
            return True, f"Successfully exported {student_id} to Microsoft Forms format", export_path
            
        except Exception as e:
            logger.error(f"Error exporting to Forms: {e}")
            return False, f"Error exporting to Forms: {str(e)}", ""
    
    def import_m2_responses(self, forms_file_path: str) -> Tuple[bool, str, int]:
        """
        Import M2 responses from Microsoft Forms export.
        Returns (success, message, updates_count)
        """
        try:
            # Read Forms export
            df = pd.read_excel(forms_file_path)
            logger.info(f"Reading Forms export with {len(df)} rows")
            
            updates_count = 0
            
            for _, row in df.iterrows():
                # Handle multiple StudentID column name formats
                student_id = ''
                for col_name in ['StudentID', 'Student ID', 'student_id', 'STUDENT_ID']:
                    if col_name in row and pd.notna(row[col_name]):
                        student_id = str(row[col_name]).strip()
                        break

                # Skip sample/header rows
                if not student_id or student_id.startswith('SAMPLE') or student_id == 'StudentID':
                    continue

                # Check if M2 has responded (handle all possible Microsoft Forms column name variations)
                m2_response_columns = [
                    'M2_ResponseDate', 'M2_Agree_Checkbox', 'M2_Score',
                    "Do you agree with M1's assessment?", "Do you agree with M1's assessment",
                    'Your Name', 'Submission_Date', 'Start time', 'Completion time'
                ]

                m2_responded = any(pd.notna(row.get(col)) for col in m2_response_columns if col in row)
                
                if m2_responded and student_id in self.workflow_status["students"]:
                    current_status = self.workflow_status["students"][student_id]
                    
                    # Only update if not already processed
                    if not current_status.get("m2_complete", False):
                        
                        # Process M2 response (handle all possible column name variations)
                        m2_agree_response = ''
                        for col_name in ["Do you agree with M1's assessment?", "Do you agree with M1's assessment"]:
                            if col_name in row and pd.notna(row[col_name]):
                                m2_agree_response = str(row[col_name]).lower()
                                break

                        m2_agreed = 'yes' in m2_agree_response or 'agree' in m2_agree_response or 'true' in m2_agree_response

                        # Handle score columns (with possible newlines in column names)
                        m2_score = None
                        for col_name in ['If No, what score would you give?', "If No, what score would you give?\n"]:
                            if col_name in row and pd.notna(row[col_name]):
                                m2_score = row[col_name]
                                break

                        # Handle feedback columns (with possible newlines in column names)
                        m2_feedback = ''
                        for col_name in ['If No, what is your feedback?', "If No, what is your feedback?\n"]:
                            if col_name in row and pd.notna(row[col_name]):
                                m2_feedback = str(row[col_name])
                                break

                        # Handle response date columns
                        response_date = datetime.now().isoformat()
                        for col_name in ['Submission_Date', 'Start time', 'Completion time']:
                            if col_name in row and pd.notna(row[col_name]):
                                response_date = str(row[col_name])
                                break
                        
                        # Update workflow status
                        self.workflow_status["students"][student_id].update({
                            "m2_complete": True,
                            "m2_agreed": m2_agreed,
                            "m2_response_date": str(response_date),
                            "m2_score": m2_score if pd.notna(m2_score) else None,
                            "m2_feedback": m2_feedback,
                            "status": "M2 Agreed" if m2_agreed else "M2 Disagreed - Needs M3"
                        })
                        
                        # Update statistics
                        self.workflow_status["stats"]["awaiting_m2"] -= 1
                        if m2_agreed:
                            self.workflow_status["stats"]["m2_agreed"] += 1
                            self.workflow_status["students"][student_id]["status"] = "Completed"
                            self.workflow_status["stats"]["completed"] += 1
                        else:
                            self.workflow_status["stats"]["m2_disagreed"] += 1
                            self.workflow_status["students"][student_id]["escalation_required"] = True
                        
                        updates_count += 1
                        logger.info(f"Updated M2 response for {student_id}: {'Agreed' if m2_agreed else 'Disagreed'}")
            
            self._save_workflow_status()
            
            message = f"Successfully imported {updates_count} M2 responses from Forms"
            logger.info(message)
            return True, message, updates_count
            
        except Exception as e:
            error_msg = f"Error importing M2 responses: {str(e)}"
            logger.error(error_msg)
            return False, error_msg, 0
    
    def get_workflow_status(self) -> Dict:
        """Get current workflow status for dashboard display."""
        return self.workflow_status.copy()
    
    def get_pending_m2_responses(self) -> List[Dict]:
        """Get list of submissions awaiting M2 responses."""
        pending = []
        for student_id, status in self.workflow_status["students"].items():
            if status["status"] == "Awaiting M2":
                pending.append({
                    "student_id": student_id,
                    "student_name": status.get("student_name"),
                    "export_date": status.get("export_date"),
                    "days_pending": self._calculate_days_pending(status.get("export_date"))
                })
        return pending
    
    def _calculate_days_pending(self, export_date: str) -> int:
        """Calculate days since export."""
        try:
            export_dt = datetime.fromisoformat(export_date.replace('Z', '+00:00'))
            return (datetime.now() - export_dt).days
        except:
            return 0
    
    def start_auto_import_monitoring(self, check_interval_minutes: int = 5):
        """Start background monitoring for M2 responses."""
        if self.auto_import_active:
            logger.info("Auto-import monitoring already active")
            return
        
        self.auto_import_active = True
        self.import_thread = threading.Thread(
            target=self._auto_import_loop,
            args=(check_interval_minutes,),
            daemon=True
        )
        self.import_thread.start()
        logger.info(f"Started auto-import monitoring (every {check_interval_minutes} minutes)")
    
    def stop_auto_import_monitoring(self):
        """Stop background monitoring."""
        self.auto_import_active = False
        if self.import_thread:
            self.import_thread.join(timeout=10)
        logger.info("Stopped auto-import monitoring")
    
    def _auto_import_loop(self, check_interval_minutes: int):
        """Background loop for auto-importing M2 responses."""
        while self.auto_import_active:
            try:
                # Check for new Forms imports
                import_files = [f for f in os.listdir(self.forms_import_dir) if f.endswith(('.xlsx', '.xls'))]
                
                for file_name in import_files:
                    file_path = os.path.join(self.forms_import_dir, file_name)

                    # Process all files in imports directory (removed time restriction)
                    success, message, count = self.import_m2_responses(file_path)
                    if success and count > 0:
                        logger.info(f"Auto-import: {message} from {file_name}")
                    elif success:
                        logger.info(f"Auto-import: No new responses in {file_name}")
                    else:
                        logger.warning(f"Auto-import: Failed to process {file_name} - {message}")
                        
                # Sleep for check interval
                time.sleep(check_interval_minutes * 60)
                
            except Exception as e:
                logger.error(f"Error in auto-import loop: {e}")
                time.sleep(60)  # Wait 1 minute before retrying

# Global instance
forms_integration = FormsIntegration()