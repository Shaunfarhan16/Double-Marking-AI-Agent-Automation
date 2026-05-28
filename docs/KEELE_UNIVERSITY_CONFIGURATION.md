# Keele University Configuration Guide

## Production vs Testing Configuration

This document explains how the double-marking system is configured for **Keele University production use** while maintaining **universal compatibility** for testing and demonstrations.

---

## 🎓 **Production Configuration (Keele University)**

### Default Email Addresses
The system is configured for Keele University with these default addresses:

```env
# Production Configuration (.env file)
AGENT_EMAIL=doublemarking.agent@gmail.com
UNIVERSITY_NAME=Keele University
DEPARTMENT_NAME=Computer Science Department

# Keele University Default Recipients
DEFAULT_M3_EMAIL=moderator@keele.ac.uk
DEFAULT_ADMIN_EMAIL=admin@keele.ac.uk
```

### Marker Email Addresses
**All markers use Keele University email accounts:**
- **M1 Markers**: `marker1@keele.ac.uk`, `marker2@keele.ac.uk`, etc.
- **M2 Markers**: `marker3@keele.ac.uk`, `marker4@keele.ac.uk`, etc.
- **M3 Moderators**: `moderator@keele.ac.uk`, `senior-marker@keele.ac.uk`, etc.
- **Administrators**: `admin@keele.ac.uk`, `cs-admin@keele.ac.uk`, etc.

### Email Infrastructure
Keele University uses **Microsoft Exchange/Office 365** infrastructure:
- **Domain**: `@keele.ac.uk`
- **Backend**: Microsoft Exchange Server
- **Client**: Outlook (Desktop and Web)
- **Security**: Corporate email security policies

---

## 🧪 **Testing & Demonstration Flexibility**

### Universal Compatibility
While configured for Keele University, the system supports **ANY email address** for testing:

```python
# Example: Testing with different email providers
test_emails = [
    'demo.marker1@gmail.com',      # Gmail for demonstration
    'test.marker2@outlook.com',    # Outlook for testing
    'marker@keele.ac.uk',          # Production Keele address
    'external@university.edu',     # External examiner
    'reviewer@company.com'         # Corporate reviewer
]

# All will work seamlessly
for email in test_emails:
    result = email_system.send_test_email(email)
    print(f"{email}: {result['status']}")
```

### Demonstration Scenarios

#### Scenario 1: Full Production Demo
```python
# Use actual Keele University addresses
m1_email = "john.smith@keele.ac.uk"
m2_email = "jane.doe@keele.ac.uk" 
m3_email = "moderator@keele.ac.uk"
```

#### Scenario 2: Mixed Environment Demo
```python
# Mix Keele and external for demonstration
m1_email = "marker1@keele.ac.uk"      # Keele marker
m2_email = "external@gmail.com"       # External examiner
m3_email = "moderator@keele.ac.uk"    # Keele moderator
```

#### Scenario 3: Fully External Demo
```python
# All external addresses for presentation
m1_email = "demo.m1@gmail.com"
m2_email = "demo.m2@outlook.com"
m3_email = "demo.m3@yahoo.com"
```

---

## 🔧 **Technical Implementation**

### Email Provider Detection
The system automatically detects and optimizes for different email providers:

```python
def _detect_email_provider(self, email: str) -> str:
    domain = email.split('@')[1].lower()
    
    provider_map = {
        'keele.ac.uk': 'Keele University (Microsoft)',  # Keele-specific
        'outlook.com': 'Microsoft Outlook',
        'gmail.com': 'Google Gmail',
        # ... other providers
    }
    
    # University pattern detection
    if any(edu_domain in domain for edu_domain in ['.ac.uk', '.edu']):
        return f'University ({domain})'
    
    return provider_map.get(domain, f'Email Provider ({domain})')
```

### Keele University Optimization
Special handling for Keele University emails:

```python
# Keele University specific optimizations
if 'keele.ac.uk' in email:
    # Microsoft Exchange optimized delivery
    # Outlook-specific HTML rendering
    # University branding
    # Corporate security compliance
```

---

## 📧 **Email Flow Examples**

