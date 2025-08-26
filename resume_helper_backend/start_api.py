#!/usr/bin/env python3
"""
Simple startup script for the unified Resume Helper API
"""

import os
import sys
import subprocess
import time

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        ('flask', 'flask'),
        ('flask-cors', 'flask_cors'),
        ('anthropic', 'anthropic'),
        ('python-docx', 'docx'),
        ('PyPDF2', 'PyPDF2')
    ]
    
    missing_packages = []
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nInstall them with: pip install " + " ".join(missing_packages))
        return False
    
    print("✅ All required packages are installed")
    return True

def check_directories():
    """Ensure required directories exist"""
    directories = ['uploads', 'resumes', 'services']
    
    for directory in directories:
        if not os.path.exists(directory):
            print(f"❌ Directory '{directory}' not found")
            return False
    
    print("✅ All required directories exist")
    return True

def activate_venv():
    """Try to activate virtual environment if it exists"""
    venv_paths = [
        'venv/bin/activate',
        'resume_app_venv/bin/activate',
        'py3.9env/bin/activate'
    ]
    
    for venv_path in venv_paths:
        if os.path.exists(venv_path):
            print(f"🔧 Found virtual environment: {venv_path}")
            
            # Set environment variables
            venv_dir = os.path.dirname(venv_path)
            os.environ['VIRTUAL_ENV'] = os.path.abspath(venv_dir)
            os.environ['PATH'] = os.path.join(os.path.abspath(venv_dir), 'bin') + os.pathsep + os.environ['PATH']
            
            # Add site-packages to Python path
            site_packages = os.path.join(venv_dir, 'lib', 'python3.9', 'site-packages')
            if os.path.exists(site_packages):
                sys.path.insert(0, site_packages)
            
            print("✅ Virtual environment activated")
            return True
    
    print("⚠️  No virtual environment found, using system Python")
    return False

def start_api():
    """Start the unified API"""
    print("\n🚀 Starting unified Resume Helper API...")
    print("📍 API will be available at: http://localhost:5001")
    print("🔍 Health check: http://localhost:5001/health")
    print("📚 API docs: http://localhost:5001/api/status")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        # Import and run the app
        from app import app
        app.run(
            host='0.0.0.0',
            port=5001,
            debug=True,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n\n🛑 API server stopped by user")
    except Exception as e:
        print(f"\n❌ Failed to start API: {e}")
        print("Check the error message above and fix any issues")

def main():
    """Main startup function"""
    print("=" * 60)
    print("🚀 Resume Helper API - Unified Startup")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies first")
        return 1
    
    # Check directories
    if not check_directories():
        print("\n❌ Please ensure all required directories exist")
        return 1
    
    # Try to activate virtual environment
    activate_venv()
    
    # Start the API
    start_api()
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
