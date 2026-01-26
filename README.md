# 🚀 Resume Helper App

An intelligent, **agentic AI-powered** resume enhancement platform that helps job seekers optimize their resumes for specific job descriptions. Built on a sophisticated **multi-agent system architecture**, the app employs specialized autonomous AI agents that collaborate to analyze resumes, identify skill gaps, and automatically enhance content while preserving professional formatting. Each agent operates independently with domain expertise, working together through orchestrated workflows to deliver intelligent, context-aware resume improvements.

## ✨ Features

### 🎯 Core Capabilities

- **Smart Resume Enhancement** - Automatically enhances your resume based on job descriptions
- **Keyword Suggestions** - Get AI-powered keyword recommendations to improve ATS compatibility
- **Resume Analysis** - Analyze your resume structure, ATS score, and keyword matching
- **Gap Analysis** - Identify missing skills and experience compared to job requirements
- **Professional Formatting** - Maintains your resume's original formatting and appearance
- **Multiple Formats** - Supports DOCX input and generates both DOCX and PDF outputs

### 🔍 Analysis Tools

- **Resume Structure Analysis** - Get detailed feedback on resume structure and ATS compatibility
- **Keyword Analysis** - Analyze existing keywords and match percentage against job categories
- **Length Analysis** - Check if your resume length is optimal
- **Industry-Specific Insights** - Get tailored recommendations based on job category

## 🏗️ Architecture

The application follows a modern, modular architecture:

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
│  - Material-UI Components                               │
│  - Firebase Authentication                              │
│  - Real-time Status Updates                             │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Backend API (Flask)                         │
│  - RESTful Endpoints                                    │
│  - File Upload/Download                                 │
│  - Workflow Orchestration                               │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              AI Agent Services                           │
│  ├── Resume Parser Agent                                │
│  ├── Job Description Parser Agent                       │
│  ├── Gap Analyzer Agent                                 │
│  ├── Document Editor Agent                              │
│  └── Structure Tagger Agent                             │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              LLM Integration Layer                       │
│  - Anthropic Claude (Primary)                           │
│  - OpenAI GPT (Fallback)                                │
│  - Unified LLM Client                                   │
└─────────────────────────────────────────────────────────┘
```

## 🤖 Agentic Architecture

This application is built on a **true agentic AI system** - a sophisticated multi-agent architecture where specialized autonomous agents collaborate to accomplish complex resume enhancement tasks. Unlike traditional single-model approaches, this system employs multiple intelligent agents, each with distinct capabilities and responsibilities, working together through orchestrated workflows.

### Multi-Agent System

The platform implements a **multi-agent system (MAS)** where five specialized AI agents work autonomously and collaboratively:

1. **Resume Parser Agent** - An autonomous agent that intelligently extracts structured data from unstructured resume documents. It uses advanced NLP techniques to identify sections, roles, achievements, and skills, building a comprehensive ResumeAST (Abstract Syntax Tree) representation.

2. **Job Description Parser Agent** - A specialized agent that analyzes job descriptions to extract must-have skills, nice-to-have skills, responsibilities, and seniority levels. This agent creates structured JDSummary objects that serve as enhancement targets.

3. **Gap Analyzer Agent** - An intelligent agent that performs comparative analysis between the resume and job description. It autonomously identifies skill gaps, missing experience, and improvement opportunities, generating actionable enhancement plans.

4. **Structure Tagger Agent** - A document understanding agent that classifies document structure and content types. It uses dynamic pattern recognition to tag paragraphs, sections, and elements, enabling precise document manipulation.

5. **Document Editor Agent** - An autonomous editing agent that applies enhancements while preserving formatting. It intelligently maps content to document locations and performs surgical edits without disrupting the professional appearance.

### Agent Orchestration

The **ResumeEnhancementOrchestrator** serves as the central agent coordinator, managing the entire agentic workflow:

- **Sequential Agent Execution** - Orchestrates agents in optimal order, ensuring each agent receives the necessary inputs from previous agents
- **Agent Communication** - Facilitates data flow between agents through structured contracts and data models
- **Error Recovery** - Implements fallback mechanisms when individual agents encounter issues
- **Workflow Management** - Tracks progress and manages the complete enhancement pipeline

### Agentic Capabilities

**Autonomous Decision Making:**
- Each agent makes independent decisions about how to process its assigned task
- Agents adapt their behavior based on document structure and content patterns
- Dynamic prompt generation based on detected patterns

**Agent Collaboration:**
- Agents share structured data through well-defined contracts (ResumeAST, JDSummary, Plan)
- Collaborative problem-solving where agents build upon each other's outputs
- Cross-agent validation and consistency checking

**Intelligent Agent Behavior:**
- **Anti-Hallucination Systems** - Agents validate content to prevent generating fake information
- **Fallback Mechanisms** - Rule-based classification when LLM-based agents fail
- **Context Awareness** - Agents understand document context and maintain formatting integrity
- **Adaptive Processing** - Agents adjust strategies based on document complexity

**Agentic Workflow:**
```
User Request → Orchestrator
    ↓
