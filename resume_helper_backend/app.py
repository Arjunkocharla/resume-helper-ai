from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import os
import logging
from pathlib import Path
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime

# Import your services
from services.orchestrator import ResumeEnhancementOrchestrator
from services.agents.skills_categorization_agent import SkillsCategorizationAgent
from services.llm_client import UnifiedLLMClient, LLMProvider
from config.llm_config import llm_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Enable CORS for frontend and production
# Note: Cannot use "*" with supports_credentials=True, so we list origins explicitly
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://resumehelperapp.web.app",
    "https://resumehelperapp.firebaseapp.com"
]

# Simplified CORS configuration
CORS(app, 
     origins=allowed_origins,
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["*"],
     supports_credentials=True)

# Configuration
UPLOAD_FOLDER = 'uploads'
RESUMES_FOLDER = 'resumes'
ALLOWED_EXTENSIONS = {'docx'}

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESUMES_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESUMES_FOLDER'] = RESUMES_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_filename(original_filename, prefix=""):
    """Generate unique filename with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name, ext = os.path.splitext(original_filename)
    unique_id = str(uuid.uuid4())[:8]
    return f"{prefix}{timestamp}_{name}_{unique_id}{ext}"

# ============================================================================
# HEALTH & STATUS ENDPOINTS
# ============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/', methods=['GET'])
def root():
    """Root endpoint for debugging"""
    return jsonify({
        'message': 'Resume Helper API is running',
        'endpoints': [
            '/health',
            '/api/enhance-resume',
            '/api/analyze-resume',
            '/suggest_keywords'
        ],
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/status', methods=['GET'])
def api_status():
    """API status and configuration"""
    return jsonify({
        'status': 'operational',
        'endpoints': {
            'resume_enhancement': '/api/enhance-resume',
            'resume_analysis': '/api/analyze-resume',
            'suggest_keywords': '/suggest_keywords',
            'user_profile': '/api/user/profile',
            'resume_management': '/api/resumes',
            'file_download': '/api/download/<filename>'
        },
        'supported_formats': list(ALLOWED_EXTENSIONS),
        'max_file_size': '16MB',
        'llm_providers': llm_config.list_available_providers()
    })

@app.route('/api/llm/providers', methods=['GET'])
def llm_providers():
    """Get available LLM providers and their status"""
    return jsonify({
        'available_providers': llm_config.list_available_providers(),
        'default_provider': llm_config.default_provider.value,
        'cost_comparison': {
            'anthropic': f"${llm_config.providers[LLMProvider.ANTHROPIC]['cost_per_1m_tokens']:.3f} per 1M tokens",
            'groq': f"${llm_config.providers[LLMProvider.GROQ]['cost_per_1m_tokens']:.3f} per 1M tokens"
        }
    })

# ============================================================================
# RESUME ENHANCEMENT ENDPOINTS
# ============================================================================

@app.route('/api/enhance-resume', methods=['POST', 'OPTIONS'])
def enhance_resume():
    """Main resume enhancement endpoint"""
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
        response.headers.add('Access-Control-Allow-Headers', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    
    try:
        # Check if file is present
        if 'resume_file' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        file = request.files['resume_file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if job description is present
        job_description = request.form.get('job_description', '').strip()
        if not job_description:
            return jsonify({'error': 'Job description is required'}), 400
        
        # Validate file
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only PDF and DOCX are allowed'}), 400
        
        # Save uploaded file
        filename = generate_filename(secure_filename(file.filename), "enhancement_")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        logger.info(f"File uploaded: {filename}")
        
        # Initialize orchestrator and enhance resume
        # Allow API to specify LLM provider, default to Groq (cheapest)
        provider_param = request.form.get('llm_provider', '').strip()
        quality_param = request.form.get('llm_quality', 'fast').strip()
        
        try:
            if provider_param:
                provider = LLMProvider(provider_param)
            else:
                provider = None  # Will default to Groq
        except ValueError:
            provider = None
        
        # HYBRID APPROACH: Orchestrator will use Groq for parsing/analysis, Anthropic for quality tasks
        llm_client = UnifiedLLMClient(preferred_provider=provider)
        orchestrator = ResumeEnhancementOrchestrator(anthropic_client=llm_client)
        
        # Create unique request ID
        request_id = str(uuid.uuid4())
        
        # Start enhancement process
        result = orchestrator.enhance_resume(
            resume_path=filepath,
            job_description=job_description,
            output_dir=app.config['RESUMES_FOLDER']
        )
        
        # Prepare response
        response_data = {
            'request_id': request_id,
            'status': 'completed',
            'workflow_summary': result['workflow_summary'],
            'files': {
                'enhanced_docx': result['file_paths']['enhanced_docx'],
                'enhanced_pdf': result['file_paths']['enhanced_pdf']
            },
            'message': 'Resume enhancement completed successfully'
        }
        
        logger.info(f"Enhancement completed for request {request_id}")
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Enhancement failed: {str(e)}")
        return jsonify({
            'error': 'Resume enhancement failed',
            'message': str(e)
        }), 500

@app.route('/api/analyze-resume', methods=['POST'])
def analyze_resume():
    """Resume analysis endpoint (without enhancement)"""
    try:
        # Check if file is present
        if 'resume_file' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        file = request.files['resume_file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if job description is present
        job_description = request.form.get('job_description', '').strip()
        if not job_description:
            return jsonify({'error': 'Job description is required'}), 400
        
        # Validate file
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only PDF and DOCX are allowed'}), 400
        
        # Save uploaded file temporarily
        filename = generate_filename(secure_filename(file.filename), "analysis_")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        logger.info(f"Analysis file uploaded: {filename}")
        
        # Initialize orchestrator for analysis only
        # Allow API to specify LLM provider, default to Groq (cheapest)
        provider_param = request.form.get('llm_provider', '').strip()
        quality_param = request.form.get('llm_quality', 'fast').strip()
        
        try:
            if provider_param:
                provider = LLMProvider(provider_param)
            else:
                provider = None  # Will default to Groq
        except ValueError:
            provider = None
        
        llm_client = UnifiedLLMClient(preferred_provider=provider)
        orchestrator = ResumeEnhancementOrchestrator(anthropic_client=llm_client)
        
        # Perform analysis without enhancement
        analysis_result = orchestrator.analyze_only(
            resume_path=filepath,
            job_description=job_description
        )
        
        # Clean up temporary file
        try:
            os.remove(filepath)
        except:
            pass
        
        return jsonify({
            'status': 'completed',
            'analysis': analysis_result,
            'message': 'Resume analysis completed successfully'
        })
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        return jsonify({
            'error': 'Resume analysis failed',
            'message': str(e)
        }), 500

@app.route('/api/suggest-keywords', methods=['POST'])
def suggest_keywords():
    """Suggest keywords endpoint (for SuggestKeywords component)"""
    logger.info("Suggest keywords endpoint called")
    logger.info(f"Request form data: {dict(request.form)}")
    logger.info(f"Request files: {list(request.files.keys())}")
    
    try:
        # Check if file is present
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        file = request.files['resume']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if job description is present
        job_description = request.form.get('job_description', '').strip()
        if not job_description:
            return jsonify({'error': 'Job description is required'}), 400
        
        # Check retry parameter
        retry = request.form.get('retry', 'false').lower() == 'true'
        
        # For suggest keywords, allow both PDF and DOCX since we're only analyzing
        file_extension = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        if file_extension not in {'pdf', 'docx'}:
            return jsonify({'error': 'Invalid file type. Only PDF and DOCX are allowed'}), 400
        
        # Save uploaded file temporarily
        filename = generate_filename(secure_filename(file.filename), "suggest_")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        logger.info(f"Suggest keywords file uploaded: {filename}")
        
        # Initialize orchestrator for keyword suggestion
        # Allow API to specify LLM provider, default to Groq (cheapest)
        provider_param = request.form.get('llm_provider', '').strip()
        quality_param = request.form.get('llm_quality', 'fast').strip()
        
        try:
            if provider_param:
                provider = LLMProvider(provider_param)
            else:
                provider = None  # Will default to Groq
        except ValueError:
            provider = None
        
        # For hybrid approach: use Groq for fast analysis, Anthropic for quality if needed
        llm_client = UnifiedLLMClient(preferred_provider=provider)
        orchestrator = ResumeEnhancementOrchestrator(anthropic_client=llm_client)
        
        # Perform keyword analysis
        analysis_result = orchestrator.analyze_only(
            resume_path=filepath,
            job_description=job_description
        )
        
        # Clean up temporary file
        try:
            os.remove(filepath)
        except:
            pass
        
        # Format response for SuggestKeywords component based on actual analysis result
        # The analyze_only method returns: jd_summary, resume_ast, improvement_plan
        jd_summary = analysis_result.get('jd_summary')
        improvement_plan = analysis_result.get('improvement_plan')
        
        # Extract skills from JD summary - handle both object and dict cases
        if hasattr(jd_summary, 'must_have') and hasattr(jd_summary, 'nice_to_have'):
            # JDSummary object
            jd_skills = []
            for skill in jd_summary.must_have:
                jd_skills.append({'name': skill, 'category': 'Must-Have', 'frequency': 'High'})
            for skill in jd_summary.nice_to_have:
                jd_skills.append({'name': skill, 'category': 'Nice-to-Have', 'frequency': 'Medium'})
        elif isinstance(jd_summary, dict):
            # Dictionary format
            jd_skills = jd_summary.get('skills', [])
        else:
            jd_skills = []
        
        # Create keyword suggestions based on the actual analysis
        keywords = []
        for skill in jd_skills[:5]:  # Top 5 skills
            keywords.append({
                'keyword': skill.get('name', 'Unknown Skill'),
                'importance': f"{skill.get('category', 'Technical')} - {skill.get('frequency', 'High')} priority",
                'placement': 'Skills section',
                'bullet_points': [
                    {
                        'point': f"Demonstrated {skill.get('name', 'skill')} in previous roles",
                        'explanation': f"Add specific examples of {skill.get('name', 'skill')} usage"
                    }
                ]
            })
        
        # If no skills found, provide generic suggestions
        if not keywords:
            keywords = [
                {
                    'keyword': 'Technical Skills',
                    'importance': 'High - Core requirement',
                    'placement': 'Skills section',
                    'bullet_points': [
                        {
                            'point': 'Add specific technical skills from job description',
                            'explanation': 'Focus on skills mentioned in the job requirements'
                        }
                    ]
                }
            ]
        
        response_data = {
            'keyword_suggestions': {
                'keywords': keywords,
                'experience_gap_analysis': f"Analysis completed with {analysis_result.get('recommendations_count', 0)} recommendations",
                'overall_strategy': 'Review the improvement plan for specific action items'
            }
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Keyword suggestion failed: {str(e)}")
        return jsonify({
            'error': 'Failed to analyze resume',
            'message': str(e)
        }), 500

# ============================================================================
# FILE MANAGEMENT ENDPOINTS
# ============================================================================

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    """Download enhanced resume files"""
    try:
        # Check if file exists in resumes folder
        file_path = os.path.join(app.config['RESUMES_FOLDER'], filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        # Determine content type
        if filename.endswith('.pdf'):
            mimetype = 'application/pdf'
        elif filename.endswith('.docx'):
            mimetype = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        else:
            mimetype = 'application/octet-stream'
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype=mimetype
        )
        
    except Exception as e:
        logger.error(f"Download failed for {filename}: {str(e)}")
        return jsonify({'error': 'Download failed'}), 500

@app.route('/api/files', methods=['GET'])
def list_files():
    """List available files for download"""
    try:
        files = []
        resumes_dir = Path(app.config['RESUMES_FOLDER'])
        
        for file_path in resumes_dir.glob('*'):
            if file_path.is_file():
                files.append({
                    'filename': file_path.name,
                    'size': file_path.stat().st_size,
                    'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                    'type': file_path.suffix
                })
        
        return jsonify({
            'files': files,
            'total_count': len(files)
        })
        
    except Exception as e:
        logger.error(f"File listing failed: {str(e)}")
        return jsonify({'error': 'Failed to list files'}), 500

# ============================================================================
# USER PROFILE ENDPOINTS
# ============================================================================

@app.route('/api/user/profile', methods=['GET'])
def get_user_profile():
    """Get user profile information"""
    # Placeholder - integrate with your auth system
    return jsonify({
        'user_id': 'user_123',
        'email': 'user@example.com',
        'name': 'Test User',
        'created_at': datetime.now().isoformat()
    })

@app.route('/api/user/profile', methods=['PUT'])
def update_user_profile():
    """Update user profile information"""
    try:
        data = request.get_json()
        # Placeholder - integrate with your auth system
        return jsonify({
            'message': 'Profile updated successfully',
            'updated_fields': list(data.keys())
        })
    except Exception as e:
        return jsonify({'error': 'Profile update failed'}), 500

# ============================================================================
# RESUME MANAGEMENT ENDPOINTS
# ============================================================================

@app.route('/api/resumes', methods=['GET'])
def list_user_resumes():
    """List user's resumes"""
    try:
        resumes = []
        resumes_dir = Path(app.config['RESUMES_FOLDER'])
        
        for file_path in resumes_dir.glob('*'):
            if file_path.is_file() and file_path.suffix in ['.pdf', '.docx']:
                resumes.append({
                    'id': str(uuid.uuid4()),
                    'filename': file_path.name,
                    'type': file_path.suffix,
                    'size': file_path.stat().st_size,
                    'uploaded_at': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                    'download_url': f"/api/download/{file_path.name}"
                })
        
        return jsonify({
            'resumes': resumes,
            'total_count': len(resumes)
        })
        
    except Exception as e:
        logger.error(f"Resume listing failed: {str(e)}")
        return jsonify({'error': 'Failed to list resumes'}), 500

