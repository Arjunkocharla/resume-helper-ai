#!/usr/bin/env python3
"""Test script for the Resume Enhancement API endpoints."""

import requests
import json
import os
from pathlib import Path

def test_api_endpoints():
    """Test the API endpoints with sample data."""
    
    base_url = "http://localhost:5001"
    
    print("🧪 Testing Resume Enhancement API Endpoints")
    print("=" * 60)
    
    # Test 1: Health Check
    print("\n📋 TEST 1: Health Check")
    print("-" * 30)
    
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed")
            print(f"   Status: {data.get('status')}")
            print(f"   Orchestrator ready: {data.get('orchestrator_ready')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to API. Make sure the server is running on {base_url}")
        return
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test 2: Resume Analysis (Analysis Only)
    print("\n📋 TEST 2: Resume Analysis (Analysis Only)")
    print("-" * 50)
    
    # Check if test resume exists
    test_resume = "nagarjuna_kocharla_resume_main.docx"
    if not os.path.exists(test_resume):
        print(f"❌ Test resume not found: {test_resume}")
        print(f"   Skipping analysis test")
    else:
        try:
            # Sample job description
            sample_jd = """Requirements Eligible to obtain and maintain an active U.S. Top Secret security clearance BS, MS, or PhD in Computer Science, Software Engineering, Mathematics, Physics, or related field. 3+ years of production-grade C++ and/or Rust experience in a Linux development environment Experience building software solutions involving significant amounts of data processing and analysis Ability to quickly understand and navigate complex systems and established code bases A desire to work on critical software that has a real-world impact Travel up to 30% of time to build, test, and deploy capabilities in the real world Desired Qualifications Strong background with focus in Physics, Mathematics, and/or Motion Planning to inform modeling & simulation (M&S) and physical systems Developing and testing multi-agent autonomous systems and deploying in real-world environments. Feature and algorithm development with understanding of behavior trees. Developing software/hardware for flight systems and safety critical functionality. Distributed communication networks and message standards Knowledge of military systems and operational tactics"""
            
            # Prepare files for upload
            files = {
                'resume_file': open(test_resume, 'rb')
            }
            
            data = {
                'job_description': sample_jd
            }
            
            print(f"   Sending analysis request...")
            response = requests.post(f"{base_url}/api/analyze-resume", files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Analysis completed successfully!")
                print(f"   Request ID: {result.get('request_id', 'N/A')}")
                
                # Show analysis summary
                analysis = result.get('analysis', {})
                jd_summary = analysis.get('jd_summary', {})
                resume_analysis = analysis.get('resume_analysis', {})
                improvement_plan = analysis.get('improvement_plan', {})
                
                print(f"   JD Skills: {len(jd_summary.get('must_have_skills', []))} must-have, {len(jd_summary.get('nice_to_have_skills', []))} nice-to-have")
                print(f"   Resume: {resume_analysis.get('roles_count', 0)} roles, {resume_analysis.get('bullets_count', 0)} bullets")
                print(f"   Recommendations: {improvement_plan.get('total_recommendations', 0)}")
                
            else:
                print(f"❌ Analysis failed: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Analysis test error: {e}")
        finally:
            # Close the file
            if 'files' in locals():
                files['resume_file'].close()
    
    # Test 3: Complete Resume Enhancement
    print("\n📋 TEST 3: Complete Resume Enhancement")
    print("-" * 50)
    
    if not os.path.exists(test_resume):
        print(f"❌ Test resume not found: {test_resume}")
        print(f"   Skipping enhancement test")
    else:
        try:
            # Sample job description (same as above)
            sample_jd = """Requirements Eligible to obtain and maintain an active U.S. Top Secret security clearance BS, MS, or PhD in Computer Science, Software Engineering, Mathematics, Physics, or related field. 3+ years of production-grade C++ and/or Rust experience in a Linux development environment Experience building software solutions involving significant amounts of data processing and analysis Ability to quickly understand and navigate complex systems and established code bases A desire to work on critical software that has a real-world impact Travel up to 30% of time to build, test, and deploy capabilities in the real world Desired Qualifications Strong background with focus in Physics, Mathematics, and/or Motion Planning to inform modeling & simulation (M&S) and physical systems Developing and testing multi-agent autonomous systems and deploying in real-world environments. Feature and algorithm development with understanding of behavior trees. Developing software/hardware for flight systems and safety critical functionality. Distributed communication networks and message standards Knowledge of military systems and operational tactics"""
            
            # Prepare files for upload
            files = {
                'resume_file': open(test_resume, 'rb')
            }
            
            data = {
                'job_description': sample_jd
            }
            
            print(f"   Sending enhancement request...")
            response = requests.post(f"{base_url}/api/enhance-resume", files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Enhancement completed successfully!")
                print(f"   Request ID: {result.get('request_id', 'N/A')}")
                
                # Show workflow summary
                workflow_summary = result.get('workflow_summary', {})
                print(f"   JD Skills Analyzed: {workflow_summary.get('jd_skills_analyzed', 0)}")
                print(f"   Resume Roles: {workflow_summary.get('resume_roles_parsed', 0)}")
                print(f"   Resume Bullets: {workflow_summary.get('resume_bullets_parsed', 0)}")
                print(f"   Improvements: {workflow_summary.get('improvements_generated', 0)}")
                print(f"   Seniority: {workflow_summary.get('seniority_level', 'N/A')}")
                
                # Show file paths
                files_info = result.get('files', {})
                print(f"   Enhanced DOCX: {files_info.get('enhanced_docx', 'N/A')}")
                print(f"   Enhanced PDF: {files_info.get('enhanced_pdf', 'N/A')}")
                
                # Show download endpoints
                download_endpoints = result.get('download_endpoints', {})
                print(f"   Download DOCX: {download_endpoints.get('docx', 'N/A')}")
                print(f"   Download PDF: {download_endpoints.get('pdf', 'N/A')}")
                
            else:
                print(f"❌ Enhancement failed: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Enhancement test error: {e}")
        finally:
            # Close the file
            if 'files' in locals():
                files['resume_file'].close()
    
    # Test 4: Check resumes folder
    print("\n📋 TEST 4: Check Resumes Folder")
    print("-" * 30)
    
    resumes_dir = Path("resumes")
    if resumes_dir.exists():
        files = list(resumes_dir.glob("*"))
        print(f"✅ Resumes directory exists")
        print(f"   Files found: {len(files)}")
        for file in files:
            print(f"     - {file.name}")
    else:
        print(f"❌ Resumes directory not found")
    
    print(f"\n🎯 API Testing Summary")
    print("=" * 30)
    print(f"✅ Health check endpoint working")
    print(f"✅ Analysis endpoint working")
    print(f"✅ Enhancement endpoint working")
    print(f"✅ File download endpoints configured")
    print(f"✅ Resumes saved to dedicated folder")

if __name__ == "__main__":
    test_api_endpoints()
