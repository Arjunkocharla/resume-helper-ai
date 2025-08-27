# Resume Helper App - Claude Development Index

## Project Architecture Overview

**Full-stack resume enhancement application using AI-powered analysis and optimization**

### Core Technologies
- **Backend**: Flask (Python 3.9+), Anthropic Claude API
- **Frontend**: React 18, Material-UI, Firebase Auth
- **Document Processing**: python-docx, PyPDF2, ReportLab
- **Storage**: Local filesystem, Firebase Auth
- **Deployment**: Gunicorn, Render.com

---

## Backend Structure (`resume_helper_backend/`)

### Main API Files
- `resume_analyzer.py` - Legacy resume analysis endpoints (14 routes)
- `resume_enhancement_api.py` - Modern orchestrator-based API (5 routes)
- `user_info_apis.py` - User profile management (6 routes)

### Services Architecture (`services/`)

#### Orchestrator System
- `orchestrator.py` - Main coordinator managing agent workflow
- **Data Flow**: Resume Upload → Parse → Analyze Gaps → Generate Plan → Apply Edits → Output

#### Agent System (`agents/`)
- `jd_parser_agent.py` - Extracts requirements from job descriptions
- `resume_parser_agent.py` - Converts resumes to structured AST
- `gap_analyzer_agent.py` - Identifies improvement opportunities  
- `document_editor_agent.py` - Applies edits while preserving formatting
- `structure_tagger_agent.py` - Adds semantic structure tags
- `evaluator_agent.py` - Validates improvements
- `llm_direct_editor_agent.py` - Direct LLM-based editing
- `skills_categorization_agent.py` - Categorizes and organizes skills

#### Data Contracts (`contracts/`)
- `resume_ast.py` - Resume Abstract Syntax Tree models
- `jd_summary.py` - Job description summary structures
- `plan.py` - Improvement plan and edit operations
- `diff.py` - Change tracking and comparison
- `verify.py` - Validation reports
- `registry.py` - Schema versioning and validation

#### Utilities (`utils/`)
- `pdf_converter.py` - PDF generation and conversion

---

## API Endpoints Reference

### Legacy APIs (`resume_analyzer.py`)
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/analyze_resume_structure` | POST | Analyzes resume sections and structure |
| `/analyze_keywords` | POST | Keyword matching against job descriptions |
| `/analyze_resume_length` | POST | Evaluates resume length and density |
| `/suggest_keywords` | POST | Suggests relevant keywords |
| `/upload_resume` | POST | File upload and basic processing |
| `/download_resume` | GET | Downloads processed resume |
| `/get_resume_download_url` | GET | Generates download URLs |
| `/apply_suggestions` | POST | Applies improvement suggestions |
| `/update_resumes` | POST | Updates resume content |
| `/update_resume_enhanced` | POST | Enhanced update with AI |
| `/update_resume_with_suggestions` | POST | Applies specific suggestions |
| `/inplace_resume_update` | POST | In-place content updates |
| `/structured_resume_update` | POST | Structured content modifications |
| `/enhance-resume` | POST | Full resume enhancement |

### Modern APIs (`resume_enhancement_api.py`)
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Service health check |
| `/api/enhance-resume` | POST | Orchestrator-based enhancement |
| `/api/analyze-resume` | POST | Comprehensive resume analysis |
| `/api/download/<filename>` | GET | File download with validation |
| `/api/status/<request_id>` | GET | Request status tracking |

### User APIs (`user_info_apis.py`)
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/user/profile` | GET/PUT | User profile management |
| `/api/user/resume` | POST | Resume upload and storage |
| `/api/user/resumes` | GET | List user's resumes |
| `/api/user/resume/<id>` | GET/DELETE | Individual resume management |

---

## Frontend Structure (`resume_helper_frontend/`)

### Core Files
- `App.js` - Main routing and authentication
- `firebase.js` - Firebase configuration
- `api.js` - API client functions

