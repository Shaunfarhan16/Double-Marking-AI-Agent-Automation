# Three-Marker Workflow System

## Workflow Overview

The double-marking system operates with **exactly 3 markers** per student assessment:

### 🎯 **Marker Roles:**

**M1 (First Marker):**
- Completes initial assessment and marking
- **Uses Enhanced UI Application to submit:**
  - Student details (ID, name)
  - **M2 marker assignment** (selected from dropdown database)
  - **M3 marker assignment** (selected from dropdown database)
  - Their own score and feedback
- **System automatically:**
  - Populates 36-column Excel workflow
  - Sends M2 email with pre-filled Microsoft Forms URL

**M2 (Second Marker):**
- Receives automated email with **pre-filled Microsoft Forms link**
- Student details already populated in the Forms
- Reviews M1's assessment (pre-filled in Forms)
- **Either:**
  - ✅ **Agrees**: Selects "Yes" in Forms → Process complete
  - ❌ **Disagrees**: Selects "No" and provides different score/feedback → **Automatic M3 escalation**

**M3 (Third Marker/Moderator):**
- **Automatically notified** when M2 disagrees (no manual trigger needed)
- Receives escalation email with **pre-filled Forms URL containing M1+M2 data**
- Reviews both M1 and M2 assessments (pre-filled in Forms)
- Makes final binding decision via Microsoft Forms
- System automatically updates Excel with final results

---

## 📋 **Microsoft Forms Structure**

### Required Fields for M1 to Complete:

```
Student Information:
├── StudentID (text)
├── StudentName (text)

M1 Assessment:
├── MarkerRole = "M1" (choice)
├── MarkerName = M1's name (text)
├── MarkerEmail = M1's email (text)
├── Score (number 0-100)
├── PassFail (choice: Pass/Fail - optional, auto-determined)
├── Feedback (long text)
├── AI_Feedback_Optional (long text - optional)

M2 Assignment:
├── M2_MarkerName (text) ← M1 specifies who M2 will be
├── M2_MarkerEmail (text) ← M1 provides M2's email

M3 Assignment:
├── M3_MarkerName (text) ← M1 specifies who M3 will be  
├── M3_MarkerEmail (text) ← M1 provides M3's email

M2 Response Fields (completed later by M2):
├── M2_Agree_Checkbox (Yes/No)
├── M2_Score (number - optional)
├── M2_Feedback (long text - optional)
```

---

## 🔄 **Automated Email Flow**

### Scenario 1: Agreement (Most Common)
```
1. M1 completes form with student details + assigns M2 & M3
   ↓ IMMEDIATE (< 5 seconds)
2. 📧 M2 receives notification: "Please review Student X assessment"
   ↓ M2 reviews and clicks "I agree with M1's mark"
3. 📧 BOTH M1 & M2 receive: "Marking complete - Final score: X"
   ✅ PROCESS COMPLETE
```

### Scenario 2: Disagreement (Escalation Required)
```
1. M1 completes form with student details + assigns M2 & M3
   ↓ IMMEDIATE (< 5 seconds) 
2. 📧 M2 receives notification: "Please review Student X assessment"
   ↓ M2 disagrees - provides different score/feedback
3. 📧 M1 receives: "M2 disagrees - M3 will make final decision"
4. 📧 M3 receives: "Escalation required - resolve disagreement between M1 & M2"
   ↓ M3 makes final decision
5. 📧 ALL THREE receive: "Final decision by M3 - Score: X"
   ✅ PROCESS COMPLETE
```

---

## 🎓 **Keele University Implementation**

### Marker Email Addresses
All markers use Keele University accounts:
- **M1 Example**: `john.smith@keele.ac.uk`
- **M2 Example**: `jane.doe@keele.ac.uk` 
- **M3 Example**: `moderator@keele.ac.uk`

### Assignment Flexibility
M1 can assign any combination of Keele staff:
```
Example Assignment 1:
M1: john.smith@keele.ac.uk
M2: jane.doe@keele.ac.uk (assigned by M1)
M3: senior.lecturer@keele.ac.uk (assigned by M1)

Example Assignment 2:
M1: lecturer.a@keele.ac.uk  
M2: lecturer.b@keele.ac.uk (assigned by M1)
M3: head.of.department@keele.ac.uk (assigned by M1)
```

