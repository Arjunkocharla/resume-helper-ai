import React, { useState, useRef } from 'react';
import {
  Container, Typography, Button, TextField, Box, CircularProgress,
  Alert, IconButton, Tooltip, AppBar, Toolbar, Grid, useTheme
} from '@mui/material';
import {
  CloudUpload as CloudUploadIcon,
  ContentCopy,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
  ExitToApp as LogoutIcon,
  AccountCircle as ProfileIcon,
  CheckCircleOutline
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

  const handleSubmit = async () => {
    if (!file || !jobDescription.trim()) {
      setError('Please provide both a resume and job description');
      return;
    }

    setError('');
    setSuggestions(null);
    setLoading(true);

    const formData = new FormData();
    formData.append('resume', file);
    formData.append('job_description', jobDescription);

    try {
      const response = await fetch('http://127.0.0.1:5000/suggest_keywords', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Failed to analyze resume');
      const data = await response.json();
      setSuggestions(data.keyword_suggestions);
    } catch (err) {
      setError(err.message || 'An error occurred while analyzing the resume');
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

  const cubStyle = {
    position: 'absolute',
    width: '60px',
    height: '60px',
    borderRadius: '12px',
    background: 'rgba(0, 0, 0, 0.02)',
    backdropFilter: 'blur(5px)',
    border: '1px solid rgba(0, 0, 0, 0.05)',
    animation: 'float 6s ease-in-out infinite',
  };

  return (
    <Box sx={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #E0E0E0 0%, #C7D2FE 100%)',
      position: 'relative',
      overflow: 'hidden'
    }}>
      <Box sx={{ ...cubStyle, top: '10%', left: '5%', animationDelay: '0s', background: 'rgba(59, 130, 246, 0.05)' }} />
      <Box sx={{ ...cubStyle, top: '70%', left: '10%', animationDelay: '1s', background: 'rgba(16, 185, 129, 0.05)' }} />
      <Box sx={{ ...cubStyle, top: '20%', right: '5%', animationDelay: '2s', background: 'rgba(245, 158, 11, 0.05)' }} />
      <Box sx={{ ...cubStyle, bottom: '15%', right: '10%', animationDelay: '3s', background: 'rgba(59, 130, 246, 0.05)' }} />

      <AppBar position="static" elevation={0} sx={{ background: 'transparent', boxShadow: 'none' }}>
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1, color: '#1E3A8A', fontWeight: 'bold' }}>
            Resume Helper AI
          </Typography>
          <IconButton onClick={handleProfileClick} sx={{ color: '#1E3A8A' }}>
            <ProfileIcon />
          </IconButton>
          <IconButton onClick={handleLogout} sx={{ color: '#1E3A8A' }}>
            <LogoutIcon />
          </IconButton>
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl">
        <Grid container spacing={0}>
          <Grid item xs={12} md={6} sx={{ 
            p: 6,
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
          }}>
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5 }}
            >
              <Typography variant="h2" sx={{ 
                color: '#1E3A8A',
                fontWeight: 'bold',
                mb: 3,
                fontSize: { xs: '2.5rem', md: '3.5rem' }
              }}>
                Get AI-Powered Resume Insights
              </Typography>
              <Typography variant="h5" sx={{ color: '#4B5563', mb: 4, lineHeight: 1.6 }}>
                Our AI analyzes your resume against job descriptions to provide:
              </Typography>

              {[
                { icon: '🎯', text: 'Tailored keyword suggestions that match job requirements' },
                { icon: '📈', text: 'Ready-to-use bullet points to highlight your experience' },
                { icon: '⚡', text: 'Strategic placement recommendations for maximum impact' }
              ].map((item, index) => (
                <Box key={index} sx={{ 
                  display: 'flex', 
                  alignItems: 'center',
                  mb: 2,
                  p: 2,
                  borderRadius: '12px',
                  background: 'rgba(255, 255, 255, 0.5)',
                  backdropFilter: 'blur(10px)',
                }}>
                  <Typography variant="h5" sx={{ mr: 2 }}>{item.icon}</Typography>
                  <Typography variant="body1" sx={{ color: '#1E293B' }}>{item.text}</Typography>
                </Box>
              ))}
            </motion.div>
          </Grid>

          <Grid item xs={12} md={6} sx={{ position: 'relative' }}>
            <Box sx={{
              height: '100%',
              display: 'flex',
              flexDirection: 'column',
              p: 6,
            }}>
              {!suggestions ? (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5 }}
                >
                  <Box sx={{
                    p: 4,
                    borderRadius: '24px',
                    background: 'rgba(255, 255, 255, 0.9)',
                    backdropFilter: 'blur(10px)',
                    border: '2px dashed rgba(59, 130, 246, 0.3)',
                    textAlign: 'center',
                    mb: 4,
                    cursor: 'pointer',
                    minHeight: '200px', // Matching height with description box
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'center',
                    alignItems: 'center',
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      borderColor: '#3B82F6',
                      background: 'rgba(255, 255, 255, 0.95)',
                    }
                  }}
                  onClick={() => fileInputRef.current.click()}
                  >
                    <input
                      type="file"
                      accept=".pdf,.docx"
                      style={{ display: 'none' }}
                      ref={fileInputRef}
                      onChange={handleFileChange}
                    />
                    <CloudUploadIcon sx={{ fontSize: 56, color: '#3B82F6', mb: 2 }} />
                    <Typography variant="h6" sx={{ color: '#1E293B', mb: 1, fontWeight: '500' }}>
                      {file ? file.name : 'Drop your resume here'}
                    </Typography>
                    <Typography variant="body1" sx={{ color: '#64748B' }}>
                      or click to browse (PDF, DOCX)
                    </Typography>
                  </Box>

                  <TextField
                    multiline
                    rows={8}
                    placeholder="Paste the job description here..."
                    value={jobDescription}
                    onChange={handleJobDescriptionChange}
                    sx={{
                      mb: 4,
                      '& .MuiOutlinedInput-root': {
                        backgroundColor: 'rgba(255, 255, 255, 0.9)',
                        borderRadius: '24px', // Matching border radius
                        minHeight: '200px', // Matching height
                        '& textarea': {
                          p: 3,
                        }
                      }
                    }}
                  />

                  {error && (
                    <Alert severity="error" sx={{ mb: 4, borderRadius: '16px' }}>
                      {error}
                    </Alert>
                  )}

                  <Button
                    variant="contained"
                    fullWidth
                    disabled={!file || !jobDescription || loading}
                    onClick={handleSubmit}
                    sx={{
                      py: 2.5,
                      background: 'linear-gradient(135deg, #3B82F6 0%, #2563EB 100%)',
                      borderRadius: '24px', // Matching border radius
                      fontSize: '1.1rem',
                      fontWeight: '500',
                      textTransform: 'none',
                      height: '60px', // Fixed height
                      '&:hover': {
                        background: 'linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%)',
                      }
                    }}
                  >
                    {loading ? <CircularProgress size={24} sx={{ color: 'white' }} /> : 'Get Personalized Suggestions'}
                  </Button>
                </motion.div>
              ) : (
                <Box sx={{
                  height: '100vh',
                  overflowY: 'auto',
                  pr: 2,
                  pb: 6,
                  scrollbarWidth: 'thin',
                  '&::-webkit-scrollbar': {
                    width: '6px',
                  },
                  '&::-webkit-scrollbar-thumb': {
                    background: 'rgba(0, 0, 0, 0.1)',
                    borderRadius: '3px',
                  }
                }}>
                  <AnimatePresence>
                    {suggestions.keywords.map((suggestion, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.3, delay: index * 0.1 }}
                      >
                        <Box sx={{
                          mb: 3,
                          borderRadius: '16px',
                          background: 'rgba(255, 255, 255, 0.9)',
                          backdropFilter: 'blur(10px)',
                          overflow: 'hidden',
                        }}>
                          <Box
                            onClick={() => setExpandedKeyword(expandedKeyword === index ? null : index)}
                            sx={{
                              p: 3,
                              display: 'flex',
                              justifyContent: 'space-between',
                              alignItems: 'center',
                              cursor: 'pointer',
                              '&:hover': { background: 'rgba(59, 130, 246, 0.05)' },
                            }}
                          >
                            <Typography variant="h6" sx={{ color: '#1E293B', fontWeight: 500 }}>
                              {suggestion.keyword}
                            </Typography>
                            <IconButton>
                              {expandedKeyword === index ? <ExpandLessIcon /> : <ExpandMoreIcon />}
                            </IconButton>
                          </Box>

                          <AnimatePresence>
                            {expandedKeyword === index && (
                              <motion.div
                                initial={{ height: 0, opacity: 0 }}
                                animate={{ height: 'auto', opacity: 1 }}
                                exit={{ height: 0, opacity: 0 }}
                                transition={{ duration: 0.3 }}
                              >
                                <Box sx={{ p: 3, pt: 0 }}>
                                  {suggestion.bullet_points.map((bullet, bulletIndex) => (
                                    <Box
                                      key={bulletIndex}
                                      sx={{
                                        mb: 2,
                                        p: 3,
                                        borderRadius: '12px',
                                        background: 'rgba(59, 130, 246, 0.05)',
                                        display: 'flex',
                                        justifyContent: 'space-between',
                                        alignItems: 'flex-start',
                                      }}
                                    >
                                      <Box sx={{ flex: 1, mr: 2 }}>
                                        <Typography sx={{ color: '#1E293B' }}>
                                          {bullet.point}
                                        </Typography>
                                        <Typography variant="body2" sx={{ mt: 1, color: '#64748B' }}>
                                          {bullet.explanation}
                                        </Typography>
                                      </Box>
                                      <Tooltip title={copySuccess === bulletIndex ? 'Copied!' : 'Copy to clipboard'}>
                                        <IconButton 
                                          onClick={() => copyToClipboard(bullet.point, bulletIndex)}
                                          sx={{ color: copySuccess === bulletIndex ? '#10B981' : '#3B82F6' }}
                                        >
                                          {copySuccess === bulletIndex ? <CheckCircleOutline /> : <ContentCopy />}
                                        </IconButton>
                                      </Tooltip>
                                    </Box>
                                  ))}
                                </Box>
                              </motion.div>
                            )}
                          </AnimatePresence>
                        </Box>
                      </motion.div>
                    ))}
                  </AnimatePresence>
                </Box>
              )}
            </Box>
          </Grid>
        </Grid>
      </Container>

      <style jsx global>{`
        @keyframes float {
          0% { transform: translateY(0px) rotate(0deg); }
          50% { transform: translateY(-20px) rotate(10deg); }
          100% { transform: translateY(0px) rotate(0deg); }
        }
      `}</style>
    </Box>
  );
}

export default SuggestKeywords;
