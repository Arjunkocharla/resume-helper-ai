# 🚀 Unified Resume Helper API

This is the **centralized, unified API** that consolidates all Resume Helper functionality into a single Flask application.

## 🎯 What This Solves

**Before (Chaos):**
- `resume_enhancement_api.py` - Resume enhancement endpoints
- `user_info_apis.py` - User profile/resume management  
- `resume_analyzer.py` - Another enhancement API (duplicate!)
- Multiple ports, different configurations, scattered endpoints
- Hard to test, deploy, and maintain

**After (Unified):**
- **Single `app.py`** with all endpoints
- **One port (5001)** for everything
- **Centralized configuration** and error handling
- **Easy testing and deployment**

## 🚀 Quick Start

### Option 1: Simple Startup (Recommended)
```bash
cd resume_helper_backend
python start_api.py
```

### Option 2: Direct Flask
```bash
cd resume_helper_backend
python app.py
```

### Option 3: With Virtual Environment
```bash
cd resume_helper_backend
source venv/bin/activate  # or your venv path
python app.py
```

## 🌐 API Endpoints

### Health & Status
- `GET /health` - Health check
- `GET /api/status` - API status and endpoints

### Resume Enhancement
- `POST /api/enhance-resume` - Main enhancement endpoint
- `POST /api/analyze-resume` - Analysis without enhancement

### File Management
- `GET /api/download/<filename>` - Download enhanced files
- `GET /api/files` - List available files
- `GET /api/resumes` - List user resumes
- `DELETE /api/resumes/<filename>` - Delete resume

### User Management
- `GET /api/user/profile` - Get user profile
- `PUT /api/user/profile` - Update user profile

### Workflow Status
- `GET /api/status/<request_id>` - Get workflow status

## 📁 File Structure

```
resume_helper_backend/
├── app.py                    # 🎯 MAIN UNIFIED API
├── start_api.py             # 🚀 Easy startup script
├── services/                 # Your existing services
│   ├── orchestrator.py
│   ├── agents/
│   └── contracts/
├── uploads/                  # Temporary uploads
├── resumes/                  # Enhanced resumes output
└── README_UNIFIED_API.md    # This file
```

## 🔧 Configuration

The API automatically:
- ✅ Creates `uploads/` and `resumes/` directories
- ✅ Sets 16MB file size limit
- ✅ Enables CORS for frontend (localhost:3000)
- ✅ Handles PDF and DOCX files
- ✅ Generates unique filenames with timestamps

## 🧪 Testing

### Health Check
```bash
curl http://localhost:5001/health
```

### API Status
```bash
curl http://localhost:5001/api/status
```

### Test Enhancement (with file)
```bash
curl -X POST http://localhost:5001/api/enhance-resume \
  -F "resume_file=@your_resume.docx" \
  -F "job_description=Your job description here"
```

## 🚨 Error Handling

The API includes comprehensive error handling:
- ✅ File validation (type, size)
- ✅ Input validation
- ✅ Proper HTTP status codes
- ✅ Detailed error messages
- ✅ Logging for debugging

## 🔄 Migration from Old APIs

### Old: Multiple API files
```bash
# Don't do this anymore!
python resume_enhancement_api.py  # Port 5001
python user_info_apis.py         # Port 5002  
python resume_analyzer.py        # Port 5003
```

### New: Single unified API
```bash
# Do this instead!
python start_api.py  # Everything on port 5001
```

## 🎨 Frontend Integration

Update your frontend API config to use the unified endpoints:

```javascript
// Old scattered endpoints
const API_ENDPOINTS = {
  enhance: 'http://localhost:5001/api/enhance-resume',
  analyze: 'http://localhost:5002/api/analyze-resume',  // ❌ Wrong port!
  user: 'http://localhost:5003/api/user/profile'        // ❌ Wrong port!
}

// New unified endpoints
const API_ENDPOINTS = {
  enhance: 'http://localhost:5001/api/enhance-resume',
  analyze: 'http://localhost:5001/api/analyze-resume',  // ✅ Same port!
  user: 'http://localhost:5001/api/user/profile'        // ✅ Same port!
}
```

## 🚀 Benefits

1. **Single Command**: `python start_api.py` starts everything
2. **One Port**: All APIs on port 5001
3. **Centralized Config**: Easy to modify settings
4. **Better Testing**: Test all endpoints together
5. **Easier Deployment**: One service to deploy
6. **Consistent Error Handling**: Same error format everywhere
7. **Better Logging**: Centralized logging and monitoring

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill any existing processes on port 5001
lsof -ti:5001 | xargs kill -9
```

### Missing Dependencies
```bash
pip install flask flask-cors anthropic python-docx PyPDF2
```

### Virtual Environment Issues
```bash
# Create new venv if needed
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 🎯 Next Steps

1. **Test the unified API**: `python start_api.py`
2. **Update frontend config** to use unified endpoints
3. **Delete old API files** (after confirming everything works)
4. **Deploy the unified API** to production

---

**🎉 You now have a clean, maintainable, and professional API structure!**
