from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import Dict, List
import json
from .models import EnhancementResponse, EnhancementSuggestion

class EnhancementChain:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.2
        )
        
        self.prompt = PromptTemplate(
            input_variables=["resume_text", "job_description"],
            template="""As an expert ATS optimization specialist and resume editor, analyze this job description and update the resume to improve ATS scoring while maintaining exact formatting.

Job Description:
{job_description}

Resume:
{resume_text}

Instructions:
1. Analyze the job description for key skills, qualifications, and terminology.
2. IMPORTANT: Use EXACTLY the same section names as they appear in the resume
3. For each suggestion, provide:
   - The exact section name as it appears in the resume
   - For work experience: include "role" and "suggestion" fields
   - For other sections: include only "suggestion" field
4. Each suggestion must be a new, unique bullet point

Return ONLY a JSON object in this exact format:
{{
    "sections": {{
        "WORK EXPERIENCE": [
            {{
                "role": "Software Engineer at Company",
                "suggestion": "• Implemented feature X improving Y by Z%"
            }}
        ],
        "SKILLS": [
            {{
                "suggestion": "• Python, Django, FastAPI"
            }}
        ]
    }}
}}"""
        )
        
        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt
        )

    def run(self, resume_sections: Dict, job_description: str) -> EnhancementResponse:
        """Run the enhancement chain"""
        try:
            # Combine all sections into a single text
            resume_text = "\n\n".join(
                f"{section.upper()}:\n{content}" 
                for section, content in resume_sections.items()
                if content  # Only include non-empty sections
            )
            
            # Get response from LLM
            response = self.chain.run({
                "resume_text": resume_text,
                "job_description": job_description
            })
            
            # Parse JSON response
            json_response = json.loads(response)
            
            # Wrap the response in 'sections' key to match our model
            wrapped_response = {'sections': json_response}
            
            # Convert to EnhancementResponse model
            return EnhancementResponse(**wrapped_response)
            
        except Exception as e:
            print(f"Error in enhancement chain: {str(e)}")
            raise
