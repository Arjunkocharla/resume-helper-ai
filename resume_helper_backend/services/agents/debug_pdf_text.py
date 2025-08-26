#!/usr/bin/env python3
"""Debug script to see what text is being extracted from the PDF."""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def debug_pdf_text():
    """Debug PDF text extraction."""
    
    # Path to the real resume PDF
    resume_path = "nagarjuna_kocharla_resume_recent.pdf"
    
    if not os.path.exists(resume_path):
        print(f"❌ Resume file not found: {resume_path}")
        return
    
    try:
        import PyPDF2
        
        print(f"Debugging PDF text extraction from: {resume_path}")
        
        with open(resume_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num, page in enumerate(pdf_reader.pages):
                print(f"\n=== PAGE {page_num + 1} ===")
                text = page.extract_text()
                
                # Show raw text
                print("RAW TEXT:")
                print(text)
                print("\n" + "="*50)
                
                # Show line by line
                lines = text.split('\n')
                print(f"LINES ({len(lines)}):")
                for i, line in enumerate(lines):
                    if line.strip():
                        print(f"{i:3d}: '{line.strip()}'")
                
                # Only show first page for brevity
                break
                
    except ImportError:
        print("PyPDF2 not available")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_pdf_text()