[Agent 1: JD Parser] → JDSummary
    ↓
[Agent 2: Resume Parser] → ResumeAST
    ↓
[Agent 3: Gap Analyzer] → Enhancement Plan
    ↓
[Agent 4: Structure Tagger] → Document Tags
    ↓
[Agent 5: Document Editor] → Enhanced Resume
    ↓
Orchestrator → Final Output
```

### Agent Specialization

Each agent is a **specialized intelligent agent** with domain expertise:

- **Domain-Specific Knowledge** - Each agent understands its specific domain (parsing, analysis, editing)
- **Task-Oriented Design** - Agents are optimized for their specific responsibilities
- **Reusable Agent Components** - Agents can be reused across different workflows
- **Modular Agent Architecture** - Easy to add new agents or modify existing ones

### Agentic AI Features

- **Autonomous Processing** - Agents work independently without constant human intervention
- **Intelligent Routing** - Orchestrator routes tasks to appropriate agents
- **Agent State Management** - Tracks agent progress and intermediate results
- **Multi-Provider LLM Support** - Agents can leverage different LLM providers (Anthropic, OpenAI) based on task requirements
- **Quality-Based Agent Selection** - Different agents use different LLM quality levels (fast, balanced, quality) based on task criticality

This agentic architecture enables the system to handle complex, multi-step resume enhancement tasks that would be impossible with a single monolithic AI model, providing more accurate, reliable, and maintainable results.

## 🛠️ Tech Stack

### Frontend
- **React 18** - Modern UI framework
- **Material-UI (MUI)** - Component library
- **Firebase** - Authentication and hosting
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Animation library

### Backend
- **Flask** - Python web framework
- **Python 3.9+** - Runtime environment
- **python-docx** - DOCX document processing
- **PyPDF2** - PDF processing
- **LibreOffice** - PDF conversion
- **Anthropic SDK** - Claude AI integration
- **OpenAI SDK** - GPT integration

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 16+** - [Download Node.js](https://nodejs.org/)
- **npm or yarn** - Package managers
- **LibreOffice** - For PDF conversion (optional, for local development)
- **Anthropic API Key** - [Get API Key](https://console.anthropic.com/)
- **OpenAI API Key** (Optional) - [Get API Key](https://platform.openai.com/)
- **Firebase Account** - For authentication and hosting

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd resume_helper_app
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd resume_helper_backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create a .env file or export variables:
export ANTHROPIC_API_KEY=your_anthropic_api_key
export OPENAI_API_KEY=your_openai_api_key  # Optional
export FLASK_ENV=development
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd resume_helper_frontend

# Install dependencies
npm install

# Set up environment variables
# Create a .env file in the frontend directory:
REACT_APP_API_BASE_URL=http://localhost:5001
REACT_APP_FIREBASE_API_KEY=your_firebase_api_key
REACT_APP_FIREBASE_PROJECT_ID=your_firebase_project_id
REACT_APP_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
```

### 4. Run the Application