@app.route('/api/resumes/<filename>', methods=['DELETE'])
def delete_resume(filename):
    """Delete a user's resume"""
    try:
        file_path = os.path.join(app.config['RESUMES_FOLDER'], filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'Resume not found'}), 404
        
        os.remove(file_path)
        
        return jsonify({
            'message': 'Resume deleted successfully',
            'deleted_file': filename
        })
        
    except Exception as e:
        logger.error(f"Resume deletion failed: {str(e)}")
        return jsonify({'error': 'Failed to delete resume'}), 500

# ============================================================================
# WORKFLOW STATUS ENDPOINTS
# ============================================================================

@app.route('/api/status/<request_id>', methods=['GET'])
def get_workflow_status(request_id):
    """Get workflow status for a specific request"""
    # Placeholder - implement actual workflow tracking
    return jsonify({
        'request_id': request_id,
        'status': 'completed',  # or 'processing', 'failed'
        'progress': 100,
        'message': 'Workflow completed successfully'
    })

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(413)
def file_too_large(error):
    return jsonify({'error': 'File too large. Maximum size is 16MB'}), 413

# ============================================================================
# MAIN APPLICATION
# ============================================================================

if __name__ == '__main__':
    logger.info("Starting unified Resume Helper API...")
    logger.info(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
    logger.info(f"Resumes folder: {app.config['RESUMES_FOLDER']}")
    
    # Run the app
    port = int(os.environ.get('PORT', 5001))
    logger.info(f"Starting app on port {port}")
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,  # Set to False for production
        threaded=True
    )
