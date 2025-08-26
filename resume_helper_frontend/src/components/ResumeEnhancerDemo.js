import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  TextField,
  Alert,
  CircularProgress,
  Paper,
  Grid,
  Chip,
  Divider
} from '@mui/material';
import { PlayArrow as PlayIcon, Download as DownloadIcon } from '@mui/icons-material';
import axios from 'axios';
import API_CONFIG from '../config/api';

const ResumeEnhancerDemo = () => {
  const [jobDescription, setJobDescription] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  // Sample job description for testing
  const sampleJD = `Software Engineer - Backend Development

We are looking for a talented Software Engineer to join our backend development team. The ideal candidate will have:

Required Skills:
- Python programming experience
- Experience with cloud platforms (AWS, Azure, or GCP)
- Knowledge of microservices architecture
- Experience with databases (PostgreSQL, MongoDB)
- Understanding of RESTful APIs and GraphQL
- Experience with Docker and Kubernetes
- Knowledge of CI/CD pipelines

Nice to Have:
- Experience with message queues (Kafka, RabbitMQ)
- Knowledge of Elasticsearch
- Experience with monitoring tools (Prometheus, Grafana)
- Understanding of distributed systems
- Experience with Terraform or similar IaC tools

Responsibilities:
- Design and implement scalable backend services
- Optimize database queries and performance
- Implement security best practices
- Collaborate with frontend and DevOps teams
- Participate in code reviews and technical discussions

This is a senior-level position requiring 3+ years of experience in backend development.`;

  const handleSampleJD = () => {
    setJobDescription(sampleJD);
  };

  const handleClear = () => {
    setJobDescription('');
    setResults(null);
    setError(null);
  };

  const testEnhancement = async () => {
    if (!jobDescription.trim()) {
      setError('Please provide a job description first');
      return;
    }

    setIsProcessing(true);
    setError(null);
    setResults(null);

    try {
      // Test the analyze-resume endpoint (no file upload needed)
      const response = await axios.post(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.ANALYZE_RESUME}`, {
        job_description: jobDescription,
        // Note: This endpoint expects a file, so we'll get an error
        // but it's good for testing the API connection
      }, {
        headers: {
          'Content-Type': 'application/json',
        },
        timeout: API_CONFIG.TIMEOUT,
      });

      setResults(response.data);
    } catch (err) {
      if (err.response?.status === 400 && err.response?.data?.message?.includes('resume file')) {
        // Expected error - API is working but needs file
        setResults({
          success: true,
          message: 'API Connection Successful!',
          note: 'The API is working correctly. The error above is expected since we didn\'t upload a resume file.',
          api_status: 'Connected',
          endpoint: `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.ANALYZE_RESUME}`,
          timestamp: new Date().toISOString()
        });
      } else {
        setError(err.response?.data?.message || 'API test failed. Please check if the backend is running.');
      }
    } finally {
      setIsProcessing(false);
    }
  };

  const testHealthCheck = async () => {
    try {
      const response = await axios.get(`${API_CONFIG.BASE_URL}/health`);
      setResults({
        success: true,
        message: 'Health Check Successful!',
        api_status: 'Healthy',
        endpoint: `${API_CONFIG.BASE_URL}/health`,
        response: response.data,
        timestamp: new Date().toISOString()
      });
      setError(null);
    } catch (err) {
      setError(`Health check failed: ${err.message}`);
      setResults(null);
    }
  };

  return (
    <Box sx={{ maxWidth: 1000, mx: 'auto', p: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom align="center" color="primary">
        Resume Enhancer API Demo
      </Typography>
      <Typography variant="h6" component="h2" gutterBottom align="center" color="text.secondary" sx={{ mb: 4 }}>
        Test the API integration and see how the enhancement workflow works
      </Typography>

      <Grid container spacing={3}>
        {/* API Configuration Display */}
        <Grid item xs={12} md={4}>
          <Card elevation={2}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                🔧 API Configuration
              </Typography>
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  Base URL:
                </Typography>
                <Chip 
                  label={API_CONFIG.BASE_URL} 
                  color="primary" 
                  variant="outlined"
                  sx={{ fontFamily: 'monospace' }}
                />
              </Box>
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  Timeout:
                </Typography>
                <Chip 
                  label={`${API_CONFIG.TIMEOUT / 1000}s`} 
                  color="secondary" 
                  variant="outlined"
                />
              </Box>
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  Max File Size:
                </Typography>
                <Chip 
                  label={`${API_CONFIG.MAX_FILE_SIZE / (1024 * 1024)}MB`} 
                  color="info" 
                  variant="outlined"
                />
              </Box>
              
              <Divider sx={{ my: 2 }} />
              
              <Button
                variant="outlined"
                fullWidth
                onClick={testHealthCheck}
                startIcon={<PlayIcon />}
              >
                Test Health Check
              </Button>
            </CardContent>
          </Card>
        </Grid>

        {/* Job Description Input */}
        <Grid item xs={12} md={8}>
          <Card elevation={2}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">
                  📝 Job Description
                </Typography>
                <Box>
                  <Button
                    size="small"
                    onClick={handleSampleJD}
                    sx={{ mr: 1 }}
                  >
                    Load Sample
                  </Button>
                  <Button
                    size="small"
                    onClick={handleClear}
                    color="secondary"
                  >
                    Clear
                  </Button>
                </Box>
              </Box>
              
              <TextField
                fullWidth
                multiline
                rows={12}
                label="Job Description"
                placeholder="Paste the job description here..."
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                variant="outlined"
                helperText="Provide a detailed job description to test the enhancement workflow"
              />
              
              <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
                <Button
                  variant="contained"
                  onClick={testEnhancement}
                  disabled={!jobDescription.trim() || isProcessing}
                  startIcon={isProcessing ? <CircularProgress size={20} /> : <PlayIcon />}
                >
                  {isProcessing ? 'Testing...' : 'Test Enhancement API'}
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Results Display */}
        {results && (
          <Grid item xs={12}>
            <Card elevation={2}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  ✅ API Test Results
                </Typography>
                
                <Paper elevation={1} sx={{ p: 2, mb: 2, backgroundColor: 'success.light' }}>
                  <Typography variant="body1" color="success.contrastText">
                    {results.message}
                  </Typography>
                </Paper>

                <Grid container spacing={2}>
                  <Grid item xs={12} md={6}>
                    <Typography variant="body2" color="text.secondary">
                      API Status:
                    </Typography>
                    <Chip 
                      label={results.api_status} 
                      color="success" 
                      sx={{ mb: 1 }}
                    />
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <Typography variant="body2" color="text.secondary">
                      Endpoint:
                    </Typography>
                    <Typography variant="body2" sx={{ fontFamily: 'monospace', fontSize: '0.8rem' }}>
                      {results.endpoint}
                    </Typography>
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <Typography variant="body2" color="text.secondary">
                      Timestamp:
                    </Typography>
                    <Typography variant="body2">
                      {new Date(results.timestamp).toLocaleString()}
                    </Typography>
                  </Grid>
                </Grid>

                {results.note && (
                  <Alert severity="info" sx={{ mt: 2 }}>
                    {results.note}
                  </Alert>
                )}

                {results.response && (
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      Health Check Response:
                    </Typography>
                    <Paper elevation={1} sx={{ p: 2, backgroundColor: 'grey.50' }}>
                      <pre style={{ margin: 0, fontSize: '0.8rem', overflow: 'auto' }}>
                        {JSON.stringify(results.response, null, 2)}
                      </pre>
                    </Paper>
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>
        )}

        {/* Error Display */}
        {error && (
          <Grid item xs={12}>
            <Alert severity="error" onClose={() => setError(null)}>
              {error}
            </Alert>
          </Grid>
        )}

        {/* Instructions */}
        <Grid item xs={12}>
          <Card elevation={1}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                📋 How to Use This Demo
              </Typography>
              <Typography variant="body2" paragraph>
                1. <strong>Load Sample JD</strong>: Click "Load Sample" to populate a realistic job description
              </Typography>
              <Typography variant="body2" paragraph>
                2. <strong>Test Health Check</strong>: Verify the backend API is running and accessible
              </Typography>
              <Typography variant="body2" paragraph>
                3. <strong>Test Enhancement API</strong>: Test the enhancement endpoint (will show expected error without file)
              </Typography>
              <Typography variant="body2" paragraph>
                4. <strong>View Results</strong>: See API responses and connection status
              </Typography>
              
              <Divider sx={{ my: 2 }} />
              
              <Typography variant="body2" color="text.secondary">
                <strong>Note:</strong> This demo tests API connectivity. For full functionality, use the ResumeEnhancer component 
                which handles file uploads and complete workflow execution.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ResumeEnhancerDemo;