**Terminal 1 - Start Backend:**
```bash
cd resume_helper_backend
python start_api.py
# Or: python app.py
```

The backend will start on `http://localhost:5001`

**Terminal 2 - Start Frontend:**
```bash
cd resume_helper_frontend
npm start
```

The frontend will start on `http://localhost:3000`

## 📖 Usage Guide

### For End Users

#### 1. **Sign Up / Login**
   - Visit the application URL
   - Sign up with Google or email/password
   - Complete your profile

#### 2. **Resume Enhancement**
   - Click on "Smart Resume Analyzer"
   - Upload your resume (DOCX format)
   - Paste the job description
   - Click "Enhance Resume"
   - Wait for processing (typically 30-60 seconds)
   - Download your enhanced resume (DOCX or PDF)

#### 3. **Keyword Suggestions**
   - Click on "Smart Resume Analyzer"
   - Upload your resume
   - Paste the job description
   - Click "Get Keyword Suggestions"
   - Review categorized keyword recommendations
   - Copy keywords to clipboard

#### 4. **Resume Analysis**
   - Click on "Resume Structure Analysis"
   - Upload your resume
   - View ATS score, structure analysis, and recommendations

### For Developers

#### API Endpoints

**Health Check**
```bash
GET /health
```

**Resume Enhancement**
```bash
POST /api/enhance-resume
Content-Type: multipart/form-data

Form Data:
- resume_file: (file) Your resume DOCX file
- job_description: (string) Job description text
```

**Resume Analysis (No Enhancement)**
```bash
POST /api/analyze-resume
Content-Type: multipart/form-data

Form Data:
- resume_file: (file) Your resume DOCX file
- job_description: (string) Job description text
```

**Keyword Suggestions**
```bash
POST /suggest_keywords
Content-Type: multipart/form-data

Form Data:
- resume: (file) Your resume DOCX file
- job_description: (string) Job description text
```

**Download Enhanced Files**
```bash
GET /api/download/<filename>
```

**Workflow Status**
```bash
GET /api/status/<request_id>
```

#### Example API Usage

**Using cURL:**
```bash
# Enhance Resume
curl -X POST http://localhost:5001/api/enhance-resume \
  -F "resume_file=@your_resume.docx" \
  -F "job_description=Software Engineer position requiring Python, React, and AWS experience"
```

**Using Python:**
```python
import requests

with open('resume.docx', 'rb') as f:
    response = requests.post(
        'http://localhost:5001/api/enhance-resume',
        files={'resume_file': f},
        data={'job_description': 'Software Engineer position...'}
    )
    
result = response.json()
print(f"Request ID: {result['request_id']}")
print(f"Status: {result['status']}")
```

## 📁 Project Structure

```
resume_helper_app/
├── resume_helper_backend/          # Backend Flask API
│   ├── app.py                      # Main Flask application
│   ├── start_api.py                # Startup script
│   ├── services/                   # Core services
│   │   ├── orchestrator.py         # Workflow orchestration
│   │   ├── llm_client.py           # LLM integration
│   │   ├── agents/                 # AI agents
│   │   │   ├── resume_parser_agent.py
│   │   │   ├── jd_parser_agent.py
│   │   │   ├── gap_analyzer_agent.py
│   │   │   ├── document_editor_agent.py
│   │   │   └── structure_tagger_agent.py
│   │   ├── contracts/              # Data models
│   │   └── utils/                  # Utilities
│   ├── config/                     # Configuration
│   │   └── llm_config.py           # LLM settings
│   ├── uploads/                    # Temporary uploads
│   ├── resumes/                    # Enhanced resume outputs
│   └── requirements.txt            # Python dependencies
│
├── resume_helper_frontend/         # Frontend React App
│   ├── src/
│   │   ├── components/             # React components
│   │   │   ├── home.js             # Home page
│   │   │   ├── ResumeEnhancer.js   # Main enhancement UI
│   │   │   ├── SuggestKeywords.js  # Keyword suggestions
│   │   │   ├── AnalyzeResumeStructure.js
│   │   │   └── ...
│   │   ├── config/                 # Configuration
│   │   │   └── api.js              # API endpoints
│   │   ├── firebase.js             # Firebase config
│   │   └── App.js                  # Main app component
│   ├── public/                     # Static files
│   └── package.json                # Node dependencies
│
├── CODEBASE_INDEX.md               # Detailed codebase reference
├── DEPLOYMENT.md                   # Deployment guide
└── README.md                       # This file
```