---

## 🔧 **System Configuration**

### Updated Forms Parser
The system needs to extract marker assignments from M1's form submission:

```python
# Extract M2 and M3 assignments from M1's form
m2_name = m1_record['M2_MarkerName']
m2_email = m1_record['M2_MarkerEmail'] 
m3_name = m1_record['M3_MarkerName']
m3_email = m1_record['M3_MarkerEmail']

# Send notification to assigned M2
send_m2_notification(student_id, m1_data, m2_email)

# If disagreement, escalate to assigned M3
if disagreement_detected:
    send_escalation_email(student_id, m1_data, m2_data, m3_email)
```

### Email Templates Updated
All email templates reference the assigned markers:

```python
# M2 Notification
subject = f"Double-Marking Required: Student {student_id}"
body = f"""Dear {m2_name},

{m1_name} has completed the initial assessment for Student {student_id}.
You have been assigned as the second marker for this submission.

First Marker's Assessment:
• Marker: {m1_name} ({m1_email})
• Score: {m1_score}
• Feedback: {m1_feedback}

Please complete your review in Microsoft Forms...
"""

# M3 Escalation  
subject = f"ESCALATION: Student {student_id} - Third Marker Required"
body = f"""Dear {m3_name},

A disagreement requires your attention between:
• M1: {m1_name} (Score: {m1_score})
• M2: {m2_name} (Score: {m2_score})

You have been assigned as the third marker to make the final decision...
"""
```

---

## 📊 **Workflow States**

### Status Progression
```
1. "M1 Complete" → M1 submitted, M2 assigned and notified
2. "Awaiting M2" → M2 notification sent, waiting for response  
3. "Agreed" → M2 agreed, process finalized
4. "Disagreed" → M2 disagreed, M3 assigned and notified
5. "Escalated" → M3 notification sent, waiting for resolution
6. "Finalized" → Final decision made, all parties notified
```

### Data Tracking
The system tracks all three marker assignments:
```python
workflow_state = {
    'student_id': 'CS2024001',
    'm1_data': {'name': 'John Smith', 'email': 'john.smith@keele.ac.uk', 'score': 85},
    'm2_data': {'name': 'Jane Doe', 'email': 'jane.doe@keele.ac.uk', 'assigned': True},
    'm3_data': {'name': 'Dr. Wilson', 'email': 'moderator@keele.ac.uk', 'assigned': True},
    'status': 'Awaiting M2',
    'escalation_required': False
}
```

---

## 🧪 **Testing Scenarios**

### Test Case 1: Complete Agreement
```python
# M1 submission
m1_data = {
    'student_id': 'TEST001',
    'marker_name': 'Dr. Smith',
    'marker_email': 'smith@keele.ac.uk',
    'score': 75,
    'm2_name': 'Dr. Jones', 
    'm2_email': 'jones@keele.ac.uk',
    'm3_name': 'Prof. Wilson',
    'm3_email': 'wilson@keele.ac.uk'
}

# Expected: M2 gets notification, agrees, process complete
```

### Test Case 2: Disagreement & Escalation
```python
# M1 submission (same as above)
# M2 disagrees with different score
m2_data = {
    'agreed': False,
    'score': 65,  # Different from M1's 75
    'feedback': 'Needs improvement in X area'
}

# Expected: M1 notified, M3 gets escalation email
```

---

## 🎯 **Key Benefits**

**✅ Flexible Assignment**: M1 chooses appropriate M2 and M3 for each assessment
**✅ Automated Routing**: System knows exactly who to notify at each stage  
**✅ Role Clarity**: Each marker knows their role and responsibilities
**✅ Complete Tracking**: Full audit trail of all three marker interactions
**✅ Efficient Escalation**: Only M3 gets involved when needed
**✅ Keele Integration**: Works seamlessly with university email system

---

**This three-marker system ensures thorough assessment while minimizing unnecessary involvement through intelligent automation.** 🎓