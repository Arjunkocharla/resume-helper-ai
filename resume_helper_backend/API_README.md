# Resume Enhancement API

A Flask-based API that provides intelligent resume enhancement using AI agents. The system analyzes job descriptions, identifies skill gaps, and enhances resumes while preserving professional formatting.

## 🚀 Features

- **Intelligent Job Description Parsing** - Extracts skills, requirements, and seniority levels
- **Resume Analysis** - Parses and structures resume content
- **Gap Analysis** - Identifies missing skills and experience
- **Smart Enhancement** - Applies improvements while preserving formatting
- **Multiple Output Formats** - Generates both DOCX and PDF versions
- **Professional Quality** - Maintains resume appearance and structure

## 🏗️ Architecture

The API uses a modular agent-based architecture:

```
API Layer (Flask)
    ↓
Orchestrator Service
    ↓
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ JD Parser      │ Resume Parser   │ Gap Analyzer    │ Document Editor │
│ Agent          │ Agent           │ Agent           │ Agent           │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

## 📋 API Endpoints

### 1. Health Check
**GET** `/health`

Check if the service is running and ready.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-18T10:30:00",
  "orchestrator_ready": true
}
```

### 2. Resume Analysis (Analysis Only)
**POST** `/api/analyze-resume`

Analyze a resume against a job description without modifying files.

**Request:**
- `resume_file`: DOCX or PDF file (multipart/form-data)
- `job_description`: Text description of the job (form data)

**Response:**
```json
{
  "success": true,
  "message": "Resume analysis completed successfully",
  "analysis": {
    "jd_summary": {
      "must_have_skills": ["Python", "C++", "Linux"],
      "nice_to_have_skills": ["Rust", "Physics", "Motion Planning"],
      "seniority_level": "senior"
    },
    "resume_analysis": {
      "roles_count": 4,
      "bullets_count": 10,
      "skills_categories": 8
    },
    "improvement_plan": {
      "total_recommendations": 6,
      "recommendations": [
        {
          "type": "insert_bullet",
          "description": "Add new bullet: Developed multi-agent autonomous systems..."
        }
      ]
    }
  },
  "timestamp": "2025-01-18T10:30:00"
}
```

### 3. Complete Resume Enhancement
**POST** `/api/enhance-resume`

Complete workflow: analyze, enhance, and save enhanced resume files.

**Request:**
- `resume_file`: DOCX or PDF file (multipart/form-data)
- `job_description`: Text description of the job (form data)

**Response:**
```json
{
  "success": true,
  "message": "Resume enhanced successfully",
  "request_id": "req_20250118_103000_abc123",
  "workflow_summary": {
    "jd_skills_analyzed": 11,
    "resume_roles_parsed": 4,
    "resume_bullets_parsed": 10,
    "improvements_generated": 6,
    "seniority_level": "senior"
  },
  "files": {
    "enhanced_docx": "/path/to/enhanced_resume.docx",
    "enhanced_pdf": "/path/to/enhanced_resume.pdf"
  },
  "download_endpoints": {
    "docx": "/api/download/enhanced_resume.docx",
    "pdf": "/api/download/enhanced_resume.pdf"
  },
  "timestamp": "2025-01-18T10:30:00"
}
```

### 4. Download Enhanced Files
**GET** `/api/download/<filename>`

Download enhanced resume files (DOCX or PDF).

**Parameters:**
- `filename`: Name of the file to download

**Response:** File download

### 5. Workflow Status
**GET** `/api/status/<request_id>`

Check the status of a specific workflow request.

**Parameters:**
- `request_id`: Unique identifier from enhancement request

**Response:**
```json
{
  "request_id": "req_20250118_103000_abc123",
  "status": "completed",
  "timestamp": "2025-01-18T10:30:00"
}
```

## 🛠️ Setup and Installation

### Prerequisites
- Python 3.9+
- Anthropic API key
- LibreOffice (for PDF conversion)

### Installation
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd resume_helper_app/resume_helper_backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**
   ```bash
   # Create .env file
   echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
   ```

