#!/usr/bin/env python3
"""Resume Enhancement API - Flask application with two main endpoints."""

import os
import logging
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import anthropic
from dotenv import load_dotenv
from flask_cors import CORS

# Import our services
from services.orchestrator import ResumeEnhancementOrchestrator

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Enable CORS for frontend at localhost:3000
CORS(app, resources={r"/api/*": {
    "origins": ["http://localhost:3000"],
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"],
    "supports_credentials": True
}})

# Create necessary directories
RESUMES_DIR = Path("resumes")
RESUMES_DIR.mkdir(exist_ok=True)
UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)

# Initialize the orchestrator
try:
    client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    orchestrator = ResumeEnhancementOrchestrator(client)
    logger.info("✅ Resume Enhancement Orchestrator initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize orchestrator: {e}")
    orchestrator = None

def allowed_file(filename):
    """Check if file extension is allowed."""
    allowed_extensions = {'docx', 'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_uploaded_file(file):
    """Save uploaded file and return the path."""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{filename}"
        file_path = UPLOADS_DIR / safe_filename
        file.save(file_path)
        logger.info(f"File saved: {file_path}")
        return str(file_path)
    return None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "orchestrator_ready": orchestrator is not None
    })

@app.route('/api/enhance-resume', methods=['POST'])
def enhance_resume():
    """
    Complete resume enhancement workflow.
    
    This endpoint:
    1. Parses the job description
    2. Analyzes the resume
    3. Generates improvement plan
    4. Applies enhancements
    5. Saves enhanced resume to resumes folder
    6. Returns file download links
    
    Request:
    - resume_file: DOCX or PDF file
    - job_description: Text description of the job
    
    Response:
    - Enhanced resume file (DOCX and PDF)
    - Workflow summary
    - Download links
    """
    try:
        # Check if orchestrator is ready
        if not orchestrator:
            return jsonify({
                "error": "Service temporarily unavailable",
                "message": "Orchestrator not initialized"
            }), 503
        
        # Validate request
        if 'resume_file' not in request.files:
            return jsonify({
                "error": "Missing resume file",
                "message": "Please upload a resume file"
            }), 400
        
        if 'job_description' not in request.form:
            return jsonify({
                "error": "Missing job description",
                "message": "Please provide a job description"
            }), 400
        
        # Get uploaded file and job description
        resume_file = request.files['resume_file']
        job_description = request.form['job_description'].strip()
        
        if not job_description:
            return jsonify({
                "error": "Empty job description",
                "message": "Job description cannot be empty"
            }), 400
        
        # Save uploaded file
        resume_path = save_uploaded_file(resume_file)
        if not resume_path:
            return jsonify({
                "error": "Invalid file format",
                "message": "Please upload a DOCX or PDF file"
            }), 400
        
        logger.info(f"Starting resume enhancement for: {resume_path}")
        
        # Run the complete enhancement workflow
        enhancement_results = orchestrator.enhance_resume(
            resume_path=resume_path,
            job_description=job_description,
            output_dir=str(RESUMES_DIR),
            preserve_original=True,
            generate_pdf=True
        )
        
        # Prepare response
        file_paths = enhancement_results.get('file_paths', {})
        workflow_summary = enhancement_results.get('workflow_summary', {})
        
        # Generate download URLs
        enhanced_docx = file_paths.get('enhanced_docx')
        enhanced_pdf = file_paths.get('enhanced_pdf')
        
        response_data = {
            "success": True,
            "message": "Resume enhanced successfully",
            "request_id": enhancement_results.get('request_id'),
            "workflow_summary": {
                "jd_skills_analyzed": workflow_summary.get('jd_skills_analyzed', 0),
                "resume_roles_parsed": workflow_summary.get('resume_roles_parsed', 0),
                "resume_bullets_parsed": workflow_summary.get('resume_bullets_parsed', 0),
                "improvements_generated": workflow_summary.get('improvements_generated', 0),
                "seniority_level": workflow_summary.get('seniority_level', 'N/A')
            },
            "files": {
                "enhanced_docx": enhanced_docx,
                "enhanced_pdf": enhanced_pdf
            },
            "download_endpoints": {
                "docx": f"/api/download/{Path(enhanced_docx).name}" if enhanced_docx else None,
                "pdf": f"/api/download/{Path(enhanced_pdf).name}" if enhanced_pdf else None
            },
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Resume enhancement completed successfully: {enhancement_results.get('request_id')}")
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Resume enhancement failed: {e}")
        return jsonify({
            "error": "Resume enhancement failed",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/analyze-resume', methods=['POST'])
def analyze_resume():
    """
    Resume analysis only (no file modification).
    
    This endpoint:
    1. Parses the job description
    2. Analyzes the resume
    3. Generates improvement plan
    4. Returns analysis results (no file changes)
    
    Request:
    - resume_file: DOCX or PDF file
    - job_description: Text description of the job
    
    Response:
    - Analysis results
    - Improvement recommendations
    - Skills gap analysis
    """
    try:
        # Check if orchestrator is ready
        if not orchestrator:
            return jsonify({
                "error": "Service temporarily unavailable",
                "message": "Orchestrator not initialized"
            }), 503
        
        # Validate request
        if 'resume_file' not in request.files:
            return jsonify({
                "error": "Missing resume file",
                "message": "Please upload a resume file"
            }), 400
        
        if 'job_description' not in request.form:
            return jsonify({
                "error": "Missing job description",
                "message": "Please provide a job description"
            }), 400
        
        # Get uploaded file and job description
        resume_file = request.files['resume_file']
        job_description = request.form['job_description'].strip()
        
        if not job_description:
            return jsonify({
                "error": "Empty job description",
                "message": "Job description cannot be empty"
            }), 400
        
        # Save uploaded file
        resume_path = save_uploaded_file(resume_file)
        if not resume_path:
            return jsonify({
                "error": "Invalid file format",
                "message": "Please upload a DOCX or PDF file"
            }), 400
        
        logger.info(f"Starting resume analysis for: {resume_path}")
        
        # Run analysis only workflow
        analysis_results = orchestrator.analyze_only(resume_path, job_description)
        
        # Extract improvement plan details
        improvement_plan = analysis_results.get('improvement_plan')
        edits = []
        
        if improvement_plan:
            for edit in improvement_plan.edits:
                edit_info = {
                    "type": edit.type,
                    "description": ""
                }
                
                if edit.type == "modify_bullet":
                    edit_info["description"] = f"Modify bullet point: {edit.new_text[:100]}..."
                elif edit.type == "insert_bullet":
                    edit_info["description"] = f"Add new bullet: {edit.text[:100]}..."
                elif edit.type == "upsert_skill":
                    edit_info["description"] = f"Add skill: {edit.value} to {edit.bucket}"
                
                edits.append(edit_info)
        
        # Prepare response
        response_data = {
            "success": True,
            "message": "Resume analysis completed successfully",
            "analysis": {
                "jd_summary": {
                    "must_have_skills": analysis_results.get('jd_summary', {}).must_have if hasattr(analysis_results.get('jd_summary', {}), 'must_have') else [],
                    "nice_to_have_skills": analysis_results.get('jd_summary', {}).nice_to_have if hasattr(analysis_results.get('jd_summary', {}), 'nice_to_have') else [],
                    "seniority_level": analysis_results.get('jd_summary', {}).seniority if hasattr(analysis_results.get('jd_summary', {}), 'seniority') else None
                },
                "resume_analysis": {
                    "roles_count": len(analysis_results.get('resume_ast', {}).roles) if hasattr(analysis_results.get('resume_ast', {}), 'roles') else 0,
                    "bullets_count": len(analysis_results.get('resume_ast', {}).bullets) if hasattr(analysis_results.get('resume_ast', {}), 'bullets') else 0,
                    "skills_categories": len(analysis_results.get('resume_ast', {}).skills_buckets) if hasattr(analysis_results.get('resume_ast', {}), 'skills_buckets') else 0
                },
                "improvement_plan": {
                    "total_recommendations": len(edits),
                    "recommendations": edits
                }
            },
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Resume analysis completed successfully")
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Resume analysis failed: {e}")
        return jsonify({
            "error": "Resume analysis failed",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    """Download enhanced resume files."""
    try:
        # Security check - only allow downloads from resumes directory
        file_path = RESUMES_DIR / filename
        
        if not file_path.exists():
            return jsonify({
                "error": "File not found",
                "message": "The requested file does not exist"
            }), 404
        
        # Determine content type
        if filename.endswith('.docx'):
            mimetype = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        elif filename.endswith('.pdf'):
            mimetype = 'application/pdf'
        else:
            mimetype = 'application/octet-stream'
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype=mimetype
        )
        
    except Exception as e:
        logger.error(f"File download failed: {e}")
        return jsonify({
            "error": "Download failed",
            "message": str(e)
        }), 500

@app.route('/api/status/<request_id>', methods=['GET'])
def get_workflow_status(request_id):
    """Get the status of a specific workflow request."""
    try:
        if not orchestrator:
            return jsonify({
                "error": "Service unavailable",
                "message": "Orchestrator not initialized"
            }), 503
        
        status = orchestrator.get_workflow_status(request_id)
        return jsonify(status), 200
        
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        return jsonify({
            "error": "Status check failed",
            "message": str(e)
        }), 500

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error."""
    return jsonify({
        "error": "File too large",
        "message": "File size exceeds 16MB limit"
    }), 413

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({
        "error": "Endpoint not found",
        "message": "The requested endpoint does not exist"
    }), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors."""
    return jsonify({
        "error": "Internal server error",
        "message": "Something went wrong on our end"
    }), 500

if __name__ == '__main__':
    # Create resumes directory if it doesn't exist
    RESUMES_DIR.mkdir(exist_ok=True)
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=True
    )