### Components (`components/`)
| Component | Route | Purpose |
|-----------|-------|---------|
| `Login.js` | `/login` | User authentication |
| `Signup.js` | `/signup` | User registration |
| `home.js` | `/home` | Main dashboard |
| `AnalyzeResumeLength.js` | `/analyze-length` | Length analysis tool |
| `AnalyzeKeywords.js` | `/analyze-keywords` | Keyword analysis |
| `SuggestKeywords.js` | `/suggest-keywords` | Keyword suggestions |
| `AnalyzeResumeStructure.js` | `/analyze-resume-structure` | Structure analysis |
| `UserProfileComponent.js` | `/profile` | User profile management |

### Key Dependencies
```json
"@mui/material": "^6.1.3"     // UI components
"firebase": "^10.14.0"        // Authentication
"axios": "^1.7.7"             // HTTP client
"react-router-dom": "^6.26.2" // Routing
"tailwindcss": "^3.4.13"      // Styling
```

---

## Key Dependencies (`requirements.txt`)

### Core Framework
- `flask==2.3.3` - Web framework
- `flask-cors==4.0.0` - CORS handling
- `gunicorn==21.0.0` - WSGI server

### AI/ML Libraries
- `anthropic==0.7.0` - Claude API client
- `openai==1.12.0` - OpenAI API client
- `langchain>=0.1.0` - LLM orchestration

### Document Processing
- `python-docx==0.8.11` - DOCX manipulation
- `PyPDF2>=3.0.1` - PDF processing
- `reportlab>=4.0.4` - PDF generation
- `pdfminer.six>=20240706` - PDF text extraction

### Cloud Storage
- `boto3>=1.26.137` - AWS S3
- `b2sdk>=1.24.0` - Backblaze B2

---

## File Organization

### Important Directories
- `resumes/` - Resume storage and processing
- `resumes/workflow_artifacts/` - AI workflow JSON files
- `uploads/` - Temporary file uploads
- `uploads/processed/` - Processed resume outputs
- `downloads/` - Generated files for download

### Configuration Files
- `render.yaml` - Render.com deployment config
- `gunicorn_config.py` - WSGI server configuration
- `firebase.json` - Firebase hosting config
- `resumehelperapp-firebase-adminsdk-*.json` - Firebase service account

---

## Environment Variables (Required)

```bash
ANTHROPIC_API_KEY=your_claude_api_key
OPENAI_API_KEY=your_openai_api_key  # Optional
FLASK_ENV=development|production
```

---

## Development Workflows

### Testing Commands
```bash
# Backend
python test_api_endpoints.py
python test_orchestrator_before_after.py
python test_document_editor_directly.py

# Frontend
npm test
npm run build
```

### Local Development
```bash
# Backend
cd resume_helper_backend
python resume_enhancement_api.py

# Frontend  
cd resume_helper_frontend
npm start
```

---

## Data Models (Key Contracts)

### ResumeAST
- Structured representation of resume content
- Hierarchical: Sections → Roles → Bullets
- Preserves formatting metadata

### JDSummary
- Extracted job requirements
- Skills, qualifications, seniority level
- Keyword importance scoring

### Plan
- Improvement recommendations
- Edit operations (insert, modify, upsert)
- Constraint validation

### Workflow Artifacts
- JSON files tracking AI decisions
- Stored in `resumes/workflow_artifacts/`
- Format: `{type}_req_{timestamp}_{id}.json`

---

## Security Considerations
- File upload validation (DOCX/PDF only)
- Secure filename handling
- Firebase authentication required
- No hardcoded API keys in repository

---

## Common Debugging Files
- `debug_document_structure.py` - Document parsing debugging
- `debug_docx_structure.py` - DOCX format analysis
- `debug_structure.py` - General structure debugging
- `debug_pdf_text.py` - PDF text extraction testing

---

*Generated: 2025-08-20*
*Claude Development Assistant Index v1.0*