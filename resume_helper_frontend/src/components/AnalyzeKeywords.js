import React, { useState, useRef } from 'react';
import {
  Container, Typography, Button, TextField, Paper, Box, CircularProgress,
  Alert, Fade, Card, CardContent, Chip, Tooltip, IconButton, useTheme,
  Stepper, Step, StepLabel, StepContent, List, ListItem, ListItemIcon, ListItemText,
  AppBar, Toolbar, Grid, Collapse, MenuItem
} from '@mui/material';
import {
  CloudUpload as CloudUploadIcon,
  ContentCopy,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
  Logout as LogoutIcon,
  CheckCircleOutline,
  Lightbulb as LightbulbIcon
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { auth } from '../firebase';
import { signOut } from 'firebase/auth';

function AnalyzeKeywords() {
  const [activeStep, setActiveStep] = useState(0);
  const [file, setFile] = useState(null);
  const [jobCategory, setJobCategory] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [expandedKeyword, setExpandedKeyword] = useState(null);
  const fileInputRef = useRef(null);
  const theme = useTheme();
  const navigate = useNavigate();
  const [keywords, setKeywords] = useState([]);
  const [stats, setStats] = useState({
    keywordMatch: '0%',
    uniqueTerms: '0'
  });

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setActiveStep(1);
  };

  const handleJobCategoryChange = (e) => {
    setJobCategory(e.target.value);
  };

  const handleNextStep = () => {
    setActiveStep((prevStep) => prevStep + 1);
  };

  const handleHomeClick = () => navigate('/');
  
  const handleLogout = async () => {
    try {
      await signOut(auth);
      navigate('/login');
    } catch (error) {
      console.error('Error signing out:', error);
    }
  };

  const handleSubmit = async () => {
    if (!file || !jobCategory) {
      setError('Please provide both a resume and job category');
      return;
    }

    setLoading(true);
    setError('');
    const formData = new FormData();
    formData.append('resume', file);
    formData.append('job_category', jobCategory);

    try {
      const response = await fetch('http://127.0.0.1:5000/analyze_keywords', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      console.log('API Response:', data);
      
      const keywordCount = data.analysis.keywords?.length || 0;
      const matchScore = Math.round((keywordCount / 10) * 100);

      setKeywords(data.analysis.keywords || []);
      setStats({
        keywordMatch: `${matchScore}%`,
        uniqueTerms: keywordCount.toString()
      });
      
    } catch (err) {
      console.error('API Error:', err);
      setError(err.message || 'An error occurred.');
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  const steps = [
    {
      label: 'Upload Resume',
      content: (
        <Box sx={{ mt: 2 }}>
          <input
            ref={fileInputRef}
            accept=".pdf,.docx"
            style={{ display: 'none' }}
            id="raised-button-file"
            type="file"
            onChange={handleFileChange}
          />
          <Button
            variant="outlined"
            component="span"
            startIcon={<CloudUploadIcon sx={{ color: '#1E293B' }} />}
            onClick={() => fileInputRef.current.click()}
            fullWidth
            sx={{ 
              color: '#1E293B',
              borderColor: '#1E293B',
              '&:hover': {
                borderColor: '#334155',
                backgroundColor: 'rgba(30, 41, 59, 0.04)'
              }
            }}
          >
            {file ? 'Change Resume' : 'Upload Resume'}
          </Button>
          {file && (
            <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
              <CheckCircleOutline sx={{ color: 'green', mr: 1 }} />
              <Typography variant="body2" sx={{ color: 'white' }}>{file.name}</Typography>
            </Box>
          )}
        </Box>
      ),
    },
    {
      label: 'Enter Job Category',
      content: (
        <Box>
          <TextField
            select
            fullWidth
            label="Job Category"
            value={jobCategory}
            onChange={handleJobCategoryChange}
            sx={{ 
              mb: 3,
              '& .MuiSelect-select': {
                color: '#1E293B',
              },
              '& .MuiInputLabel-root': {
                color: '#64748B',
                '&.Mui-focused': {
                  color: '#3B82F6'
                }
              },
              '& .MuiOutlinedInput-root': {
                backgroundColor: 'white',
                '& fieldset': {
                  borderColor: 'rgba(59, 130, 246, 0.2)',
                },
                '&:hover fieldset': {
                  borderColor: 'rgba(59, 130, 246, 0.3)',
                },
                '&.Mui-focused fieldset': {
                  borderColor: '#3B82F6',
                }
              }
            }}
            SelectProps={{
              native: false,
              MenuProps: {
                PaperProps: {
                  sx: {
                    backgroundColor: 'white',
                    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                    borderRadius: '8px',
                    mt: 1
                  }
                }
              }
            }}
          >
            <MenuItem value="">Select a job category</MenuItem>
            <MenuItem value="software_engineering">Software Engineering</MenuItem>
            <MenuItem value="data_science">Data Science</MenuItem>
            <MenuItem value="product_management">Product Management</MenuItem>
            <MenuItem value="marketing">Marketing</MenuItem>
            <MenuItem value="sales">Sales</MenuItem>
          </TextField>
          <Button
            onClick={handleNextStep}
            variant="contained"
            disabled={!jobCategory.trim()}
            sx={{
              mt: 2,
              bgcolor: theme.palette.primary.main,
              color: 'white',
              '&:hover': {
                bgcolor: theme.palette.primary.dark,
              },
            }}
          >
            Next
          </Button>
        </Box>
      ),
    },
    {
      label: 'Analyze Keywords',
      content: (
        <Button
          onClick={handleSubmit}
          variant="contained"
          disabled={loading || !file || !jobCategory}
          fullWidth
          sx={{
            mt: 2,
            bgcolor: theme.palette.primary.main,
            color: 'white',
            '&:hover': {
              bgcolor: theme.palette.primary.dark,
            },
          }}
        >
          {loading ? <CircularProgress size={24} /> : 'Analyze Keywords'}
        </Button>
      ),
    },
  ];

  const renderStats = () => (
    <Grid container spacing={2}>
      {[
        { 
          title: 'Keyword Match',
          value: stats.keywordMatch || '0%',
          icon: <CheckCircleOutline sx={{ color: '#10B981' }} />,
          description: 'Industry alignment'
        },
        { 
          title: 'Unique Terms',
          value: stats.uniqueTerms || '0',
          icon: <LightbulbIcon sx={{ color: '#3B82F6' }} />,
          description: 'Specialized keywords'
        }
      ].map((stat, index) => (
        <Grid item xs={12} key={index}>
          <Box sx={{
            p: 3,
            background: 'white',
            borderRadius: '16px',
            boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
            border: '1px solid rgba(59, 130, 246, 0.1)'
          }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              {stat.icon}
              <Typography variant="h6" sx={{ ml: 1, color: '#1E293B' }}>
                {stat.title}
              </Typography>
            </Box>
            <Typography variant="h4" sx={{ color: '#3B82F6', mb: 1 }}>
              {stat.value}
            </Typography>
            <Typography variant="body2" sx={{ color: '#64748B' }}>
              {stat.description}
            </Typography>
          </Box>
        </Grid>
      ))}
    </Grid>
  );

  const renderKeywords = () => (
    <Box sx={{
      background: 'white',
      borderRadius: '24px',
      border: '1px solid rgba(59, 130, 246, 0.1)',
      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
      p: 4,
    }}>
      {keywords.map((keyword, index) => (
        <Box key={index} sx={{
          mb: 3,
          background: 'rgba(59, 130, 246, 0.05)',
          borderRadius: '16px',
          overflow: 'hidden'
        }}>
          <Box sx={{
            p: 3,
            cursor: 'pointer',
            '&:hover': { background: 'rgba(59, 130, 246, 0.1)' }
          }}
          onClick={() => setExpandedKeyword(expandedKeyword === index ? null : index)}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Typography variant="h6" sx={{ color: '#1E293B', fontWeight: 600 }}>
                {keyword.keyword}
              </Typography>
              {expandedKeyword === index ? 
                <ExpandLessIcon sx={{ color: '#3B82F6' }} /> : 
                <ExpandMoreIcon sx={{ color: '#3B82F6' }} />
              }
            </Box>
          </Box>

          <Collapse in={expandedKeyword === index}>
            <Box sx={{ p: 3, pt: 0 }}>
              <Typography sx={{ color: '#64748B', mb: 2 }}>
                {keyword.importance}
              </Typography>
              <Typography variant="subtitle1" sx={{ color: '#1E293B', fontWeight: 600, mb: 2 }}>
                Suggested Implementations:
              </Typography>
              <List>
                {keyword.bullet_points.map((bulletPoint, bulletIndex) => (
                  <ListItem key={bulletIndex}
                    sx={{
                      background: 'rgba(59, 130, 246, 0.05)',
                      borderRadius: '12px',
                      mb: 2
                    }}
                    secondaryAction={
                      <Tooltip title="Copy to clipboard">
                        <IconButton onClick={() => copyToClipboard(
                          typeof bulletPoint === 'object' ? bulletPoint.point : bulletPoint
                        )}>
                          <ContentCopy sx={{ color: '#3B82F6' }} />
                        </IconButton>
                      </Tooltip>
                    }>
                    <ListItemText
                      primary={typeof bulletPoint === 'object' ? bulletPoint.point : bulletPoint}
                      primaryTypographyProps={{ color: '#1E293B' }}
                    />
                  </ListItem>
                ))}
              </List>
            </Box>
          </Collapse>
        </Box>
      ))}
    </Box>
  );

  const renderUploadSection = () => (
    <Box sx={{
      background: 'white',
      borderRadius: '24px',
      border: '1px solid rgba(59, 130, 246, 0.1)',
      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
      p: 4,
    }}>
      <Typography 
        variant="h3" 
        sx={{ 
          fontWeight: 700,
          mb: 3,
          background: 'linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
        }}>
        Keyword Analysis
      </Typography>
      <Typography 
        sx={{ 
          color: '#64748B',
          mb: 4,
          fontSize: '1.1rem',
          lineHeight: 1.5
        }}>
        Understand how your resume's keywords align with industry standards and job requirements.
      </Typography>

      <Box sx={{ mt: 4 }}>
        <input
          accept=".pdf,.docx"
          style={{ display: 'none' }}
          id="resume-upload"
          type="file"
          onChange={handleFileChange}
        />
        <label htmlFor="resume-upload">
          <Button
            component="span"
            variant="outlined"
            fullWidth
            startIcon={<CloudUploadIcon />}
            sx={{
              mb: 2,
              py: 2,
              borderColor: '#3B82F6',
              color: '#3B82F6',
              '&:hover': {
                borderColor: '#2563EB',
                background: 'rgba(59, 130, 246, 0.05)'
              }
            }}
          >
            {file ? file.name : 'Upload Resume (PDF or DOCX)'}
          </Button>
        </label>

        <TextField
          select
          fullWidth
          label="Job Category"
          value={jobCategory}
          onChange={handleJobCategoryChange}
          sx={{ 
            mb: 3,
            '& .MuiSelect-select': {
              color: '#1E293B',
            },
            '& .MuiInputLabel-root': {
              color: '#64748B',
              '&.Mui-focused': {
                color: '#3B82F6'
              }
            },
            '& .MuiOutlinedInput-root': {
              backgroundColor: 'white',
              '& fieldset': {
                borderColor: 'rgba(59, 130, 246, 0.2)',
              },
              '&:hover fieldset': {
                borderColor: 'rgba(59, 130, 246, 0.3)',
              },
              '&.Mui-focused fieldset': {
                borderColor: '#3B82F6',
              }
            }
          }}
          SelectProps={{
            native: false,
            MenuProps: {
              PaperProps: {
                sx: {
                  backgroundColor: 'white',
                  boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                  borderRadius: '8px',
                  mt: 1
                }
              }
            }
          }}
        >
          <MenuItem value="">Select a job category</MenuItem>
          <MenuItem value="software_engineering">Software Engineering</MenuItem>
          <MenuItem value="data_science">Data Science</MenuItem>
          <MenuItem value="product_management">Product Management</MenuItem>
          <MenuItem value="marketing">Marketing</MenuItem>
          <MenuItem value="sales">Sales</MenuItem>
        </TextField>

        <Button
          onClick={handleSubmit}
          variant="contained"
          fullWidth
          disabled={loading || !file || !jobCategory}
          sx={{
            py: 2,
            bgcolor: '#3B82F6',
            '&:hover': {
              bgcolor: '#2563EB'
            },
            '&.Mui-disabled': {
              bgcolor: '#94A3B8',
              color: 'white'
            }
          }}
        >
          {loading ? (
            <CircularProgress size={24} sx={{ color: 'white' }} />
          ) : (
            'Analyze Keywords'
          )}
        </Button>

        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}
      </Box>
    </Box>
  );

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
      style={{ width: '100%', height: '100%', willChange: 'transform' }}
    >
      <Box sx={{
        minHeight: '100vh',
        background: theme.palette.mode === 'dark'
          ? 'linear-gradient(135deg, #1E293B 0%, #334155 50%, #475569 100%)'
          : 'linear-gradient(135deg, #FFFFFF 0%, #EBF3FF 35%, #D6E8FF 65%, #B6DCFE 100%)',
        position: 'relative',
        overflow: 'hidden'
      }}>
        {/* Floating background elements */}
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

        {/* AppBar */}
        <AppBar position="static" elevation={0} 
          sx={{ 
            background: 'transparent', 
            backdropFilter: 'blur(10px)',
            borderBottom: '1px solid rgba(255, 255, 255, 0.1)'
          }}>
          <Toolbar>
            <Typography 
              variant="h6" 
              onClick={handleHomeClick}
              sx={{ 
                flexGrow: 1,
                background: 'linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                fontWeight: '700',
                letterSpacing: '-0.5px',
                cursor: 'pointer',
                '&:hover': { opacity: 0.8 }
              }}>
              Resume Helper AI
            </Typography>
            
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
        </AppBar>

        {/* Main Content */}
        <Container maxWidth="xl" sx={{ mt: { xs: 4, md: 8 }, position: 'relative', zIndex: 1 }}>
          <Grid container spacing={6} alignItems="flex-start">
            <Grid item xs={12} md={4}>
              {renderStats()}
            </Grid>
            <Grid item xs={12} md={8}>
              {keywords.length > 0 ? renderKeywords() : renderUploadSection()}
            </Grid>
          </Grid>
        </Container>
      </Box>
    </motion.div>
  );
}

export default AnalyzeKeywords;
