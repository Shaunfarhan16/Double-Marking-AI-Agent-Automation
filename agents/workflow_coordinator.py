from typing import Dict, List, Optional, Any, TypedDict
from datetime import datetime
import pandas as pd
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkflowState(TypedDict):
    """State object that gets passed between workflow nodes."""
    student_id: str
    action: str
    forms_data: pd.DataFrame
    current_status: str
    m1_data: Optional[Dict]
    m2_data: Optional[Dict]
    m3_data: Optional[Dict]
    notification_sent: bool
    escalation_required: bool
    final_score: Optional[float]
    messages: List[str]
    error: Optional[str]

class WorkflowCoordinator:
    """
    Coordinates the double-marking workflow using LangGraph agents.
    Handles marker handovers, agreement tracking, and escalation logic.
    """
    
    def __init__(self):
        self.workflow_graph = self._build_workflow_graph()
        self.outlook_automation = None
        self._initialize_outlook()
    
    def _initialize_outlook(self):
        """Initialize automated email system."""
        try:
            from utils.automated_email_system import AutomatedEmailSystem
            self.outlook_automation = AutomatedEmailSystem()
            logger.info("Automated email system initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize automated email system: {str(e)}")
            self.outlook_automation = None
    
    def _build_workflow_graph(self) -> StateGraph:
        """Build the LangGraph workflow for double-marking process."""
        workflow = StateGraph(WorkflowState)
        
        # Add nodes for different workflow steps
        workflow.add_node("intake", self._intake_node)
        workflow.add_node("handoff", self._handoff_node)
        workflow.add_node("agreement_check", self._agreement_check_node)
        workflow.add_node("escalation", self._escalation_node)
        workflow.add_node("finalization", self._finalization_node)
        workflow.add_node("notification", self._notification_node)
        
        # Define workflow edges
        workflow.set_entry_point("intake")
        
        workflow.add_edge("intake", "handoff")
        workflow.add_conditional_edges(
            "handoff",
            self._handoff_router,
            {
                "agreement_check": "agreement_check",
                "notification": "notification",
                "end": END
            }
        )
        
        workflow.add_conditional_edges(
            "agreement_check",
            self._agreement_router,
            {
                "finalization": "finalization",
                "escalation": "escalation",
                "notification": "notification"
            }
        )
        
        workflow.add_edge("escalation", "notification")
        workflow.add_edge("finalization", "notification")
        workflow.add_edge("notification", END)
        
        return workflow.compile()
    
    def _intake_node(self, state: WorkflowState) -> WorkflowState:
        """
        Initial intake node - analyzes current submission status.
        """
        logger.info(f"Processing intake for student {state['student_id']}")
        
        try:
            # Find student data in forms
            student_data = state['forms_data'][
                state['forms_data']['StudentID'] == state['student_id']
            ]
            
            if student_data.empty:
                state['error'] = f"No data found for student {state['student_id']}"
                return state
            
            # Get latest status
            latest_record = student_data.iloc[-1]
            state['current_status'] = latest_record.get('Status', 'Unknown')
            
            # Extract M1 data and assigned marker information
            state['m1_data'] = {
                'marker_name': latest_record.get('M1_MarkerName'),
                'marker_email': latest_record.get('M1_MarkerEmail'),
                'score': latest_record.get('M1_Score'),
                'passfail': latest_record.get('M1_PassFail'),
                'feedback': latest_record.get('M1_Feedback')
            } if latest_record.get('M1_MarkerName') else None
            
            # M2 assignment (from M1's form) and actual response data
            m2_assigned_name = latest_record.get('M2_AssignedName')
            m2_assigned_email = latest_record.get('M2_AssignedEmail')
            
            state['m2_data'] = {
                'assigned_name': m2_assigned_name,
                'assigned_email': m2_assigned_email,
                'marker_name': latest_record.get('M2_MarkerName'),
                'marker_email': latest_record.get('M2_MarkerEmail'),
                'score': latest_record.get('M2_Score'),
                'passfail': latest_record.get('M2_PassFail'),
                'feedback': latest_record.get('M2_Feedback'),
                'agreed': latest_record.get('M2_Agreed')
            } if m2_assigned_name or latest_record.get('M2_MarkerName') else None
            
            # M3 assignment (from M1's form)
            state['m3_data'] = {
                'assigned_name': latest_record.get('M3_AssignedName'),
                'assigned_email': latest_record.get('M3_AssignedEmail')
            } if latest_record.get('M3_AssignedName') else None
            
            state['messages'].append(f"Intake completed for student {state['student_id']}")
            logger.info(f"Intake completed. Current status: {state['current_status']}")
            
        except Exception as e:
            state['error'] = f"Intake error: {str(e)}"
            logger.error(f"Intake error: {str(e)}")
        
        return state
    
    def _handoff_node(self, state: WorkflowState) -> WorkflowState:
        """
        Handoff node - manages marker transitions.
        """
        logger.info(f"Processing handoff for student {state['student_id']}")
        
        try:
            if state['action'] == "Send M2 Notification" and state['m1_data']:
                # M1 has submitted, notify M2
                state['notification_sent'] = False  # Will be handled by notification node
                state['messages'].append("M2 notification prepared")
                
            elif state['action'] == "Process Agreement" and state['m2_data']:
                # M2 has submitted, check agreement
                state['messages'].append("Agreement check prepared")
                
            elif state['action'] == "Escalate to M3":
                state['escalation_required'] = True
                state['messages'].append("Escalation prepared")
                
            elif state['action'] == "Finalize Mark":
                state['messages'].append("Finalization prepared")
            
            logger.info(f"Handoff completed for action: {state['action']}")
            
        except Exception as e:
            state['error'] = f"Handoff error: {str(e)}"
            logger.error(f"Handoff error: {str(e)}")
        
        return state
    
    def _agreement_check_node(self, state: WorkflowState) -> WorkflowState:
        """
        Agreement check node - determines if M2 agrees with M1.
        """
        logger.info(f"Checking agreement for student {state['student_id']}")
        
        try:
            if not state['m2_data']:
                state['error'] = "No M2 data available for agreement check"
                return state
            
            # Check explicit agreement
            if state['m2_data'].get('agreed') is True:
                state['final_score'] = state['m1_data']['score']
                state['messages'].append("M2 explicitly agreed with M1")
                logger.info("M2 explicitly agreed")
                
            # Check for disagreement indicators
            elif (state['m2_data'].get('score') is not None and 
                  state['m2_data']['score'] != state['m1_data']['score']):
                state['escalation_required'] = True
                state['messages'].append("Score disagreement detected")
                logger.info("Score disagreement detected")
                
            elif (state['m2_data'].get('passfail') != state['m1_data'].get('passfail')):
                state['escalation_required'] = True
                state['messages'].append("Pass/Fail disagreement detected")
                logger.info("Pass/Fail disagreement detected")
                
            else:
                # Default to agreement if no clear disagreement
                state['final_score'] = state['m1_data']['score']
                state['messages'].append("No disagreement detected, using M1 score")
                logger.info("Default agreement - using M1 score")
            
        except Exception as e:
            state['error'] = f"Agreement check error: {str(e)}"
            logger.error(f"Agreement check error: {str(e)}")
        
        return state
    
    def _escalation_node(self, state: WorkflowState) -> WorkflowState:
        """
        Escalation node - prepares third marker notification.
        """
        logger.info(f"Processing escalation for student {state['student_id']}")
        
        try:
            state['escalation_required'] = True
            state['messages'].append(
                f"Escalation required for student {state['student_id']} due to marker disagreement"
            )
            logger.info("Escalation prepared")
            
        except Exception as e:
            state['error'] = f"Escalation error: {str(e)}"
            logger.error(f"Escalation error: {str(e)}")
        
        return state
    
    def _finalization_node(self, state: WorkflowState) -> WorkflowState:
        """
        Finalization node - finalizes agreed marks.
        """
        logger.info(f"Finalizing mark for student {state['student_id']}")
        
        try:
            if state['final_score'] is not None:
                state['messages'].append(
                    f"Final score set to {state['final_score']} for student {state['student_id']}"
                )
                logger.info(f"Mark finalized: {state['final_score']}")
            else:
                state['error'] = "Cannot finalize: no final score determined"
            
        except Exception as e:
            state['error'] = f"Finalization error: {str(e)}"
            logger.error(f"Finalization error: {str(e)}")
        
        return state
    
    def _notification_node(self, state: WorkflowState) -> WorkflowState:
        """
        Notification node - sends appropriate email notifications.
        """
        logger.info(f"Sending notifications for student {state['student_id']}")
        
        try:
            if self.outlook_automation is None:
                state['messages'].append("Automated email system not available - skipping email")
                logger.warning("Automated email system not available")
                return state
            
            if state['escalation_required']:
                logger.info(f"⚠️ Processing disagreement escalation for student {state['student_id']}")
                
                # First, notify M1 about the disagreement - REAL-TIME DELIVERY
                logger.info(f"📧 Sending M1 disagreement notification...")
                m1_result = self.outlook_automation.send_m1_disagreement_notification(
                    student_id=state['student_id'],
                    m1_data=state['m1_data'],
                    m2_data=state['m2_data']
                )
                
                if m1_result['status'] == 'delivered':
                    state['messages'].append(f"✅ M1 disagreement notification delivered to {state['m1_data'].get('marker_email', 'N/A')}")
                    logger.info(f"✅ M1 notification delivered successfully")
                else:
                    state['messages'].append(f"❌ M1 notification failed: {m1_result.get('message', 'Unknown error')}")
                    logger.error(f"❌ M1 notification failed: {m1_result}")
                
                # Then, send escalation email to assigned M3 - REAL-TIME DELIVERY
                m3_email = state['m3_data'].get('assigned_email') if state['m3_data'] else None
                logger.info(f"📧 Sending M3 escalation email to {m3_email}...")
                escalation_result = self.outlook_automation.send_escalation_email(
                    student_id=state['student_id'],
                    m1_data=state['m1_data'],
                    m2_data=state['m2_data'],
                    m3_email=m3_email
                )
                
                if escalation_result['status'] == 'delivered':
                    state['messages'].append(f"✅ M3 escalation email delivered - both assessments provided")
                    logger.info(f"✅ M3 escalation email delivered successfully")
                else:
                    state['messages'].append(f"❌ M3 escalation failed: {escalation_result.get('message', 'Unknown error')}")
                    logger.error(f"❌ M3 escalation failed: {escalation_result}")
                
            elif state['current_status'] == "Awaiting M2" and state['m1_data'] and state['m2_data']:
                # Send M2 notification - REAL-TIME DELIVERY to assigned M2
                m2_email = state['m2_data'].get('assigned_email') or state['m2_data'].get('marker_email')
                logger.info(f"📧 Sending M2 notification for student {state['student_id']} to {m2_email}")
                
                result = self.outlook_automation.send_m2_notification(
                    student_id=state['student_id'],
                    m1_data=state['m1_data'],
                    m2_email=m2_email
                )
                
                if result['status'] == 'delivered':
                    state['messages'].append(f"✅ M2 notification delivered to {m2_email}")
                    logger.info(f"✅ M2 notification delivered successfully")
                else:
                    state['messages'].append(f"❌ M2 notification failed: {result.get('message', 'Unknown error')}")
                    logger.error(f"❌ M2 notification failed: {result}")
                
            elif state['final_score'] is not None:
                # Send finalization confirmation - REAL-TIME DELIVERY
                logger.info(f"📧 Sending finalization email for student {state['student_id']}")
                result = self.outlook_automation.send_finalization_email(
                    student_id=state['student_id'],
                    final_score=state['final_score'],
                    m1_email=state['m1_data']['marker_email'],
                    m2_email=state['m2_data']['marker_email'] if state['m2_data'] else None
                )
                
                if result['status'] == 'delivered':
                    state['messages'].append(f"✅ Finalization email delivered - final score: {state['final_score']}")
                    logger.info(f"✅ Finalization email delivered successfully")
                else:
                    state['messages'].append(f"❌ Finalization email failed: {result.get('message', 'Unknown error')}")
                    logger.error(f"❌ Finalization email failed: {result}")
            
            state['notification_sent'] = True
            logger.info("Notifications sent successfully")
            
        except Exception as e:
            state['error'] = f"Notification error: {str(e)}"
            logger.error(f"Notification error: {str(e)}")
        
        return state
    
    def _handoff_router(self, state: WorkflowState) -> str:
        """Route decision after handoff node."""
        if state.get('error'):
            return "end"
        elif state['action'] == "Process Agreement":
            return "agreement_check"
        else:
            return "notification"
    
    def _agreement_router(self, state: WorkflowState) -> str:
        """Route decision after agreement check."""
        if state.get('error'):
            return "notification"
        elif state.get('escalation_required'):
            return "escalation"
        else:
            return "finalization"
    
    def process_action(self, student_id: str, action: str, forms_data: pd.DataFrame) -> str:
        """
        Process a single workflow action for a student.
        
        Args:
            student_id: Student identifier
            action: Action to perform
            forms_data: Current forms data
            
        Returns:
            str: Result message
        """
        initial_state = WorkflowState(
            student_id=student_id,
            action=action,
            forms_data=forms_data,
            current_status="",
            m1_data=None,
            m2_data=None,
            m3_data=None,
            notification_sent=False,
            escalation_required=False,
            final_score=None,
            messages=[],
            error=None
        )
        
        try:
            # Run the workflow
            final_state = self.workflow_graph.invoke(initial_state)
            
            if final_state.get('error'):
                return f"Error: {final_state['error']}"
            
            return ". ".join(final_state.get('messages', ['Action completed']))
            
        except Exception as e:
            logger.error(f"Workflow execution error: {str(e)}")
            return f"Workflow error: {str(e)}"
    
    def process_all_pending(self, forms_data: pd.DataFrame) -> List[Dict]:
        """
        Process all pending submissions automatically.
        
        Args:
            forms_data: Current forms data
            
        Returns:
            List[Dict]: Results for each processed submission
        """
        results = []
        
        try:
            # Find all submissions requiring action
            pending = forms_data[forms_data['Requires_Action'] == True]
            
            for _, row in pending.iterrows():
                student_id = row['StudentID']
                status = row['Status']
                
                # Determine appropriate action based on status
                if status == "Awaiting M2":
                    action = "Send M2 Notification"
                elif status == "Disagreed":
                    action = "Escalate to M3"
                else:
                    continue
                
                # Process the action
                result_message = self.process_action(student_id, action, forms_data)
                
                results.append({
                    'student_id': student_id,
                    'action': action,
                    'status': 'success' if not result_message.startswith('Error') else 'error',
                    'message': result_message
                })
                
        except Exception as e:
            results.append({
                'student_id': 'all',
                'action': 'process_all_pending',
                'status': 'error',
                'message': f"Batch processing error: {str(e)}"
            })
        
        return results