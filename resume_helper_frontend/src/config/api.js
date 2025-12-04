// API Configuration
const API_CONFIG = {
  // Backend API base URL
  BASE_URL: process.env.REACT_APP_API_URL || 'https://resume-helper-api.onrender.com',
  
  // API endpoints
  ENDPOINTS: {
    ENHANCE_RESUME: '/api/enhance-resume',
    ANALYZE_RESUME: '/api/analyze-resume',
    SUGGEST_KEYWORDS: '/api/suggest-keywords',
    DOWNLOAD_FILE: '/api/download',
    WORKFLOW_STATUS: '/api/status',
    USER_PROFILE: '/api/user/profile',
    USER_RESUMES: '/api/user/resumes',
    UPLOAD_RESUME: '/api/user/resume',
  },
  
  // Request timeout (in milliseconds)
  TIMEOUT: 300000, // 5 minutes for long-running operations
  
  // File upload settings
  MAX_FILE_SIZE: 16 * 1024 * 1024, // 16MB
  ALLOWED_FILE_TYPES: ['.docx', '.pdf'],
  
  // Status polling interval (in milliseconds)
  STATUS_POLLING_INTERVAL: 2000, // 2 seconds
};

export default API_CONFIG;
