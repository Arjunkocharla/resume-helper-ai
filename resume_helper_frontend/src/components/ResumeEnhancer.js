import React, { useState, useRef } from 'react';
import {
  Container, Typography, Button, TextField, Box, CircularProgress,
  Alert, IconButton, Tooltip, Grid, useTheme
} from '@mui/material';
import {
  CloudUpload as CloudUploadIcon,
  Description as DescriptionIcon,
  AutoAwesome as EnhanceIcon,
  Download as DownloadIcon,
  CheckCircle as CheckIcon,
  Refresh as RefreshIcon
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import API_CONFIG from '../config/api';

const ResumeEnhancer = () => {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentWorkflow, setCurrentWorkflow] = useState(null);
  const [workflowStatus, setWorkflowStatus] = useState(null);
  const [enhancementResults, setEnhancementResults] = useState(null);
  const [error, setError] = useState(null);
  
  const fileInputRef = useRef();
  const statusIntervalRef = useRef();
  const theme = useTheme();

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
      setResumeFile(selectedFile);
      setError('');
    } else {
      setError('Please upload a DOCX file only');
      setResumeFile(null);
    }
  };

  const handleJobDescriptionChange = (e) => {
    setJobDescription(e.target.value);
    setError('');
  };

  const startEnhancement = async () => {
    if (!resumeFile || !jobDescription.trim()) {
      setError('Please provide both a resume and job description');
      return;
    }

    setIsProcessing(true);
    setError(null);
    
    const formData = new FormData();
    formData.append('resume_file', resumeFile);
    formData.append('job_description', jobDescription);

    try {
      const response = await axios.post(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.ENHANCE_RESUME}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: API_CONFIG.TIMEOUT,
      });

      const { request_id, workflow_summary } = response.data;
      setCurrentWorkflow(request_id);
      setEnhancementResults(response.data);
      
      startStatusPolling(request_id);
      
    } catch (err) {
      setError(err.response?.data?.message || 'Enhancement failed. Please try again.');
      setIsProcessing(false);
    }
  };

  const startStatusPolling = (requestId) => {
    statusIntervalRef.current = setInterval(async () => {
      try {
        const response = await axios.get(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.WORKFLOW_STATUS}/${requestId}`);
        const status = response.data;
        setWorkflowStatus(status);
        
        if (status.status === 'completed' || status.status === 'failed') {
          clearInterval(statusIntervalRef.current);
          setIsProcessing(false);
        }
      } catch (err) {
        console.error('Status check failed:', err);
      }
    }, API_CONFIG.STATUS_POLLING_INTERVAL);
  };

  const downloadFile = async (filename, fileType) => {
    try {
      const response = await axios.get(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.DOWNLOAD_FILE}/${filename}`, {
        responseType: 'blob',
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError('Download failed. Please try again.');
    }
  };

  const getWorkflowProgress = () => {
    if (!workflowStatus) return 0;
    
    const progressMap = {
      'parsing_jd': 25,
      'parsing_resume': 50,
      'analyzing_gaps': 75,
      'enhancing_document': 90,
      'completed': 100
    };
    
    return progressMap[workflowStatus.status] || 0;
  };

  const getStatusColor = () => {
    if (!workflowStatus) return '#3B82F6';
    if (workflowStatus.status === 'completed') return '#10B981';
    if (workflowStatus.status === 'failed') return '#EF4444';
    return '#3B82F6';
  };

  const resetForm = () => {
    setResumeFile(null);
    setJobDescription('');
    setEnhancementResults(null);
    setWorkflowStatus(null);
    setError(null);
  };

  return (
    <Box sx={{
      minHeight: '100vh',
      background: theme.palette.mode === 'dark'
        ? 'linear-gradient(135deg, #1E293B 0%, #334155 50%, #475569 100%)'
        : 'linear-gradient(135deg, #FFFFFF 0%, #EBF3FF 35%, #D6E8FF 65%, #B6DCFE 100%)',
      position: 'relative',
      overflow: 'hidden'
    }}>
      {/* Refined floating elements */}
      <Box sx={{
        position: 'absolute',
        width: '100%',
        height: '100%',
        opacity: 0.6,
        zIndex: 0,
        overflow: 'hidden'
      }}>
        {[...Array(5)].map((_, i) => (
          <motion.div
            key={i}
            animate={{
              y: [0, -20, 0],
              rotate: [0, 10, 0],
              scale: [1, 1.05, 1]
            }}
            transition={{
              duration: 8,
              delay: i * 1.2,
              repeat: Infinity,
              ease: "easeInOut"
            }}
            style={{
              position: 'absolute',
              width: '300px',
              height: '300px',
              borderRadius: '50%',
              background: `radial-gradient(circle, ${
                ['#e0e7ff33', '#dbeafe33', '#e0f2fe33', '#f0f9ff33', '#f8fafc33'][i]
              } 0%, transparent 70%)`,
              left: `${[10, 60, 20, 70, 40][i]}%`,
              top: `${[20, 60, 80, 30, 50][i]}%`,
              transform: 'translate(-50%, -50%)',
              filter: 'blur(40px)',
            }}
          />
        ))}
      </Box>

      <Container maxWidth="xl" sx={{ mt: { xs: 4, md: 8 }, position: 'relative', zIndex: 1 }}>
        <Grid container spacing={6} alignItems="center">
          {/* Left side content */}
          <Grid item xs={12} md={5}>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, ease: "easeOut" }}
            >
              <Typography 
                variant="h1" 
                sx={{ 
                  fontSize: { xs: '2.5rem', md: '3.5rem' },
                  fontWeight: '700',
                  letterSpacing: '-1px',
                  lineHeight: 1.2,
                  mb: 3,
                  background: 'linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                }}>
                AI Resume Enhancer
              </Typography>
              <Typography 
                sx={{ 
                  color: '#64748B',
                  fontSize: '1.1rem',
                  lineHeight: 1.6,
                  mb: 6
                }}>
                Our AI analyzes your resume against job descriptions to provide tailored enhancements and improvements.
              </Typography>

              {/* Feature cards with glass morphism */}
              {[
                { 
                  icon: '✨', 
                  title: 'Smart Enhancement', 
                  text: 'AI-powered keyword integration to identify and add missing skills from job descriptions'
                },
                { 
                  icon: '🎯', 
                  title: 'Tailored Improvements', 
                  text: 'Get customized bullet points and phrases that align perfectly with the job requirements'
                },
                { 
                  icon: '⚡', 
                  title: 'Instant Results', 
                  text: 'Receive an enhanced resume with integrated keywords and improved content within minutes'
                }
              ].map((feature, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                >
                  <Box sx={{
                    mb: 3,
                    p: 3,
                    borderRadius: '24px',
                    background: 'rgba(255, 255, 255, 0.7)',
                    backdropFilter: 'blur(20px)',
                    border: '1px solid rgba(255, 255, 255, 0.3)',
                    transition: 'all 0.3s ease',
                    cursor: 'default',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                      background: 'rgba(255, 255, 255, 0.8)',
                      boxShadow: '0 20px 40px rgba(0, 0, 0, 0.05)'
                    }
                  }}>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <Typography sx={{ fontSize: '2rem', mr: 2 }}>{feature.icon}</Typography>
                      <Box>
                        <Typography sx={{ 
                          fontWeight: '600',
                          color: '#1E293B',
                          mb: 0.5
                        }}>
                          {feature.title}
                        </Typography>
                        <Typography sx={{ 
                          color: '#64748B',
                          fontSize: '0.9rem'
                        }}>
                          {feature.text}
                        </Typography>
                      </Box>
                    </Box>
                  </Box>
                </motion.div>
              ))}
            </motion.div>
          </Grid>

          {/* Right side content */}
          <Grid item xs={12} md={7}>
            <Box sx={{
              position: 'relative',
              zIndex: 2,
              p: { xs: 2, md: 4 },
              borderRadius: '32px',
              background: 'rgba(255, 255, 255, 0.6)',
              backdropFilter: 'blur(20px)',
              border: '1px solid rgba(255, 255, 255, 0.3)',
              boxShadow: '0 20px 40px rgba(0, 0, 0, 0.05)'
            }}>
              {!enhancementResults ? (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6 }}
                >
                  {/* File upload area */}
                  <Box
                    onClick={() => fileInputRef.current.click()}
                    sx={{
                      p: 4,
                      mb: 4,
                      borderRadius: '20px',
                      background: 'rgba(255, 255, 255, 0.8)',
                      border: '2px dashed rgba(59, 130, 246, 0.3)',
                      transition: 'all 0.3s ease',
                      cursor: 'pointer',
                      textAlign: 'center',
                      '&:hover': {
                        background: 'rgba(255, 255, 255, 0.9)',
                        borderColor: '#3B82F6',
                        transform: 'translateY(-4px)',
                        boxShadow: '0 10px 20px rgba(59, 130, 246, 0.1)'
                      }
                    }}
                  >
                    <input
                      type="file"
                      accept=".docx"
                      style={{ display: 'none' }}
                      ref={fileInputRef}
                      onChange={handleFileChange}
                    />
                    <motion.div
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                    >
                      <CloudUploadIcon sx={{ 
                        fontSize: 48,
                        color: '#3B82F6',
                        opacity: 0.8,
                        mb: 2
                      }} />
                    </motion.div>
                    <Typography variant="h6" sx={{ 
                      color: '#1E293B',
                      fontWeight: '600',
                      mb: 1
                    }}>
                      {resumeFile ? resumeFile.name : 'Drop your resume here'}
                    </Typography>
                    <Typography sx={{ color: '#64748B', fontSize: '0.9rem' }}>
                      or click to browse (DOCX only)
                    </Typography>
                  </Box>

                  {/* Job description input */}
                  <Box sx={{ mb: 4 }}>
                    <TextField
                      multiline
                      rows={4}
                      placeholder="Paste the job description here..."
                      value={jobDescription}
                      onChange={handleJobDescriptionChange}
                      fullWidth
                      sx={{
                        '& .MuiOutlinedInput-root': {
                          borderRadius: '16px',
                          background: 'rgba(255, 255, 255, 0.8)',
                          '& fieldset': {
                            borderColor: 'rgba(59, 130, 246, 0.2)'
                          },
                          '&:hover fieldset': {
                            borderColor: '#3B82F6'
                          },
                          '&.Mui-focused fieldset': {
                            borderColor: '#3B82F6'
                          }
                        }
                      }}
                    />
                  </Box>

                  {error && (
                    <Alert 
                      severity="error" 
                      sx={{ 
                        mb: 4,
                        borderRadius: '16px',
                        border: '1px solid rgba(239, 68, 68, 0.2)'
                      }}
                    >
                      {error}
                    </Alert>
                  )}

                  {/* Submit button */}
                  <motion.div
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    <Button
                      variant="contained"
                      fullWidth
                      disabled={!resumeFile || !jobDescription || isProcessing}
                      onClick={startEnhancement}
                      sx={{
                        py: 1.5,
                        background: 'linear-gradient(135deg, #3B82F6 0%, #2563EB 100%)',
                        borderRadius: '12px',
                        fontSize: '1rem',
                        fontWeight: '600',
                        textTransform: 'none',
                        boxShadow: '0 8px 16px rgba(59, 130, 246, 0.2)',
                        '&:hover': {
                          background: 'linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%)',
                        },
                        '&:disabled': {
                          background: '#94A3B8',
                          boxShadow: 'none'
                        }
                      }}
                    >
                      {isProcessing ? (
                        <CircularProgress size={24} sx={{ color: 'white' }} />
                      ) : (
                        'Enhance Resume'
                      )}
                    </Button>
                  </motion.div>
                </motion.div>
              ) : (
                <Box sx={{
                  height: '100vh',
                  overflowY: 'auto',
                  pr: 2,
                  pb: 6,
                  scrollbarWidth: 'thin',
                  '&::-webkit-scrollbar': { width: '6px' },
                  '&::-webkit-scrollbar-thumb': {
                    background: 'rgba(0, 0, 0, 0.1)',
                    borderRadius: '3px',
                  }
                }}>
                  {/* New Analysis Button */}
                  <Box sx={{ 
                    display: 'flex', 
                    justifyContent: 'flex-end',
                    mb: 3 
                  }}>
                    <motion.div
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                    >
                      <Button
                        onClick={resetForm}
                        startIcon={<RefreshIcon />}
                        sx={{
                          background: 'linear-gradient(135deg, #3B82F6 0%, #2563EB 100%)',
                          color: 'white',
                          px: 3,
                          py: 1,
                          borderRadius: '12px',
                          textTransform: 'none',
                          fontWeight: '500',
                          '&:hover': {
                            background: 'linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%)',
                          }
                        }}
                      >
                        Start New Enhancement
                      </Button>
                    </motion.div>
                  </Box>

                  {/* Results Display */}
                  <Box sx={{ mb: 4 }}>
                    <Box sx={{
                      p: 3,
                      background: 'white',
                      borderRadius: '16px',
                      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                      border: '1px solid rgba(59, 130, 246, 0.1)'
                    }}>
                      <Box sx={{ textAlign: 'center', mb: 4 }}>
                        <CheckIcon sx={{ fontSize: 60, color: '#10B981', mb: 2 }} />
                        <Typography variant="h4" sx={{ color: '#10B981', mb: 2, fontWeight: '700' }}>
                          Enhancement Complete!
                        </Typography>
                        <Typography variant="h6" sx={{ color: '#64748B', mb: 4 }}>
                          Your resume has been enhanced with AI-powered insights
                        </Typography>
                      </Box>

                      {/* Summary Stats */}
                      <Grid container spacing={3} sx={{ mb: 4 }}>
                        <Grid item xs={6}>
                          <Box sx={{ 
                            textAlign: 'center', 
                            p: 2, 
                            borderRadius: '12px',
                            background: 'rgba(59, 130, 246, 0.1)',
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center'
                          }}>
                            <Typography variant="h6" sx={{ color: '#3B82F6', fontWeight: 600 }}>
                              {enhancementResults.workflow_summary.jd_skills_analyzed}
                            </Typography>
                            <Typography variant="body2" sx={{ color: '#64748B' }}>
                              Skills Analyzed
                            </Typography>
                          </Box>
                        </Grid>
                        <Grid item xs={6}>
                          <Box sx={{ 
                            textAlign: 'center', 
                            p: 2, 
                            borderRadius: '12px',
                            background: 'rgba(16, 185, 129, 0.1)',
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center'
                          }}>
                            <Typography variant="h6" sx={{ color: '#10B981', fontWeight: 600 }}>
                              {enhancementResults.workflow_summary.improvements_generated}
                            </Typography>
                            <Typography variant="body2" sx={{ color: '#64748B' }}>
                              Improvements
                            </Typography>
                          </Box>
                        </Grid>
                      </Grid>

                      {/* Download Buttons */}
                      <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
                        {enhancementResults.files.enhanced_docx && (
                          <Button
                            variant="contained"
                            startIcon={<DownloadIcon />}
                            onClick={() => downloadFile(
                              enhancementResults.files.enhanced_docx.split('/').pop(),
                              'docx'
                            )}
                            sx={{
                              bgcolor: '#3B82F6',
                              borderRadius: '12px',
                              px: 3,
                              py: 1.5,
                              fontWeight: '600',
                              textTransform: 'none',
                              '&:hover': {
                                bgcolor: '#2563EB',
                              }
                            }}
                          >
                            Download DOCX
                          </Button>
                        )}
                        
                        {enhancementResults.files.enhanced_pdf && (
                          <Button
                            variant="outlined"
                            startIcon={<DownloadIcon />}
                            onClick={() => downloadFile(
                              enhancementResults.files.enhanced_pdf.split('/').pop(),
                              'pdf'
                            )}
                            sx={{
                              borderColor: '#3B82F6',
                              color: '#3B82F6',
                              borderRadius: '12px',
                              px: 3,
                              py: 1.5,
                              fontWeight: '600',
                              textTransform: 'none',
                              '&:hover': {
                                borderColor: '#2563EB',
                                bgcolor: 'rgba(59, 130, 246, 0.1)',
                              }
                            }}
                          >
                            Download PDF
                          </Button>
                        )}
                      </Box>
                    </Box>
                  </Box>
                </Box>
              )}

              {/* Processing Status */}
              {isProcessing && (
                <Box sx={{
                  p: 4,
                  background: 'rgba(255, 255, 255, 0.8)',
                  borderRadius: '20px',
                  textAlign: 'center',
                  mt: 4
                }}>
                  <CircularProgress
                    size={60}
                    sx={{ color: getStatusColor(), mb: 3 }}
                  />
                  <Typography variant="h5" sx={{ color: '#1E293B', mb: 2, fontWeight: '600' }}>
                    Enhancing Your Resume...
                  </Typography>
                  <Typography variant="body1" sx={{ color: '#64748B', mb: 3 }}>
                    This usually takes 1-2 minutes
                  </Typography>
                  
                  {/* Progress Bar */}
                  <Box sx={{ width: '100%', mb: 3 }}>
                    <Box
                      sx={{
                        width: '100%',
                        height: 8,
                        background: 'rgba(0, 0, 0, 0.1)',
                        borderRadius: 4,
                        overflow: 'hidden',
                      }}
                    >
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${getWorkflowProgress()}%` }}
                        transition={{ duration: 0.5, ease: "easeOut" }}
                        style={{
                          height: '100%',
                          background: getStatusColor(),
                          borderRadius: 4,
                        }}
                      />
                    </Box>
                  </Box>
                  
                  <Typography variant="body2" sx={{ color: getStatusColor(), fontWeight: '600' }}>
                    {workflowStatus?.status?.replace('_', ' ').toUpperCase() || 'Starting...'}
                  </Typography>
                </Box>
              )}
            </Box>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

export default ResumeEnhancer;
