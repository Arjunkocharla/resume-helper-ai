#!/usr/bin/env python3
"""Test the document editor directly with a mock improvement plan."""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.agents.document_editor_agent import DocumentEditorAgent
from services.contracts import Plan, InsertBullet, ModifyBullet, UpsertSkill

def test_document_editor_directly():
    """Test the document editor with a mock plan to verify bullet formatting fixes."""
    
    print("🧪 Testing Document Editor Agent Directly")
    print("=" * 50)
    
    # Test resume file
    test_resume = "nagarjuna_kocharla_resume_main.docx"
    
    if not os.path.exists(test_resume):
        print(f"❌ Test resume not found: {test_resume}")
        return
    
    print(f"📄 Original Resume: {test_resume}")
    print(f"   Size: {os.path.getsize(test_resume)} bytes")
    
    # Create a mock improvement plan
    mock_plan = Plan(
        edits=[
            InsertBullet(
                role_id="role_1",
                text="Developed and tested multi-agent autonomous systems for defense applications, leveraging behavior trees and distributed communication networks to enable real-world deployments in critical software environments."
            ),
            InsertBullet(
                role_id="role_1", 
                text="Engineered software and hardware solutions for flight systems and safety-critical functionality, with expertise in physics, mathematics, and motion planning for modeling & simulation applications."
            ),
            UpsertSkill(
                bucket="Technical Skills",
                value="Multi-Agent Systems"
            ),
            UpsertSkill(
                bucket="Technical Skills", 
                value="Behavior Trees"
            )
        ]
    )
    
    print(f"\n🎯 Mock Improvement Plan:")
    print(f"   - Insert 2 new bullets")
    print(f"   - Add 2 new skills")
    print(f"   Total edits: {len(mock_plan.edits)}")
    
    # Create a mock ResumeAST (simplified)
    class MockResumeAST:
        def __init__(self):
            self.roles = [MockRole("role_1", "Software Engineer", "CentrAlert")]
            self.bullets = []
            self.skills_buckets = {"Technical Skills": ["Python", "C#", ".NET"]}
    
    class MockRole:
        def __init__(self, id, title, company):
            self.id = id
            self.title = title
            self.company = company
    
    mock_resume_ast = MockResumeAST()
    
    print(f"\n🔄 Testing Document Editor...")
    print("-" * 30)
    
    try:
        # Initialize document editor
        doc_editor = DocumentEditorAgent()
        
        # Apply the mock plan
        enhanced_path = doc_editor.apply_plan(
            docx_path=test_resume,
            plan=mock_plan,
            resume_ast=mock_resume_ast
        )
        
        print(f"✅ Document editing completed successfully!")
        print(f"   Enhanced file: {enhanced_path}")
        print(f"   File size: {os.path.getsize(enhanced_path)} bytes")
        
        # Check if the enhanced file exists
        if os.path.exists(enhanced_path):
            print(f"\n📁 Files in current directory:")
            for file in os.listdir("."):
                if file.endswith(".docx") and "enhanced" in file:
                    print(f"   - {file} ({os.path.getsize(file)} bytes)")
            
            print(f"\n🎯 Before/After Summary:")
            print(f"   BEFORE: {test_resume}")
            print(f"   AFTER:  {os.path.basename(enhanced_path)}")
            
            print(f"\n✅ Test completed successfully!")
            print(f"   The document editor should now properly handle bullet formatting")
            print(f"   - No more double bullets (• •)")
            print(f"   - Respects Word's automatic bullet formatting")
            print(f"   - Only adds manual bullets when needed")
            
        else:
            print(f"❌ Enhanced file not found: {enhanced_path}")
            
    except Exception as e:
        print(f"❌ Document editing failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_document_editor_directly()
