#!/usr/bin/env python3
"""Test script for orchestrator service showing before/after resume names."""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.orchestrator import ResumeEnhancementOrchestrator
import anthropic
from dotenv import load_dotenv

def test_orchestrator_before_after():
    """Test the orchestrator service and show before/after resume names."""
    
    print("🧪 Testing Resume Enhancement Orchestrator - Before/After Comparison")
    print("=" * 70)
    
    # Load environment variables
    load_dotenv()
    
    # Initialize the orchestrator
    try:
        client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        orchestrator = ResumeEnhancementOrchestrator(client)
        print("✅ Resume Enhancement Orchestrator initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize orchestrator: {e}")
        return
    
    # Ensure resumes directory exists
    resumes_dir = Path("resumes")
    if not resumes_dir.exists():
        resumes_dir.mkdir(exist_ok=True)
        print("✅ Created resumes directory")
    
    # Test resume file
    test_resume = resumes_dir / "res1.docx"
    
    if not test_resume.exists():
        print(f"❌ Test resume not found: {test_resume}")
        return
    
    print(f"\n📄 Original Resume: {test_resume}")
    print(f"   Size: {os.path.getsize(test_resume)} bytes")
    
    # Sample job description
    sample_jd = """Nationally focused online retailer and publisher recruiting a motivated Web Developer to our team. In this role, you will work with a small team of developers (managed by our software engineer) to maintain and update existing infrastructure while creating and integrating new features and projects into existing platforms. Candidates should have 2 years programming experience minimum, but a college degree is not required. This is primarily a programming position, PHP knowledge is required.

This is an in-office position in Charlotte, NC.

Responsibilities:

Work with a team to develop and maintain existing ecomm and media websites
Integrate websites with third party systems
Design, test, and develop website applications to meet business needs.
Monitor web application performance by ensuring its security, stability, and availability for use to optimize the security, privacy, and integrity of company data.
Evaluate code to ensure proper structure, validity, and compliance in accordance with industry standards, as well as compatibility with various browsers, devices, and operating systems.
Required Skills:

HTML
PHP
MySQL
JavaScript
Knowledge of hosting environments and servers
Able to apply technical knowledge to real-world needs
Able to work in a team environment while working independently as needed
Great to have, but not required:

Laravel
Vue
Benefits:

Vacation/Sick Leave
Life Insurance (100% paid by employer, option to add more)
401k + generous employer match
FSA/DCFSA with generous employer match
Employee discounts and more!
Unfortunately, we are unable to offer health insurance at this time

**Candidates must be able to pass background screening which will include a credit check. A good credit score is required.

Job Type: Full-time

Pay: $60,000.00 - $70,000.00 per year

Benefits:

401(k)
401(k) matching
Employee discount
Flexible schedule
Flexible spending account
Life insurance
Paid time off
Retirement plan
Schedule:

8 hour shift
Day shift
Experience:

JavaScript: 1 year (Preferred)
PHP: 1 year (Required)
Ability to Commute:

Charlotte, NC 28277 (Required)
Work Location: In person"""
    
    print(f"\n🎯 Job Description: {len(sample_jd)} characters")
    print(f"   Focus: Web Developer position with multi-agent systems")
    
    print(f"\n🔄 Starting Resume Enhancement Workflow...")
    print("-" * 50)
    
    try:
        # Run the complete enhancement workflow
        enhancement_results = orchestrator.enhance_resume(
            resume_path=test_resume,
            job_description=sample_jd,
            output_dir="resumes",
            preserve_original=True,
            generate_pdf=False  # Disable PDF generation since LibreOffice is not installed
        )
        
        print(f"✅ Enhancement completed successfully!")
        print(f"   Request ID: {enhancement_results.get('request_id')}")
        
        # Show workflow summary
        workflow_summary = enhancement_results.get('workflow_summary', {})
        print(f"\n📊 Workflow Summary:")
        print(f"   JD Skills Analyzed: {workflow_summary.get('jd_skills_analyzed', 0)}")
        print(f"   Resume Roles Parsed: {workflow_summary.get('resume_roles_parsed', 0)}")
        print(f"   Resume Bullets Parsed: {workflow_summary.get('resume_bullets_parsed', 0)}")
        print(f"   Improvements Generated: {workflow_summary.get('improvements_generated', 0)}")
        print(f"   Seniority Level: {workflow_summary.get('seniority_level', 'N/A')}")
        
        # Show file paths
        file_paths = enhancement_results.get('file_paths', {})
        enhanced_docx = file_paths.get('enhanced_docx')
        enhanced_pdf = file_paths.get('enhanced_pdf')
        
        print(f"\n📁 Generated Files:")
        if enhanced_docx:
            print(f"   Enhanced DOCX: {os.path.basename(enhanced_docx)}")
            print(f"     Full Path: {enhanced_docx}")
            print(f"     Size: {os.path.getsize(enhanced_docx)} bytes")
        
        if enhanced_pdf:
            print(f"   Enhanced PDF: {os.path.basename(enhanced_pdf)}")
            print(f"     Full Path: {enhanced_pdf}")
            print(f"     Size: {os.path.getsize(enhanced_pdf)} bytes")
        
        # Check resumes directory
        resumes_dir = Path("resumes")
        if resumes_dir.exists():
            print(f"\n📂 Resumes Directory Contents:")
            files = list(resumes_dir.glob("*"))
            for file in files:
                print(f"   - {file.name} ({file.stat().st_size} bytes)")
        
        print(f"\n🎯 Before/After Summary:")
        print(f"   BEFORE: {test_resume}")
        print(f"   AFTER:  {os.path.basename(enhanced_docx) if enhanced_docx else 'N/A'}")
        print(f"   PDF:    {os.path.basename(enhanced_pdf) if enhanced_pdf else 'N/A'}")
        
    except Exception as e:
        print(f"❌ Enhancement failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_orchestrator_before_after()