## 🔧 Configuration

### Backend Environment Variables

```bash
# Required
ANTHROPIC_API_KEY=your_anthropic_api_key

# Optional
OPENAI_API_KEY=your_openai_api_key
FLASK_ENV=development|production
SECRET_KEY=your_secret_key
```

### Frontend Environment Variables

```bash
# API Configuration
REACT_APP_API_BASE_URL=http://localhost:5001

# Firebase Configuration
REACT_APP_FIREBASE_API_KEY=your_firebase_api_key
REACT_APP_FIREBASE_PROJECT_ID=your_firebase_project_id
REACT_APP_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
REACT_APP_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
REACT_APP_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
REACT_APP_FIREBASE_APP_ID=your_app_id
```

## 🧪 Testing

### Backend Tests

```bash
cd resume_helper_backend
python test_api_endpoints.py
```

### Frontend Tests

```bash
cd resume_helper_frontend
npm test
```

## 🚀 Deployment

### Backend Deployment

The backend can be deployed using:

1. **Gunicorn** (Recommended for production)
   ```bash
   gunicorn -c gunicorn_config.py app:app
   ```

2. **Docker**
   ```bash
   docker build -t resume-helper-backend .
   docker run -p 5001:5001 -e ANTHROPIC_API_KEY=xxx resume-helper-backend
   ```

3. **Platform-as-a-Service** (Render, Heroku, etc.)
   - See `DEPLOYMENT.md` for detailed instructions

### Frontend Deployment

**Firebase Hosting:**
```bash
cd resume_helper_frontend
npm run build
firebase deploy --only hosting
```

**Other Platforms:**
- Build the app: `npm run build`
- Deploy the `build/` folder to your hosting service

## 🔒 Security Features

- **File Type Validation** - Only accepts DOCX files
- **File Size Limits** - Maximum 16MB per file
- **Secure Filenames** - Prevents path traversal attacks
- **CORS Configuration** - Restricted to allowed origins
- **Firebase Authentication** - Secure user authentication
- **Input Validation** - Comprehensive request validation

## 🐛 Troubleshooting

### Common Issues

**Backend won't start:**
- Check if port 5001 is available: `lsof -ti:5001 | xargs kill -9`
- Verify environment variables are set
- Ensure all dependencies are installed: `pip install -r requirements.txt`

**Frontend won't connect to backend:**
- Verify `REACT_APP_API_BASE_URL` is correct
- Check CORS configuration in backend
- Ensure backend is running on the correct port

**LLM API errors:**
- Verify API keys are valid and have sufficient credits
- Check API rate limits
- Review logs for specific error messages

**File upload issues:**
- Ensure file is DOCX format
- Check file size is under 16MB
- Verify file is not corrupted

**PDF conversion fails:**
- Install LibreOffice: `brew install --cask libreoffice` (macOS)
- For production, use a service with LibreOffice pre-installed

## 📚 Additional Documentation

- **[CODEBASE_INDEX.md](./CODEBASE_INDEX.md)** - Detailed codebase reference for developers
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Comprehensive deployment guide
- **[API_README.md](./resume_helper_backend/API_README.md)** - API documentation
- **[README_UNIFIED_API.md](./resume_helper_backend/README_UNIFIED_API.md)** - Unified API guide

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 🙏 Acknowledgments

- **Anthropic** - For Claude AI API
- **OpenAI** - For GPT API
- **Material-UI** - For React components
- **Firebase** - For authentication and hosting

## 📞 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check existing documentation
- Review logs for error details

---

**Made with ❤️ for job seekers everywhere**

