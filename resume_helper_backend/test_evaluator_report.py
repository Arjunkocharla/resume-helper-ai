#!/usr/bin/env python3
"""Test script to see detailed evaluation report."""

import os
import json
from pathlib import Path

# Read the latest workflow summary to see the evaluation report
artifacts_dir = "resumes/workflow_artifacts"
if os.path.exists(artifacts_dir):
    files = [f for f in os.listdir(artifacts_dir) if f.startswith("workflow_summary_")]
    if files:
        latest_file = sorted(files)[-1]
        with open(os.path.join(artifacts_dir, latest_file), 'r') as f:
            data = json.load(f)
            
        print("🔍 Latest Evaluation Report:")
        print("=" * 50)
        
        eval_report = data.get("evaluation_report", {})
        print(f"✅ Passed: {eval_report.get('passed', 'Unknown')}")
        print(f"🚨 Issues: {eval_report.get('issues', [])}")
        
        if eval_report.get("duplicates"):
            print(f"\n📋 Duplicate Bullets ({len(eval_report['duplicates'])}):")
            for dup in eval_report["duplicates"]:
                print(f"  - Para {dup['paragraph_index']}: {dup['text'][:100]}...")
        
        if eval_report.get("orphaned_bullets"):
            print(f"\n🔗 Orphaned Bullets ({len(eval_report['orphaned_bullets'])}):")
            for orph in eval_report["orphaned_bullets"]:
                print(f"  - Para {orph['paragraph_index']}: {orph['text'][:100]}...")
        
        if eval_report.get("company_changes"):
            print(f"\n🏢 Company Line Changes:")
            for change in eval_report["company_changes"]:
                print(f"  Original: {change.get('original', [])}")
                print(f"  Enhanced: {change.get('enhanced', [])}")
        
        if eval_report.get("structural_issues"):
            print(f"\n🏗️ Structural Issues ({len(eval_report['structural_issues'])}):")
            for issue in eval_report["structural_issues"]:
                print(f"  - Para {issue['paragraph_index']}: {issue['issue']} - {issue['text']}")
        
        print(f"\n📁 Enhanced File: {data['file_paths']['enhanced_docx']}")
    else:
        print("No workflow summary files found")
else:
    print("No artifacts directory found")
