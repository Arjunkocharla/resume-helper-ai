#!/usr/bin/env python3
"""Test script for the new LLM Document Editor Agent."""

import os
import sys
import anthropic
from dotenv import load_dotenv

# Add the services directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'services'))

from services.agents.llm_document_editor_agent import LLMDocumentEditorAgent
from services.contracts import Plan, ModifyBullet, InsertBullet, UpsertSkill, PlanConstraints

def test_llm_document_editor():
    """Test the LLM document editor with a simple improvement plan."""
    
    # Load environment variables
    load_dotenv()
    
    # Initialize Anthropic client
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found in environment variables")
        return
    
    client = anthropic.Anthropic(api_key=api_key)
    
    # Initialize the LLM document editor
    editor = LLMDocumentEditorAgent(client)
    
    # Test document path
    test_docx = "nagarjuna_kocharla_resume_main.docx"
    if not os.path.exists(test_docx):
        print(f"❌ Test document not found: {test_docx}")
        return
    
    print(f"🧪 Testing LLM Document Editor Agent")
    print(f"📄 Input document: {test_docx}")
    
    # Create a simple test improvement plan
    test_plan = Plan(
        edits=[
            ModifyBullet(
                bullet_id="bullet_1",
                new_text="• Designed and scaled a distributed backend system for an emergency communications platform serving 100,000+ users, using .NET (C# 9.0+), Python, and SQL Server; architected RESTful and gRPC APIs, reducing end-to-end latency by 40% and enabling seamless third-party integrations."
            ),
            InsertBullet(
                role_id="role_1",
                after_bullet_id="bullet_2",
                text="• Implemented caching mechanisms using Redis and Memcached, reducing database load by 30% and improving response times for high-traffic API endpoints."
            )
        ],
        constraints=PlanConstraints(max_bullets_per_role=5, forbid_fabrication=True)
    )
    
    # Mock resume AST for context
    class MockResumeAST:
        def __init__(self):
            self.roles = [type('Role', (), {'id': 'role_1'})()]
            self.bullets = [type('Bullet', (), {'id': 'bullet_1'})()]
    
    resume_ast = MockResumeAST()
    
    try:
        print("🔄 Applying improvement plan with LLM vision...")
        
        # Apply the plan
        enhanced_docx = editor.apply_plan(
            docx_path=test_docx,
            plan=test_plan,
            resume_ast=resume_ast
        )
        
        print(f"✅ Success! Enhanced document saved to: {enhanced_docx}")
        
        # Check file size
        if os.path.exists(enhanced_docx):
            size = os.path.getsize(enhanced_docx)
            print(f"📁 File size: {size} bytes")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_llm_document_editor()
