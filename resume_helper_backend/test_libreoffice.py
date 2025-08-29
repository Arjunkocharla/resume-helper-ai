#!/usr/bin/env python3
"""
Test script to verify LibreOffice installation in Docker container
"""
import subprocess
import sys
import os

def test_libreoffice():
    """Test if LibreOffice is properly installed and accessible"""
    print("Testing LibreOffice installation...")
    
    # Test 1: Check if soffice command exists
    try:
        result = subprocess.run(['which', 'soffice'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ soffice found at: {result.stdout.strip()}")
        else:
            print("❌ soffice command not found")
            return False
    except Exception as e:
        print(f"❌ Error checking soffice: {e}")
        return False
    
    # Test 2: Check LibreOffice version
    try:
        result = subprocess.run(['soffice', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ LibreOffice version: {result.stdout.strip()}")
        else:
            print(f"❌ LibreOffice version check failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error checking LibreOffice version: {e}")
        return False
    
    # Test 3: Check if we can create a simple document
    try:
        # Create a simple test document
        test_content = """<?xml version="1.0" encoding="UTF-8"?>
<office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0">
<office:body><office:text><text:p>Test document</text:p></office:text></office:body>
</office:document-content>"""
        
        with open('test.odt', 'w') as f:
            f.write(test_content)
        
        # Try to convert it to PDF
        result = subprocess.run([
            'soffice', '--headless', '--convert-to', 'pdf', '--outdir', '.', 'test.odt'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ LibreOffice PDF conversion test passed")
        else:
            print(f"❌ LibreOffice PDF conversion failed: {result.stderr}")
            return False
            
        # Clean up test files
        for file in ['test.odt', 'test.pdf']:
            if os.path.exists(file):
                os.remove(file)
                
    except Exception as e:
        print(f"❌ Error testing LibreOffice conversion: {e}")
        return False
    
    print("🎉 All LibreOffice tests passed!")
    return True

if __name__ == "__main__":
    success = test_libreoffice()
    sys.exit(0 if success else 1)
