import React, { useState, useRef } from 'react';
import {
  Container, Typography, Button, TextField, Box, CircularProgress,
  Alert, IconButton, Tooltip, AppBar, Toolbar, Grid, useTheme, Collapse
} from '@mui/material';
import {
  CloudUpload as CloudUploadIcon,
  ContentCopy,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
  ExitToApp as LogoutIcon,
  AccountCircle as ProfileIcon,
  CheckCircleOutline,
  Refresh as RefreshIcon,  // Changed this line
  Assessment as AssessmentIcon,
  Lightbulb as LightbulbIcon
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { auth } from '../firebase';
import { signOut } from 'firebase/auth';

function SuggestKeywords() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [suggestions, setSuggestions] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [expandedKeyword, setExpandedKeyword] = useState(null);
  const [copySuccess, setCopySuccess] = useState(null);
  const fileInputRef = useRef(null);
  const navigate = useNavigate();
  const theme = useTheme();
  const [showFullAnalysis, setShowFullAnalysis] = useState(false);
  const [showActionPlan, setShowActionPlan] = useState(false);

  const handleProfileClick = () => navigate('/profile');
  
  const handleLogout = async () => {
    try {
      await signOut(auth);
      navigate('/login');
    } catch (error) {
      console.error('Error signing out:', error);
    }
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && (selectedFile.type === 'application/pdf' || 
        selectedFile.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')) {
      setFile(selectedFile);
      setError('');
    } else {
      setError('Please upload a PDF or DOCX file');
      setFile(null);
    }
  };

  const handleJobDescriptionChange = (e) => {
    setJobDescription(e.target.value);
    setError('');
  };

  const callSuggestKeywordsAPI = async (retry = false) => {
    const formData = new FormData();
    formData.append('resume', file);
    formData.append('job_description', jobDescription);
    formData.append('retry', retry.toString());

    const response = await fetch('http://127.0.0.1:5000/suggest_keywords', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) throw new Error('Failed to analyze resume');
    return await response.json();
  };

  const handleSubmit = async () => {
    if (!file || !jobDescription.trim()) {
      setError('Please provide both a resume and job description');
      return;
    }

    setError('');
    setSuggestions(null);
    setLoading(true);

    try {
      // First attempt
      const data = await callSuggestKeywordsAPI(false);
      setSuggestions(data.keyword_suggestions);
    } catch (err) {
      console.error('First attempt failed:', err);
      try {
        // Retry with retry=true if first attempt fails
        const retryData = await callSuggestKeywordsAPI(true);
        setSuggestions(retryData.keyword_suggestions);
      } catch (retryErr) {
        console.error('Retry attempt failed:', retryErr);
        setError('Failed to analyze resume after multiple attempts. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = async (text, index) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopySuccess(index);
      setTimeout(() => setCopySuccess(null), 2000);
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  };

  // Add this function with your other handlers
  const handleStartNewAnalysis = () => {
    setSuggestions(null);
    setFile(null);
    setJobDescription('');
    setError('');
    setExpandedKeyword(null);
  };

  // Add this handler with your other handlers
  const handleHomeClick = () => navigate('/');

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

      {/* Refined AppBar */}
      <AppBar position="static" elevation={0} 
        sx={{ 
          background: 'transparent', 
          backdropFilter: 'blur(10px)',
          borderBottom: '1px solid rgba(255, 255, 255, 0.1)'
        }}>
        <Container maxWidth="xl">
          <Toolbar sx={{ px: { xs: 0, sm: 2 } }}>
            <Typography variant="h6" 
              onClick={handleHomeClick}  // Add this
              sx={{ 
                flexGrow: 1, 
                background: 'linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                fontWeight: '700',
                letterSpacing: '-0.5px',
                cursor: 'pointer',  // Add this to show it's clickable
                '&:hover': {  // Add hover effect
                  opacity: 0.8
                }
              }}>
              Resume Helper AI
            </Typography>
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
              <IconButton onClick={handleProfileClick} 
                sx={{ 
                  color: '#1E3A8A',
                  background: 'rgba(255, 255, 255, 0.1)',
                  backdropFilter: 'blur(10px)',
                  mr: 1,
                  '&:hover': { background: 'rgba(255, 255, 255, 0.2)' }
                }}>
                <ProfileIcon />
              </IconButton>
            </motion.div>
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
              <IconButton onClick={handleLogout}
                sx={{ 
                  color: '#1E3A8A',
                  background: 'rgba(255, 255, 255, 0.1)',
                  backdropFilter: 'blur(10px)',
                  '&:hover': { background: 'rgba(255, 255, 255, 0.2)' }
                }}>
                <LogoutIcon />
              </IconButton>
            </motion.div>
          </Toolbar>
        </Container>
      </AppBar>

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
                Elevate Your Resume
              </Typography>
              <Typography 
                sx={{ 
                  color: '#64748B',
                  fontSize: '1.1rem',
                  lineHeight: 1.6,
                  mb: 6
                }}>
                Our AI analyzes your resume against job descriptions to provide tailored insights and suggestions.
              </Typography>

              {/* Feature cards with glass morphism */}
              {[
                { 
                  icon: '✨', 
                  title: 'Smart Analysis', 
                  text: 'AI-powered keyword matching to identify the most relevant skills and experiences from your resume'
                },
                { 
                  icon: '🎯', 
                  title: 'Tailored Suggestions', 
                  text: 'Get customized bullet points and phrases that align perfectly with the job requirements'
                },
                { 
                  icon: '⚡', 
                  title: 'Instant Results', 
                  text: 'Receive quick, actionable feedback to improve your resume\'s impact within minutes'
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
              {!suggestions ? (
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
                      accept=".pdf,.docx"
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
                      {file ? file.name : 'Drop your resume here'}
                    </Typography>
                    <Typography sx={{ color: '#64748B', fontSize: '0.9rem' }}>
                      or click to browse (PDF, DOCX)
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
                      disabled={!file || !jobDescription || loading}
                      onClick={handleSubmit}
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
                      {loading ? (
                        <CircularProgress size={24} sx={{ color: 'white' }} />
                      ) : (
                        'Analyze Resume'
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
                        onClick={handleStartNewAnalysis}
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
                        Start New Analysis
                      </Button>
                    </motion.div>
                  </Box>

                  {/* Quick Summary Strip */}
                  <Box sx={{ mb: 4 }}>
                    <Grid container spacing={3}>
                      {/* Key Findings Card */}
                      <Grid item xs={12}>
                        <Box sx={{
                          p: 3,
                          background: 'white',
                          borderRadius: '16px',
                          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                          border: '1px solid rgba(59, 130, 246, 0.1)'
                        }}>
                          <Grid container spacing={2}>
                            {/* Summary Stats */}
                            <Grid item xs={12} md={8}>
                              <Box sx={{ display: 'flex', gap: 3 }}>
                                {/* Match Score */}
                                <Box sx={{ 
                                  flex: 1,
                                  p: 2, 
                                  borderRadius: '12px',
                                  background: 'rgba(59, 130, 246, 0.1)',
                                  display: 'flex',
                                  flexDirection: 'column',
                                  alignItems: 'center'
                                }}>
                                  <Typography variant="h6" sx={{ color: '#3B82F6', fontWeight: 600 }}>
                                    {suggestions.keywords.length}
                                  </Typography>
                                  <Typography variant="body2" sx={{ color: '#64748B' }}>
                                    Keywords Found
                                  </Typography>
                                </Box>
                                
                                {/* Quick Actions */}
                                <Box sx={{ 
                                  flex: 2,
                                  p: 2, 
                                  borderRadius: '12px',
                                  background: 'rgba(16, 185, 129, 0.1)',
                                  display: 'flex',
                                  alignItems: 'center',
                                  gap: 2
                                }}>
                                  <Box sx={{ flex: 1 }}>
                                    <Typography variant="body2" sx={{ color: '#064E3B', fontWeight: 600, mb: 0.5 }}>
                                      Quick Action
                                    </Typography>
                                    <Typography variant="body2" sx={{ color: '#047857' }}>
                                      Start with high-priority keywords in your summary section
                                    </Typography>
                                  </Box>
                                  <Button
                                    variant="contained"
                                    size="small"
                                    onClick={() => setExpandedKeyword(0)} // Opens first keyword
                                    sx={{
                                      bgcolor: '#10B981',
                                      '&:hover': { bgcolor: '#059669' }
                                    }}
                                  >
                                    Start
                                  </Button>
                                </Box>
                              </Box>
                            </Grid>

                            {/* Action Menu */}
                            <Grid item xs={12} md={4}>
                              <Box sx={{ 
                                height: '100%',
                                display: 'flex',
                                alignItems: 'center',
                                gap: 2,
                                justifyContent: 'flex-end'
                              }}>
                                <Tooltip title="View Full Analysis">
                                  <IconButton
                                    onClick={() => setShowFullAnalysis(prev => !prev)}
                                    sx={{ 
                                      color: '#3B82F6',
                                      bgcolor: 'rgba(59, 130, 246, 0.1)',
                                      '&:hover': { bgcolor: 'rgba(59, 130, 246, 0.2)' }
                                    }}
                                  >
                                    <AssessmentIcon />
                                  </IconButton>
                                </Tooltip>
                                <Tooltip title="View Action Plan">
                                  <IconButton
                                    onClick={() => setShowActionPlan(prev => !prev)}
                                    sx={{ 
                                      color: '#10B981',
                                      bgcolor: 'rgba(16, 185, 129, 0.1)',
                                      '&:hover': { bgcolor: 'rgba(16, 185, 129, 0.2)' }
                                    }}
                                  >
                                    <LightbulbIcon />
                                  </IconButton>
                                </Tooltip>
                              </Box>
                            </Grid>
                          </Grid>

                          {/* Expandable Analysis */}
                          <Collapse in={showFullAnalysis}>
                            <Box sx={{ mt: 2, p: 2, bgcolor: 'rgba(59, 130, 246, 0.05)', borderRadius: '12px' }}>
                              <Typography variant="subtitle1" sx={{ mb: 2, fontWeight: 600 }}>
                                Analysis Points:
                              </Typography>
                              {/* Split the text into points by splitting on periods */}
                              {suggestions.experience_gap_analysis.split('. ')
                                .filter(point => point.trim())  // Remove empty points
                                .map((point, index) => (
                                  <Box key={index} sx={{ 
                                    display: 'flex', 
                                    gap: 2, 
                                    mb: 2,
                                    p: 2,
                                    borderRadius: '8px',
                                    bgcolor: 'white',
                                    border: '1px solid rgba(59, 130, 246, 0.1)'
                                  }}>
                                    <Box sx={{
                                      minWidth: 24,
                                      height: 24,
                                      borderRadius: '50%',
                                      bgcolor: 'primary.main',
                                      color: 'white',
                                      display: 'flex',
                                      alignItems: 'center',
                                      justifyContent: 'center',
                                      fontSize: '0.8rem'
                                    }}>
                                      {index + 1}
                                    </Box>
                                    <Typography sx={{ fontSize: '0.9rem', color: '#334155' }}>
                                      {point.trim()}.
                                    </Typography>
                                  </Box>
                                ))}
                            </Box>
                          </Collapse>

                          {/* Expandable Action Plan */}
                          <Collapse in={showActionPlan}>
                            <Box sx={{ mt: 2, p: 2, bgcolor: 'rgba(16, 185, 129, 0.05)', borderRadius: '12px' }}>
                              <Typography variant="subtitle1" sx={{ mb: 2, fontWeight: 600 }}>
                                Action Steps:
                              </Typography>
                              {/* Split the text into steps by splitting on periods */}
                              {suggestions.overall_strategy.split('. ')
                                .filter(step => step.trim())  // Remove empty steps
                                .map((step, index) => (
                                  <Box key={index} sx={{ 
                                    display: 'flex', 
                                    gap: 2, 
                                    mb: 2,
                                    p: 2,
                                    borderRadius: '8px',
                                    bgcolor: 'white',
                                    border: '1px solid rgba(16, 185, 129, 0.1)'
                                  }}>
                                    <Box sx={{
                                      minWidth: 24,
                                      height: 24,
                                      borderRadius: '50%',
                                      bgcolor: 'success.main',
                                      color: 'white',
                                      display: 'flex',
                                      alignItems: 'center',
                                      justifyContent: 'center',
                                      fontSize: '0.8rem'
                                    }}>
                                      {index + 1}
                                    </Box>
                                    <Typography sx={{ fontSize: '0.9rem', color: '#334155' }}>
                                      {step.trim()}.
                                    </Typography>
                                  </Box>
                                ))}
                            </Box>
                          </Collapse>
                        </Box>
                      </Grid>
                    </Grid>
                  </Box>

                  {/* Keywords Section */}
                  <Box sx={{ mb: 4 }}>
                    <Typography variant="h5" sx={{ color: '#1E293B', mb: 3, fontWeight: 600 }}>
                      Recommended Keywords & Improvements
                    </Typography>
                    
                    <Grid container spacing={3}>
                      {suggestions.keywords.map((suggestion, index) => (
                        <Grid item xs={12} key={index}>
                          <Box
                            sx={{
                              background: 'white',
                              borderRadius: '16px',
                              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                              overflow: 'hidden',
                              border: '1px solid rgba(59, 130, 246, 0.1)'
                            }}
                          >
                            {/* Keyword Header */}
                            <Box
                              onClick={() => setExpandedKeyword(expandedKeyword === index ? null : index)}
                              sx={{
                                p: 3,
                                display: 'flex',
                                alignItems: 'flex-start',
                                cursor: 'pointer',
                                background: expandedKeyword === index ? 'rgba(59, 130, 246, 0.05)' : 'transparent',
                                transition: 'background 0.2s ease',
                                '&:hover': { background: 'rgba(59, 130, 246, 0.05)' },
                              }}
                            >
                              <Box sx={{ flex: 1 }}>
                                <Typography variant="h6" sx={{ color: '#1E293B', fontWeight: 600, mb: 1 }}>
                                  {suggestion.keyword}
                                </Typography>
                                <Typography variant="body2" sx={{ color: '#64748B' }}>
                                  {suggestion.importance}
                                </Typography>
                                <Typography 
                                  variant="caption" 
                                  sx={{ 
                                    display: 'inline-block',
                                    mt: 2,
                                    px: 2,
                                    py: 0.5,
                                    borderRadius: '12px',
                                    background: 'rgba(59, 130, 246, 0.1)',
                                    color: '#3B82F6'
                                  }}
                                >
                                  Suggested Section: {suggestion.placement}
                                </Typography>
                              </Box>
                              <IconButton>
                                {expandedKeyword === index ? <ExpandLessIcon /> : <ExpandMoreIcon />}
                              </IconButton>
                            </Box>

                            {/* Expanded Content */}
                            <AnimatePresence>
                              {expandedKeyword === index && (
                                <motion.div
                                  initial={{ height: 0, opacity: 0 }}
                                  animate={{ height: 'auto', opacity: 1 }}
                                  exit={{ height: 0, opacity: 0 }}
                                  transition={{ duration: 0.3 }}
                                >
                                  <Box sx={{ p: 3, pt: 0, borderTop: '1px solid rgba(59, 130, 246, 0.1)' }}>
                                    <Typography variant="subtitle2" sx={{ color: '#1E293B', mb: 2, fontWeight: 600 }}>
                                      Suggested Implementations:
                                    </Typography>
                                    {suggestion.bullet_points.map((bullet, bulletIndex) => (
                                      <Box
                                        key={bulletIndex}
                                        sx={{
                                          mb: 2,
                                          p: 3,
                                          borderRadius: '12px',
                                          background: 'rgba(59, 130, 246, 0.05)',
                                          border: '1px solid rgba(59, 130, 246, 0.1)',
                                        }}
                                      >
                                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                                          <Typography sx={{ color: '#1E293B', flex: 1, pr: 2 }}>
                                            {bullet.point}
                                          </Typography>
                                          <Tooltip title={copySuccess === bulletIndex ? 'Copied!' : 'Copy to clipboard'}>
                                            <IconButton 
                                              onClick={() => copyToClipboard(bullet.point, bulletIndex)}
                                              sx={{ 
                                                color: copySuccess === bulletIndex ? '#10B981' : '#3B82F6',
                                                '&:hover': { background: 'rgba(59, 130, 246, 0.1)' }
                                              }}
                                            >
                                              {copySuccess === bulletIndex ? <CheckCircleOutline /> : <ContentCopy />}
                                            </IconButton>
                                          </Tooltip>
                                        </Box>
                                        <Typography variant="body2" sx={{ color: '#64748B' }}>
                                          {bullet.explanation}
                                        </Typography>
                                      </Box>
                                    ))}
                                  </Box>
                                </motion.div>
                              )}
                            </AnimatePresence>
                          </Box>
                        </Grid>
                      ))}
                    </Grid>
                  </Box>
                </Box>
              )}
            </Box>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}

export default SuggestKeywords;
