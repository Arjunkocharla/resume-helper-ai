#!/usr/bin/env python3
"""PDF conversion utility for converting DOCX to PDF and PDF to DOCX."""

import logging
import os
import subprocess
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class PDFConverter:
    """Utility for converting between DOCX and PDF formats."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def convert_pdf_to_docx(self, pdf_path: str, output_path: Optional[str] = None) -> str:
        """
        Convert PDF file to DOCX format.
        
        Args:
            pdf_path: Path to input PDF file
            output_path: Path for output DOCX file (optional)
            
        Returns:
            str: Path to created DOCX file
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist
            RuntimeError: If conversion fails
        """
        try:
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
            # Generate output path if not provided
            if output_path is None:
                output_path = self._generate_docx_path(pdf_path)
            
            self.logger.info(f"Converting {pdf_path} to DOCX: {output_path}")
            
            # Extract text from PDF
            text_content = self._extract_text_from_pdf(pdf_path)
            
            # Create DOCX from text
            self._create_docx_from_text(text_content, output_path)
            
            self.logger.info(f"Successfully converted PDF to DOCX: {output_path}")
            return output_path
                
        except Exception as e:
            self.logger.error(f"PDF to DOCX conversion failed: {e}")
            raise
    
    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from PDF file."""
        try:
            import PyPDF2
            
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text_content = ""
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text_content += page.extract_text() + "\n"
                
                return text_content.strip()
                
        except ImportError:
            raise RuntimeError("PyPDF2 is required for PDF to DOCX conversion")
        except Exception as e:
            raise RuntimeError(f"Failed to extract text from PDF: {e}")
    
    def _create_docx_from_text(self, text_content: str, output_path: str) -> None:
        """Create a DOCX file from text content."""
        try:
            from docx import Document
            
            # Create output directory if it doesn't exist
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Create new document
            doc = Document()
            
            # Split text into paragraphs and add to document
            paragraphs = text_content.split('\n')
            for paragraph_text in paragraphs:
                if paragraph_text.strip():  # Skip empty lines
                    doc.add_paragraph(paragraph_text.strip())
            
            # Save document
            doc.save(output_path)
            
        except ImportError:
            raise RuntimeError("python-docx is required for PDF to DOCX conversion")
        except Exception as e:
            raise RuntimeError(f"Failed to create DOCX from text: {e}")
    
    def _generate_docx_path(self, pdf_path: str) -> str:
        """Generate output DOCX path from input PDF path."""
        pdf_dir = os.path.dirname(pdf_path)
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        return os.path.join(pdf_dir, f"{pdf_name}_converted.docx")
    
    def convert_docx_to_pdf(self, docx_path: str, output_path: Optional[str] = None) -> str:
        """
        Convert DOCX file to PDF format.
        
        Args:
            docx_path: Path to input DOCX file
            output_path: Path for output PDF file (optional)
            
        Returns:
            str: Path to created PDF file
            
        Raises:
            FileNotFoundError: If DOCX file doesn't exist
            RuntimeError: If conversion fails
        """
        try:
            if not os.path.exists(docx_path):
                raise FileNotFoundError(f"DOCX file not found: {docx_path}")
            
            # Generate output path if not provided
            if output_path is None:
                output_path = self._generate_pdf_path(docx_path)
            
            self.logger.info(f"Converting {docx_path} to PDF: {output_path}")
            
            # Try different conversion methods
            if self._try_libreoffice_conversion(docx_path, output_path):
                self.logger.info("Successfully converted using LibreOffice")
                return output_path
            elif self._try_docx2pdf_conversion(docx_path, output_path):
                self.logger.info("Successfully converted using docx2pdf")
                return output_path
            else:
                # Don't fail the entire workflow, just log and return DOCX path
                self.logger.warning("All PDF conversion methods failed, returning DOCX path")
                return docx_path
                
        except Exception as e:
            self.logger.error(f"PDF conversion failed: {e}")
            raise
    
    def _try_libreoffice_conversion(self, docx_path: str, output_path: str) -> bool:
        """Try to convert using LibreOffice headless."""
        try:
            # Create output directory if it doesn't exist
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # LibreOffice command for headless conversion
            cmd = [
                'soffice',
                '--headless',
                '--convert-to', 'pdf',
                '--outdir', output_dir,
                docx_path
            ]
            
            # Run conversion
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60  # 60 second timeout
            )
            
            if result.returncode == 0:
                # LibreOffice creates PDF with same name in output directory
                libreoffice_pdf = os.path.join(
                    output_dir, 
                    os.path.splitext(os.path.basename(docx_path))[0] + '.pdf'
                )
                
                # Move to desired output path if different
                if libreoffice_pdf != output_path:
                    os.rename(libreoffice_pdf, output_path)
                
                return True
            else:
                self.logger.warning(f"LibreOffice conversion failed: {result.stderr}")
                return False
                
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
            self.logger.warning(f"LibreOffice conversion not available: {e}")
            return False
    
    def _try_docx2pdf_conversion(self, docx_path: str, output_path: str) -> bool:
        """Try to convert using docx2pdf library."""
        try:
            import docx2pdf
            
            # Create output directory if it doesn't exist
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Convert using docx2pdf
            docx2pdf.convert(docx_path, output_path)
            
            # Verify file was created
            if os.path.exists(output_path):
                return True
            else:
                return False
                
        except ImportError:
            self.logger.warning("docx2pdf library not available")
            return False
        except Exception as e:
            self.logger.warning(f"docx2pdf conversion failed: {e}")
            return False
    
    def _generate_pdf_path(self, docx_path: str) -> str:
        """Generate output PDF path from DOCX path."""
        path = Path(docx_path)
        output_name = f"{path.stem}_enhanced.pdf"
        output_path = path.parent / output_name
        
        # Ensure unique filename
        counter = 1
        while output_path.exists():
            output_name = f"{path.stem}_enhanced_{counter}.pdf"
            output_path = path.parent / output_name
            counter += 1
        
        return str(output_path)
    
    def verify_pdf_creation(self, pdf_path: str) -> bool:
        """
        Verify that PDF file was created successfully.
        
        Args:
            pdf_path: Path to PDF file to verify
            
        Returns:
            bool: True if PDF is valid, False otherwise
        """
        try:
            if not os.path.exists(pdf_path):
                return False
            
            # Check file size (should be reasonable for a resume)
            file_size = os.path.getsize(pdf_path)
            if file_size < 1000:  # Less than 1KB is suspicious
                return False
            
            # Try to read PDF header
            with open(pdf_path, 'rb') as f:
                header = f.read(4)
                if header != b'%PDF':
                    return False
            
            self.logger.info(f"PDF verification successful: {pdf_path} ({file_size:,} bytes)")
            return True
            
        except Exception as e:
            self.logger.error(f"PDF verification failed: {e}")
            return False
