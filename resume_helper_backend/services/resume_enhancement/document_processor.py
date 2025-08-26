from langchain.text_splitter import RecursiveCharacterTextSplitter
from docx import Document
import os
from langchain_community.document_loaders import Docx2txtLoader

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " "]
        )
    
    def load_and_parse(self, file_path: str) -> dict:
        """Load and parse document into structured sections"""
        loader = Docx2txtLoader(file_path)
        doc = loader.load()[0]  # Returns list of documents, get first one
        return self._extract_sections(doc.page_content)

    def _extract_sections(self, text: str) -> dict:
        """Extract sections from resume text"""
        sections = {}
        current_section = None
        current_content = []
        
        # Split text into lines
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if line is a section header (all uppercase)
            if line.isupper():
                # Save previous section if exists
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content)
                
                # Start new section
                current_section = line
                current_content = []
            elif current_section:
                current_content.append(line)
        
        # Add last section
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