4. **Run the API**
   ```bash
   python resume_enhancement_api.py
   ```

The API will start on `http://localhost:5000`

## 📁 File Structure

```
resume_helper_backend/
├── resume_enhancement_api.py    # Main Flask API
├── services/                    # Core services
│   ├── orchestrator.py         # Workflow orchestration
│   ├── agents/                 # AI agents
│   ├── contracts/              # Data models
│   └── utils/                  # Utilities
├── resumes/                     # Enhanced resume outputs
├── uploads/                     # Temporary upload storage
└── requirements.txt             # Python dependencies
```

## 🔄 Workflow Process

### Analysis Only Workflow
1. **Upload resume** (DOCX/PDF)
2. **Provide job description**
3. **Receive analysis results**
4. **Get improvement recommendations**

### Complete Enhancement Workflow
1. **Upload resume** (DOCX/PDF)
2. **Provide job description**
3. **System analyzes gaps**
4. **Applies improvements**
5. **Generates enhanced files**
6. **Saves to resumes folder**
7. **Returns download links**

## 📊 Example Usage

### Using cURL

**Resume Analysis:**
```bash
curl -X POST http://localhost:5000/api/analyze-resume \
  -F "resume_file=@resume.docx" \
  -F "job_description=Software Engineer position requiring Python and cloud experience"
```

**Complete Enhancement:**
```bash
curl -X POST http://localhost:5000/api/enhance-resume \
  -F "resume_file=@resume.docx" \
  -F "job_description=Software Engineer position requiring Python and cloud experience"
```

### Using Python Requests

```python
import requests

# Resume Analysis
with open('resume.docx', 'rb') as f:
    response = requests.post(
        'http://localhost:5000/api/analyze-resume',
        files={'resume_file': f},
        data={'job_description': 'Software Engineer position...'}
    )
    
if response.status_code == 200:
    result = response.json()
    print(f"Recommendations: {result['analysis']['improvement_plan']['total_recommendations']}")
```

## 🎯 Key Benefits

- **Targeted Enhancement** - Resumes are tailored to specific job requirements
- **Professional Quality** - Maintains formatting and appearance
- **Intelligent Analysis** - Uses AI to identify skill gaps and opportunities
- **Multiple Formats** - Supports both DOCX and PDF
- **Scalable Architecture** - Modular design for easy extension

## 🚨 Error Handling

The API includes comprehensive error handling:

- **400 Bad Request** - Missing or invalid input
- **413 Payload Too Large** - File exceeds 16MB limit
- **500 Internal Server Error** - Processing failures
- **503 Service Unavailable** - Orchestrator not ready

## 🔒 Security Features

- **File Type Validation** - Only accepts DOCX and PDF files
- **File Size Limits** - Maximum 16MB per file
- **Secure Filenames** - Prevents path traversal attacks
- **Download Restrictions** - Only allows downloads from resumes directory

## 📈 Performance

- **Asynchronous Processing** - Non-blocking file operations
- **Efficient Parsing** - Optimized document processing
- **Memory Management** - Streams large files without loading into memory
- **Caching** - Reuses parsed data when possible

## 🧪 Testing

Run the test script to verify all endpoints:

```bash
python test_api_endpoints.py
```

This will test:
- Health check endpoint
- Resume analysis endpoint
- Complete enhancement endpoint
- File download functionality

## 🚀 Production Deployment

For production deployment:

1. **Use Gunicorn** instead of Flask development server
2. **Set up proper logging** and monitoring
3. **Configure environment variables** securely
4. **Set up file storage** (S3, etc.) for production
5. **Add authentication** and rate limiting
6. **Set up health checks** and monitoring

## 📞 Support

For issues or questions:
- Check the logs for detailed error information
- Verify the orchestrator is properly initialized
- Ensure all required dependencies are installed
- Check that the Anthropic API key is valid

## 🔄 Version History

- **v1.0** - Initial API with basic enhancement workflow
- **v1.1** - Added analysis-only endpoint
- **v1.2** - Enhanced error handling and validation
- **v1.3** - Added workflow status tracking
