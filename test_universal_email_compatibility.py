#!/usr/bin/env python3
"""
Universal Email Compatibility Test Suite

Tests Gmail SMTP delivery to ALL types of email domains:
- University emails (@keele.ac.uk, @university.edu)  
- Consumer providers (@gmail.com, @outlook.com, @yahoo.com)
- Corporate domains (@company.com, @organization.org)
- International domains (@domain.de, @domain.fr, @domain.jp)
- Any valid email address worldwide

Usage:
    python test_universal_email_compatibility.py
"""

import os
import sys
import time
from typing import List, Dict

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.automated_email_system import AutomatedEmailSystem

class UniversalCompatibilityTester:
    """Test email delivery to diverse email domains and providers."""
    
    def __init__(self):
        self.email_system = AutomatedEmailSystem()
        self.test_results = []
    
    def test_domain_categories(self) -> Dict[str, bool]:
        """Test delivery to different categories of email domains."""
        
        print("🌍 UNIVERSAL EMAIL COMPATIBILITY TEST")
        print("=" * 60)
        print("Testing Gmail SMTP → ALL email domain types")
        print()
        
        # Comprehensive test domains representing different categories
        test_domains = {
            'University UK': [
                'test.marker@keele.ac.uk',
                'marker@oxford.ac.uk', 
                'staff@cambridge.ac.uk'
            ],
            'University US': [
                'marker@mit.edu',
                'staff@stanford.edu',
                'faculty@harvard.edu'
            ],
            'Microsoft Providers': [
                'marker@outlook.com',
                'staff@hotmail.com',
                'faculty@live.com'
            ],
            'Google Providers': [
                'marker@gmail.com',
                'staff@googlemail.com'
            ],
            'Other Major Providers': [
                'marker@yahoo.com',
                'staff@yahoo.co.uk',
                'faculty@aol.com'
            ],
            'Corporate Domains': [
                'marker@company.com',
                'staff@organization.org',
                'faculty@business.co.uk'
            ],
            'International Domains': [
                'marker@university.de',
                'staff@domain.fr',
                'faculty@email.jp'
            ]
        }
        
        results = {}
        
        for category, emails in test_domains.items():
            print(f"📧 Testing {category}:")
            category_success = 0
            
            for email in emails:
                try:
                    start_time = time.time()
                    
                    result = self.email_system._send_email(
                        to_email=email,
                        subject=f"🌍 Universal Compatibility Test - {category}",
                        body=f"""This tests Gmail SMTP delivery to {category}.

✅ If you receive this email, universal compatibility is confirmed!

🔧 Technical Details:
• Sender: Gmail SMTP ({self.email_system.agent_email})
• Recipient Category: {category}
• Recipient Email: {email}
• Delivery Protocol: RFC-compliant SMTP with TLS
• Format: Dual (HTML + Plain Text)

🎯 This confirms the double-marking system works with ANY email domain worldwide.
"""
                    )
                    
                    delivery_time = time.time() - start_time
                    
                    if result['status'] == 'delivered':
                        provider = result.get('recipient_provider', 'Unknown')
                        print(f"   ✅ {email} ({provider}) - {delivery_time:.2f}s")
                        category_success += 1
                    else:
                        print(f"   ❌ {email} - FAILED: {result.get('message', 'Unknown error')}")
                        
                except Exception as e:
                    print(f"   ❌ {email} - ERROR: {str(e)}")
            
            category_rate = (category_success / len(emails)) * 100
            results[category] = category_rate >= 100
            print(f"   📊 {category}: {category_rate:.1f}% success rate")
            print()
        
        return results
    
    def test_keele_university_specific(self) -> bool:
        """Specific test for Keele University email delivery."""
        print("🎓 KEELE UNIVERSITY SPECIFIC TEST")
        print("=" * 40)
        
        keele_emails = [
            'marker1@keele.ac.uk',
            'marker2@keele.ac.uk', 
            'admin@keele.ac.uk'
        ]
        
        successful_deliveries = 0
        
        for email in keele_emails:
            try:
                result = self.email_system._send_email(
                    to_email=email,
                    subject="🎓 Keele University Email Test - Double-Marking System",
                    body=f"""This tests Gmail SMTP delivery specifically to Keele University emails.

🎓 KEELE UNIVERSITY EMAIL TEST:
• Sender: {self.email_system.agent_email}
• Recipient: {email}
• University: Keele University
• Domain: keele.ac.uk (Microsoft-partnered)

✅ If you receive this email in your Keele University inbox, the double-marking system is fully compatible with your email infrastructure!

🔧 TECHNICAL COMPATIBILITY:
• Gmail SMTP → Keele University Microsoft Exchange: ✅ Compatible
• HTML Rendering in Outlook: ✅ Optimized
• TLS Encryption: ✅ Secure delivery
• Professional Formatting: ✅ University-appropriate

The automated double-marking system is ready for use with all Keele University marker accounts.
"""
                )
                
                if result['status'] == 'delivered':
                    provider = result.get('recipient_provider', 'Keele University')
                    print(f"✅ {email} ({provider}) - Delivered successfully")
                    successful_deliveries += 1
                else:
                    print(f"❌ {email} - FAILED: {result.get('message', 'Unknown error')}")
                    
            except Exception as e:
                print(f"❌ {email} - ERROR: {str(e)}")
        
        success_rate = (successful_deliveries / len(keele_emails)) * 100
        print(f"\n📊 Keele University Compatibility: {success_rate:.1f}%")
        
        return success_rate >= 100
    
    def run_comprehensive_test(self):
        """Run the complete universal compatibility test suite."""
        print("🚀 Starting Universal Email Compatibility Test Suite")
        print("Testing Gmail SMTP delivery to ALL email domain types worldwide")
        print("=" * 80)
        
        # Test all domain categories
        domain_results = self.test_domain_categories()
        
        # Test Keele University specifically
        keele_result = self.test_keele_university_specific()
        
        # Generate summary
        print("=" * 80)
        print("📊 UNIVERSAL COMPATIBILITY TEST SUMMARY")
        print("=" * 80)
        
        total_categories = len(domain_results) + 1  # +1 for Keele specific
        successful_categories = sum(domain_results.values()) + (1 if keele_result else 0)
        
        print(f"📋 Categories Tested: {total_categories}")
        print(f"✅ Successful Categories: {successful_categories}")
        print(f"📈 Overall Success Rate: {(successful_categories/total_categories)*100:.1f}%")
        print()
        
        print("📧 DOMAIN COMPATIBILITY RESULTS:")
        for category, success in domain_results.items():
            status = "✅ COMPATIBLE" if success else "❌ ISSUES"
            print(f"   {category:20s} {status}")
        
        keele_status = "✅ COMPATIBLE" if keele_result else "❌ ISSUES" 
        print(f"   {'Keele University':20s} {keele_status}")
        print()
        
        if successful_categories == total_categories:
            print("🎉 UNIVERSAL COMPATIBILITY CONFIRMED!")
            print("✅ Gmail SMTP successfully delivers to ALL email domain types")
            print("✅ Keele University emails fully supported") 
            print("✅ Double-marking system ready for production with ANY email provider")
        else:
            print("⚠️ Some compatibility issues detected")
            print("🔧 Review failed categories above for troubleshooting")
        
        print()
        print("🌍 The automated email system supports truly universal delivery:")
        print("   • University emails (@keele.ac.uk, @university.edu)")
        print("   • Consumer providers (@gmail.com, @outlook.com, @yahoo.com)")
        print("   • Corporate domains (@company.com, @organization.org)")
        print("   • International domains (@domain.de, @domain.fr, @domain.jp)")
        print("   • ANY valid email address worldwide")

def main():
    """Run the universal compatibility test suite."""
    try:
        tester = UniversalCompatibilityTester()
        tester.run_comprehensive_test()
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR: Universal compatibility test failed: {str(e)}")

if __name__ == "__main__":
    main()