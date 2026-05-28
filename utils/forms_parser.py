import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Union
import io

class FormsParser:
    """
    Parses Microsoft Forms export data and derives workflow status.
    Handles Excel and CSV formats with the required schema.
    """
    
    REQUIRED_COLUMNS = [
        'StudentID', 'StudentName', 'MarkerRole', 'MarkerName', 
        'MarkerEmail', 'Score', 'PassFail', 'Feedback', 
        'AI_Feedback_Optional', 'M2_MarkerName', 'M2_MarkerEmail',
        'M3_MarkerName', 'M3_MarkerEmail', 'M2_Agree_Checkbox', 'M2_Score', 'M2_Feedback'
    ]
    
    def __init__(self):
        self.data = None
        self.processed_data = None
    
    def parse_forms_data(self, uploaded_file) -> pd.DataFrame:
        """
        Parse uploaded Forms data and derive workflow status.
        
        Args:
            uploaded_file: Streamlit uploaded file object (Excel or CSV)
            
        Returns:
            pd.DataFrame: Processed data with derived status columns
        """
        try:
            # Read the file based on type
            if uploaded_file.name.endswith('.xlsx'):
                self.data = pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith('.csv'):
                self.data = pd.read_csv(uploaded_file)
            else:
                raise ValueError("Unsupported file format. Please use Excel (.xlsx) or CSV (.csv)")
            
            # Validate required columns
            self._validate_columns()
            
            # Clean and process data
            self._clean_data()
            
            # Derive workflow status
            self.processed_data = self._derive_workflow_status()
            
            return self.processed_data
            
        except Exception as e:
            raise Exception(f"Error parsing forms data: {str(e)}")
    
    def _validate_columns(self):
        """Validate that all required columns are present."""
        missing_cols = [col for col in self.REQUIRED_COLUMNS if col not in self.data.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
    
    def _clean_data(self):
        """Clean and standardize the data."""
        # Convert data types
        self.data['StudentID'] = self.data['StudentID'].astype(str).str.strip()
        self.data['MarkerRole'] = self.data['MarkerRole'].str.upper().str.strip()
        self.data['Score'] = pd.to_numeric(self.data['Score'], errors='coerce')
        self.data['M2_Agree_Checkbox'] = self.data['M2_Agree_Checkbox'].fillna(False)
        
        # Handle boolean conversion for M2_Agree_Checkbox
        bool_map = {'true': True, 'false': False, 'yes': True, 'no': False, '1': True, '0': False}
        self.data['M2_Agree_Checkbox'] = self.data['M2_Agree_Checkbox'].replace(bool_map)
        self.data['M2_Agree_Checkbox'] = self.data['M2_Agree_Checkbox'].astype(bool)
        
        # Auto-determine Pass/Fail based on score (above 50 = Pass, 50 and below = Fail)
        self.data['PassFail_Auto'] = self.data['Score'].apply(self._determine_pass_fail)
        
        # Use manual PassFail if provided, otherwise use auto-determined value
        self.data['PassFail'] = self.data['PassFail'].fillna(self.data['PassFail_Auto'])
        
        # Add timestamp if not present
        if 'Timestamp' not in self.data.columns:
            self.data['Timestamp'] = datetime.now()
        
        # Sort by StudentID and timestamp for proper processing order
        self.data = self.data.sort_values(['StudentID', 'Timestamp'])
    
    def _determine_pass_fail(self, score) -> str:
        """
        Determine Pass/Fail based on score.
        
        Args:
            score: Numeric score
            
        Returns:
            str: 'Pass' if score > 50, 'Fail' if score <= 50, NaN if score is missing
        """
        if pd.isna(score):
            return pd.NA
        return 'Pass' if score > 50 else 'Fail'
    
    def _derive_workflow_status(self) -> pd.DataFrame:
        """
        Derive workflow status for each student based on submission patterns.
        
        Returns:
            pd.DataFrame: Data with derived Status, M1_Score, M2_Score, Final_Score columns
        """
        results = []
        
        # Group by StudentID to analyze submission patterns
        for student_id, group in self.data.groupby('StudentID'):
            student_status = self._analyze_student_submissions(student_id, group)
            results.extend(student_status)
        
        return pd.DataFrame(results)
    
    def _analyze_student_submissions(self, student_id: str, group: pd.DataFrame) -> List[Dict]:
        """
        Analyze submissions for a single student and determine workflow status.
        
        Args:
            student_id: Student identifier
            group: All submissions for this student
            
        Returns:
            List[Dict]: Processed records for this student
        """
        results = []
        
        # Separate M1 and M2 submissions
        m1_submissions = group[group['MarkerRole'] == 'M1'].copy()
        m2_submissions = group[group['MarkerRole'] == 'M2'].copy()
        
        # Get the latest M1 submission
        if not m1_submissions.empty:
            latest_m1 = m1_submissions.iloc[-1]
            
            # Check if M2 has submitted
            if not m2_submissions.empty:
                latest_m2 = m2_submissions.iloc[-1]
                
                # Determine agreement status
                status = self._determine_agreement_status(latest_m1, latest_m2)
                
                # Create record with M2 decision
                record = self._create_record(latest_m1, latest_m2, status)
                results.append(record)
                
            else:
                # M1 submitted, awaiting M2
                record = self._create_record(latest_m1, None, "Awaiting M2")
                results.append(record)
        
        # If no results yet, add individual submissions as records
        if not results:
            for _, row in group.iterrows():
                record = self._create_record(row, None, "Individual Submission")
                results.append(record)
        
        return results
    
    def _determine_agreement_status(self, m1_record: pd.Series, m2_record: pd.Series) -> str:
        """
        Determine if M2 agrees with M1 and derive appropriate status.
        
        Args:
            m1_record: M1 submission record
            m2_record: M2 submission record
            
        Returns:
            str: Status ('Agreed', 'Disagreed', 'Escalated')
        """
        # Check explicit agreement checkbox
        if m2_record['M2_Agree_Checkbox']:
            return "Agreed"
        
        # If not explicitly agreed, check for disagreement indicators
        # M2 providing a different score indicates disagreement
        if pd.notna(m2_record['Score']) and m2_record['Score'] != m1_record['Score']:
            return "Disagreed"
        
        # Check Pass/Fail disagreement
        if (pd.notna(m1_record['PassFail']) and pd.notna(m2_record['PassFail']) and 
            m1_record['PassFail'] != m2_record['PassFail']):
            return "Disagreed"
        
        # If M2 provided extensive feedback without agreeing, might indicate disagreement
        if (pd.notna(m2_record['Feedback']) and len(str(m2_record['Feedback'])) > 100 and
            not m2_record['M2_Agree_Checkbox']):
            return "Disagreed"
        
        # Default to awaiting M2 if unclear
        return "Awaiting M2"
    
    def _create_record(self, m1_record: pd.Series, m2_record: Optional[pd.Series], 
                      status: str) -> Dict:
        """
        Create a processed record with all relevant information.
        
        Args:
            m1_record: M1 submission record
            m2_record: M2 submission record (optional)
            status: Derived workflow status
            
        Returns:
            Dict: Processed record
        """
        # Determine final score and pass/fail based on agreement logic
        final_score = None
        final_passfail = None
        
        if status == "Agreed":
            final_score = m1_record['Score']  # Use M1's score when agreed
            final_passfail = self._determine_pass_fail(final_score)
        elif status == "Disagreed" and m2_record is not None:
            # In disagreement, both scores are retained for M3 review
            final_score = None
            final_passfail = None
        elif status == "Individual Submission":
            final_score = m1_record['Score']
            final_passfail = self._determine_pass_fail(final_score)
        
        # Extract marker assignments from M1's form submission
        m2_assigned_name = m1_record.get('M2_MarkerName', '')
        m2_assigned_email = m1_record.get('M2_MarkerEmail', '')
        m3_assigned_name = m1_record.get('M3_MarkerName', '')
        m3_assigned_email = m1_record.get('M3_MarkerEmail', '')
        
        # Parse dropdown selections if they are in formatted form
        if ' (' in str(m2_assigned_name) and ')' in str(m2_assigned_name):
            # Extract from dropdown format: "Dr. John Smith (john.smith@keele.ac.uk) [DEMO]"
            m2_assigned_name = self._parse_dropdown_name(str(m2_assigned_name))
        if ' (' in str(m3_assigned_name) and ')' in str(m3_assigned_name):
            m3_assigned_name = self._parse_dropdown_name(str(m3_assigned_name))

        record = {
            'StudentID': m1_record['StudentID'],
            'StudentName': m1_record['StudentName'],
            'Status': status,
            'M1_MarkerName': m1_record['MarkerName'],
            'M1_MarkerEmail': m1_record['MarkerEmail'],
            'M1_Score': m1_record['Score'],
            'M1_PassFail': m1_record['PassFail'],
            'M1_Feedback': m1_record['Feedback'],
            'M1_Timestamp': m1_record.get('Timestamp', datetime.now()),
            # M2 assignment from M1's form
            'M2_AssignedName': m2_assigned_name,
            'M2_AssignedEmail': m2_assigned_email,
            # M2 actual response
            'M2_MarkerName': m2_record['MarkerName'] if m2_record is not None else None,
            'M2_MarkerEmail': m2_record['MarkerEmail'] if m2_record is not None else None,
            'M2_Score': m2_record.get('M2_Score') if m2_record is not None else (m2_record['Score'] if m2_record is not None else None),
            'M2_PassFail': m2_record['PassFail'] if m2_record is not None else None,
            'M2_Feedback': m2_record.get('M2_Feedback') if m2_record is not None else (m2_record['Feedback'] if m2_record is not None else None),
            'M2_Timestamp': m2_record.get('Timestamp') if m2_record is not None else None,
            'M2_Agreed': m2_record['M2_Agree_Checkbox'] if m2_record is not None else None,
            # M3 assignment from M1's form
            'M3_AssignedName': m3_assigned_name,
            'M3_AssignedEmail': m3_assigned_email,
            'AI_Feedback': m1_record.get('AI_Feedback_Optional', ''),
            'Final_Score': final_score,
            'Final_PassFail': final_passfail,
            'Requires_Action': status in ['Awaiting M2', 'Disagreed'],
            'Last_Updated': datetime.now()
        }
        
        return record
    
    def _parse_dropdown_name(self, dropdown_selection: str) -> str:
        """
        Parse dropdown selection to extract just the name.
        
        Args:
            dropdown_selection: Full dropdown text like "Dr. John Smith (john.smith@keele.ac.uk) [DEMO]"
            
        Returns:
            str: Just the name part
        """
        try:
            # Remove demo label if present
            clean_selection = dropdown_selection.replace(" [DEMO]", "")
            
            # Extract name: "Dr. John Smith (john.smith@keele.ac.uk)" -> "Dr. John Smith"
            if "(" in clean_selection:
                name = clean_selection.split("(")[0].strip()
                return name
            else:
                return clean_selection.strip()
                
        except Exception:
            return dropdown_selection
    
    def get_pending_notifications(self) -> List[Dict]:
        """
        Get list of submissions requiring notifications.
        
        Returns:
            List[Dict]: Records requiring notifications
        """
        if self.processed_data is None:
            return []
        
        pending = self.processed_data[
            self.processed_data['Status'].isin(['Awaiting M2', 'Disagreed'])
        ].copy()
        
        return pending.to_dict('records')
    
    def get_summary_stats(self) -> Dict:
        """
        Get summary statistics for the dashboard.
        
        Returns:
            Dict: Summary statistics
        """
        if self.processed_data is None:
            return {}
        
        stats = {
            'total_submissions': len(self.processed_data),
            'awaiting_m2': len(self.processed_data[self.processed_data['Status'] == 'Awaiting M2']),
            'agreed': len(self.processed_data[self.processed_data['Status'] == 'Agreed']),
            'disagreed': len(self.processed_data[self.processed_data['Status'] == 'Disagreed']),
            'escalated': len(self.processed_data[self.processed_data['Status'] == 'Escalated']),
            'completed': len(self.processed_data[self.processed_data['Final_Score'].notna()])
        }
        
        return stats