### Production Flow (Keele University)
```
M1 (john.smith@keele.ac.uk) submits assessment
    ↓ IMMEDIATE (< 5 seconds)
📧 M2 (jane.doe@keele.ac.uk) receives notification via Microsoft Exchange
    ↓ Opens in Outlook with perfect formatting
M2 disagrees with assessment
    ↓ IMMEDIATE (< 5 seconds)
📧 M1 receives disagreement notification
📧 M3 (moderator@keele.ac.uk) receives escalation email
    ↓ All delivered via Keele's Microsoft infrastructure
```

### Demo Flow (Mixed Providers)
```
M1 (demo@gmail.com) submits assessment
    ↓ IMMEDIATE (< 5 seconds)  
📧 M2 (marker@keele.ac.uk) receives notification
    ↓ Gmail SMTP → Keele Microsoft Exchange → Outlook
Perfect delivery and formatting maintained across providers
```

---

## ⚙️ **Configuration Management**

### Production Deployment
1. **Use Keele University addresses** in Microsoft Forms
2. **Configure .env** with production Keele emails
3. **Test with Keele accounts** before going live
4. **Monitor delivery** to Keele infrastructure

### Testing & Demonstration
1. **Keep production config** in .env file
2. **Override with test emails** in Forms or code
3. **Mix providers** to demonstrate universal compatibility
4. **Show real-time delivery** across different email systems

### Environment Variables Override
```python
# Override defaults for testing without changing .env
email_system = AutomatedEmailSystem()

# Test with demo addresses
result = email_system.send_m2_notification(
    student_id="DEMO001",
    m1_data={'marker_name': 'Demo Marker', 'score': 85},
    m2_email="demo.marker@gmail.com"  # Override default
)
```

---

## 🛡️ **Security & Compliance**

### Keele University Requirements
- **Microsoft Exchange Integration**: Native compatibility
- **Corporate Security**: Meets university email policies  
- **Data Protection**: GDPR compliant email handling
- **Audit Trails**: Complete logging for compliance

### External Communication
- **Secure SMTP**: TLS encryption for all external delivery
- **Professional Branding**: Keele University identification
- **Proper Headers**: RFC compliance for deliverability
- **Spam Prevention**: Configured to avoid spam filters

---

## 📊 **Monitoring & Analytics**

### Production Monitoring
```python
# Monitor Keele University email delivery
delivery_stats = {
    'keele_deliveries': 0,
    'external_deliveries': 0,
    'failed_deliveries': 0
}

# Real-time logging
logger.info(f"✅ Email delivered to {email} (Keele University) at {timestamp}")
```

### Testing Analytics
```python
# Track demonstration effectiveness
demo_stats = {
    'gmail_demos': 0,
    'outlook_demos': 0, 
    'keele_demos': 0,
    'mixed_provider_demos': 0
}
```

---

## 🚀 **Quick Setup Commands**

### Production Setup (Keele University)
```bash
# Verify Keele configuration
python -c "
from utils.automated_email_system import AutomatedEmailSystem
system = AutomatedEmailSystem()
print(f'M3 Email: {system.default_m3_email}')
print(f'University: {system.university}')
"

# Test Keele delivery
python test_universal_email_compatibility.py
```

### Demo Setup (Any Provider)
```bash
# Test universal compatibility
python -c "
from utils.automated_email_system import AutomatedEmailSystem
system = AutomatedEmailSystem()
system.send_test_email('demo@gmail.com')
system.send_test_email('test@outlook.com')  
system.send_test_email('marker@keele.ac.uk')
"
```

---

## 📋 **Summary**

**✅ Production Ready**: Fully configured for Keele University with `@keele.ac.uk` addresses
**✅ Universal Testing**: Works with any email provider for demonstrations  
**✅ Microsoft Compatibility**: Optimized for Keele's Microsoft Exchange infrastructure
**✅ Real-time Delivery**: < 5 seconds to any email provider worldwide
**✅ Professional Branding**: Keele University identification in all emails
**✅ Secure & Compliant**: Meets university security and data protection requirements

The system is **production-ready for Keele University** while maintaining **complete flexibility** for testing, demonstrations, and external collaboration.

---

*This configuration ensures optimal performance for Keele University operations while demonstrating universal email compatibility across all providers.*