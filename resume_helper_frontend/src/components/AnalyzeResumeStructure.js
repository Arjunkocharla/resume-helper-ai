import React, { useState, useEffect } from 'react';
import {
  Box, Button, Typography, CircularProgress, Paper, Grid,
  List, ListItem, ListItemIcon, ListItemText, Divider,
  Container, Fade, Alert, LinearProgress, Tooltip,
  Accordion, AccordionSummary, AccordionDetails, Chip,
  Card, CardContent, Step, Stepper, StepLabel, StepContent, useTheme,
  AppBar, Toolbar, IconButton
} from '@mui/material';
import { 
  CloudUpload as CloudUploadIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
  CheckCircleOutline,
  ExpandMore as ExpandMoreIcon,
  ThumbUp as ThumbUpIcon,
  Build as BuildIcon,
  ArrowForward as ArrowForwardIcon,
  Description as DescriptionIcon,
  Analytics as AnalyticsIcon,
  CompareArrows as CompareArrowsIcon,
  Lightbulb as LightbulbIcon,
  Refresh as RefreshIcon,
  AccountCircle as ProfileIcon,
  ExitToApp as LogoutIcon
} from '@mui/icons-material';
import { Radar } from 'react-chartjs-2';
import { Chart as ChartJS, RadialLinearScale, PointElement, LineElement, Filler, Tooltip as ChartTooltip, Legend } from 'chart.js';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { auth } from '../firebase';
import { signOut } from 'firebase/auth';

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, ChartTooltip, Legend);

const AnalyzeResumeStructure = () => {
  const [file, setFile] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeStep, setActiveStep] = useState(0);
  const navigate = useNavigate();

  const loadingSteps = [
    { label: 'Parsing resume', description: 'Extracting text and structure...', icon: <DescriptionIcon /> },
    { label: 'Analyzing content', description: 'Evaluating resume components...', icon: <AnalyticsIcon /> },
    { label: 'Comparing to standards', description: 'Checking against industry benchmarks...', icon: <CompareArrowsIcon /> },
    { label: 'Generating insights', description: 'Crafting personalized recommendations...', icon: <LightbulbIcon /> },
  ];

  useEffect(() => {
    let interval;
    if (loading) {
      interval = setInterval(() => {
        setActiveStep((prevStep) => {
          if (prevStep < loadingSteps.length - 1) {
            return prevStep + 1;
          }
          return prevStep;
        });
      }, 3000);
    }
    return () => clearInterval(interval);
  }, [loading, loadingSteps.length]);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async () => {
    if (!file) {
      setError('Please select a resume file.');
      return;
    }

    setLoading(true);
    setError(null);
    setActiveStep(0);

    const formData = new FormData();
    formData.append('resume', file);

    try {
      const response = await fetch('http://127.0.0.1:5000/analyze_resume_structure', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to analyze resume');
      }

      const data = await response.json();
      setAnalysis(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleHomeClick = () => navigate('/');
  const handleProfileClick = () => navigate('/profile');
  const handleStartNew = () => {
    setFile(null);
    setAnalysis(null);
    setError(null);
    setActiveStep(0);
  };

  const handleLogout = async () => {
    try {
      await signOut(auth);
      navigate('/login');
    } catch (error) {
      console.error('Error signing out:', error);
    }
  };

  const renderLoadingState = () => (
    <Box sx={{ 
      maxWidth: 600, 
      margin: '0 auto', 
      mt: 4, 
      background: 'white',
      borderRadius: '24px',
      p: 4,
      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    }}>
      <Typography variant="h6" sx={{ 
        color: '#1E293B',
        textAlign: 'center',
        mb: 4 
      }}>
        Analyzing Your Resume
      </Typography>

      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 4 }}>
        {loadingSteps.map((step, index) => (
          <Box
            key={step.label}
            sx={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              position: 'relative',
              width: '120px'
            }}
          >
            {/* Connector line */}
            {index < loadingSteps.length - 1 && (
              <Box sx={{
                position: 'absolute',
                top: '20px',
                right: '-50%',
                width: '100%',
                height: '2px',
                bgcolor: index < activeStep ? '#3B82F6' : 'rgba(203, 213, 225, 0.5)',
                transition: 'background-color 0.3s ease'
              }} />
            )}

            {/* Step circle */}
            <Box sx={{
              width: 40,
              height: 40,
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              bgcolor: index <= activeStep ? 'rgba(59, 130, 246, 0.1)' : 'rgba(203, 213, 225, 0.2)',
              color: index <= activeStep ? '#3B82F6' : '#94A3B8',
              transition: 'all 0.3s ease',
              mb: 2,
              zIndex: 1
            }}>
              {index === activeStep ? (
                <CircularProgress size={24} sx={{ color: '#3B82F6' }} />
              ) : index < activeStep ? (
                <CheckCircleIcon />
              ) : (
                step.icon
              )}
            </Box>

            {/* Step label */}
            <Typography 
              variant="body2" 
              sx={{ 
                color: index <= activeStep ? '#1E293B' : '#94A3B8',
                textAlign: 'center',
                fontWeight: index === activeStep ? 500 : 400,
                transition: 'all 0.3s ease'
              }}
            >
              {step.label}
            </Typography>
          </Box>
        ))}
      </Box>

      {/* Current step description */}
      <Box sx={{
        textAlign: 'center',
        p: 3,
        bgcolor: 'rgba(59, 130, 246, 0.05)',
        borderRadius: '12px',
        border: '1px solid rgba(59, 130, 246, 0.1)'
      }}>
        <Typography sx={{ color: '#3B82F6', fontWeight: 500, mb: 1 }}>
          {loadingSteps[activeStep].label}
        </Typography>
        <Typography sx={{ color: '#64748B' }}>
          {loadingSteps[activeStep].description}
        </Typography>
      </Box>

      {/* Overall progress */}
      <Box sx={{ mt: 4 }}>
        <LinearProgress 
          variant="determinate" 
          value={(activeStep + 1) * (100 / loadingSteps.length)}
          sx={{
            height: 6,
            borderRadius: 3,
            bgcolor: 'rgba(203, 213, 225, 0.2)',
            '& .MuiLinearProgress-bar': {
              bgcolor: '#3B82F6',
              borderRadius: 3,
            }
          }}
        />
        <Typography 
          variant="body2" 
          sx={{ 
            color: '#64748B',
            textAlign: 'center',
            mt: 2 
          }}
        >
          {Math.round((activeStep + 1) * (100 / loadingSteps.length))}% Complete
        </Typography>
      </Box>
    </Box>
  );

  const renderUploadSection = () => (
    <Box
      sx={{
        position: 'relative',
        borderRadius: '24px',
        background: 'white',
        border: '1px solid rgba(59, 130, 246, 0.1)',
        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
        p: 4,
        mb: 4,
      }}
    >
      <Grid container spacing={4}>
        {/* Header Section */}
        <Grid item xs={12} sx={{ textAlign: 'center', mb: 2 }}>
          <Typography 
            variant="h4" 
            sx={{ 
              fontWeight: 700,
              background: 'linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              mb: 2
            }}
          >
            Resume Structure Analysis
          </Typography>
          <Typography variant="body1" sx={{ color: '#64748B', maxWidth: '600px', margin: '0 auto' }}>
            Get instant feedback on your resume's effectiveness and ATS compatibility
          </Typography>
        </Grid>

        {/* Process Steps */}
        <Grid item xs={12}>
          <Box sx={{ display: 'flex', justifyContent: 'center', gap: 4, flexWrap: 'wrap', mb: 4 }}>
            {[
              {
                icon: <CloudUploadIcon sx={{ fontSize: 32, color: '#3B82F6' }} />,
                title: 'Upload Resume',
                description: 'PDF or Word format'
              },
              {
                icon: <AnalyticsIcon sx={{ fontSize: 32, color: '#3B82F6' }} />,
                title: 'AI Analysis',
                description: 'Instant ATS scan'
              },
              {
                icon: <LightbulbIcon sx={{ fontSize: 32, color: '#3B82F6' }} />,
                title: 'Get Insights',
                description: 'Actionable feedback'
              }
            ].map((step, index) => (
              <Box 
                key={index}
                sx={{
                  textAlign: 'center',
                  position: 'relative',
                  width: '180px'
                }}
              >
                <Box sx={{
                  width: 64,
                  height: 64,
                  borderRadius: '16px',
                  bgcolor: 'rgba(59, 130, 246, 0.1)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '0 auto',
                  mb: 2
                }}>
                  {step.icon}
                </Box>
                <Typography variant="h6" sx={{ mb: 1, color: '#1E293B' }}>
                  {step.title}
                </Typography>
                <Typography variant="body2" sx={{ color: '#64748B' }}>
                  {step.description}
                </Typography>
                
                {/* Connector line between steps */}
                {index < 2 && (
                  <Box sx={{
                    position: 'absolute',
                    top: '32px',
                    right: '-40px',
                    width: '40px',
                    height: '2px',
                    bgcolor: 'rgba(59, 130, 246, 0.2)',
                    display: { xs: 'none', md: 'block' }
                  }} />
                )}
              </Box>
            ))}
          </Box>
        </Grid>

        {/* Upload Section */}
        <Grid item xs={12} sx={{ textAlign: 'center' }}>
          <Box sx={{ 
            maxWidth: '400px', 
            margin: '0 auto',
            p: 3,
            borderRadius: '16px',
            bgcolor: 'rgba(59, 130, 246, 0.05)',
            border: '1px dashed rgba(59, 130, 246, 0.2)'
          }}>
            <input
              accept=".pdf,.docx"
              style={{ display: 'none' }}
              id="contained-button-file"
              type="file"
              onChange={handleFileChange}
            />
            
            {!file ? (
              <Box>
                <label htmlFor="contained-button-file">
                  <Button
                    variant="contained"
                    component="span"
                    startIcon={<CloudUploadIcon />}
                    sx={{
                      background: 'linear-gradient(135deg, #3B82F6 0%, #2563EB 100%)',
                      '&:hover': {
                        background: 'linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%)',
                      },
                      mb: 2
                    }}
                  >
                    Upload Resume
                  </Button>
                </label>
                <Typography variant="body2" sx={{ color: '#64748B' }}>
                  Supported formats: PDF, DOCX
                </Typography>
              </Box>
            ) : (
              <Box>
                <CheckCircleIcon sx={{ fontSize: 40, color: '#10B981', mb: 2 }} />
                <Typography sx={{ color: '#1E293B', mb: 2 }}>
                  {file.name}
                </Typography>
                <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
                  <Button
                    variant="outlined"
                    onClick={() => setFile(null)}
                    sx={{
                      color: '#64748B',
                      borderColor: 'rgba(100, 116, 139, 0.5)',
                    }}
                  >
                    Remove
                  </Button>
                  <Button
                    variant="contained"
                    onClick={handleSubmit}
                    disabled={loading}
                    sx={{
                      background: 'linear-gradient(135deg, #3B82F6 0%, #2563EB 100%)',
                      '&:hover': {
                        background: 'linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%)',
                      },
                    }}
                  >
                    {loading ? 'Analyzing...' : 'Start Analysis'}
                  </Button>
                </Box>
              </Box>
            )}
          </Box>
        </Grid>
      </Grid>
    </Box>
  );

  const renderATSScore = () => {
    if (!analysis) return null;
    return (
      <Box textAlign="center" mb={4}>
        <Typography variant="h4" gutterBottom>ATS Compatibility Score</Typography>
        <Box position="relative" display="inline-flex">
          <CircularProgress
            variant="determinate"
            value={analysis.ATS_Compatibility_Score}
            size={200}
            thickness={4}
            sx={{ color: getScoreColor(analysis.ATS_Compatibility_Score) }}
          />
          <Box
            position="absolute"
            top={0}
            left={0}
            bottom={0}
            right={0}
            display="flex"
            alignItems="center"
            justifyContent="center"
          >
            <Typography variant="h3" component="div" color="text.secondary">
              {analysis.ATS_Compatibility_Score}%
            </Typography>
          </Box>
        </Box>
      </Box>
    );
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'success.main';
    if (score >= 60) return 'warning.main';
    return 'error.main';
  };

  const renderContentMetrics = () => {
    const { Content_Analysis, Industry_Standards } = analysis || {};
    if (!Content_Analysis || !Industry_Standards) return null;

    const metrics = [
      { label: 'Word Count', value: Content_Analysis.Total_Word_Count, range: Industry_Standards.Word_Count_Range },
      { label: 'Bullet Points', value: Content_Analysis.Bullet_Points_Count, range: Industry_Standards.Bullet_Points_Range },
      { label: 'Action Verbs', value: Content_Analysis.Action_Verbs_Count },
      { label: 'Quantifiable Achievements', value: Content_Analysis.Quantifiable_Achievements_Count, ideal: Industry_Standards.Ideal_Quantifiable_Achievements },
    ];

    return (
      <Grid container spacing={2} justifyContent="center">
        {metrics.map((metric, index) => (
          <Grid item xs={6} sm={3} key={index}>
            <Paper elevation={2} sx={{ p: 2, height: '100%', textAlign: 'center' }}>
              <Typography variant="h5" color="primary">{metric.value}</Typography>
              <Typography variant="subtitle2">{metric.label}</Typography>
              {metric.range && (
                <Typography variant="caption" color="text.secondary">
                  Industry: {metric.range}
                </Typography>
              )}
              {metric.ideal && (
                <Typography variant="caption" color="text.secondary">
                  Ideal: {metric.ideal}
                </Typography>
              )}
            </Paper>
          </Grid>
        ))}
      </Grid>
    );
  };

  const renderStrengthsAndImprovements = () => {
    if (!analysis) return null;

    const strengths = analysis.Strengths || [];
    const improvements = analysis.ATS_Optimization_Tips || [];

    return (
      <Grid container spacing={3} mt={2}>
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ p: 2, height: '100%', bgcolor: '#e8f5e9' }}>
            <Typography variant="h6" gutterBottom>
              <ThumbUpIcon sx={{ verticalAlign: 'middle', mr: 1 }} />
              Strengths
            </Typography>
            <List dense>
              {strengths.map((strength, index) => (
                <ListItem key={index}>
                  <ListItemIcon><CheckCircleIcon color="success" /></ListItemIcon>
                  <ListItemText primary={strength} />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ p: 2, height: '100%', bgcolor: '#fff3e0' }}>
            <Typography variant="h6" gutterBottom>
              <BuildIcon sx={{ verticalAlign: 'middle', mr: 1 }} />
              Possible Improvements
            </Typography>
            <List dense>
              {improvements.map((improvement, index) => (
                <ListItem key={index}>
                  <ListItemIcon><WarningIcon color="warning" /></ListItemIcon>
                  <ListItemText primary={improvement} />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
      </Grid>
    );
  };

  const renderKeywordsAnalysis = () => {
    const { Keywords_Analysis, Industry_Standards } = analysis || {};
    if (!Keywords_Analysis || !Industry_Standards) return null;

    return (
      <Box mb={3}>
        <Typography variant="h6" gutterBottom>Key Terms</Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Paper elevation={2} sx={{ p: 2, height: '100%' }}>
              <Typography variant="subtitle1" gutterBottom>Present in Your Resume</Typography>
              <Box display="flex" flexWrap="wrap" gap={1}>
                {Keywords_Analysis.Present_Keywords.map((keyword, index) => (
                  <Chip key={index} label={keyword} color="primary" variant="outlined" />
                ))}
              </Box>
            </Paper>
          </Grid>
          <Grid item xs={12} md={6}>
            <Paper elevation={2} sx={{ p: 2, height: '100%' }}>
              <Typography variant="subtitle1" gutterBottom>Suggested Additions</Typography>
              <Box display="flex" flexWrap="wrap" gap={1}>
                {Keywords_Analysis.Missing_Keywords.map((keyword, index) => (
                  <Chip key={index} label={keyword} color="secondary" variant="outlined" />
                ))}
              </Box>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    );
  };

  const renderSectionOrder = () => {
    const { ATS_Friendly_Structure } = analysis || {};
    if (!ATS_Friendly_Structure) return null;

    const { Section_Order, Recommended_Section_Order } = ATS_Friendly_Structure;

    return (
      <Box mb={3}>
        <Typography variant="h6" gutterBottom>Resume Section Order</Typography>
        <Paper elevation={2} sx={{ p: 2, position: 'relative' }}>
          <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
            <Typography variant="subtitle1">Current Order</Typography>
            <Typography variant="subtitle1">Recommended Order</Typography>
          </Box>
          <Box display="flex" justifyContent="space-between" position="relative">
            <Box flex={1}>
              {Section_Order.map((section, index) => (
                <Chip
                  key={index}
                  label={section}
                  sx={{ m: 0.5 }}
                  color={Recommended_Section_Order[index] === section ? 'primary' : 'default'}
                />
              ))}
            </Box>
            <Box
              position="absolute"
              top="50%"
              left="50%"
              sx={{ transform: 'translate(-50%, -50%)' }}
            >
              <ArrowForwardIcon color="action" fontSize="large" />
            </Box>
            <Box flex={1} textAlign="right">
              {Recommended_Section_Order.map((section, index) => (
                <Chip
                  key={index}
                  label={section}
                  sx={{ m: 0.5 }}
                  color="primary"
                />
              ))}
            </Box>
          </Box>
        </Paper>
      </Box>
    );
  };

  const renderATSFriendlyStructure = () => {
    const { ATS_Friendly_Structure, Industry_Standards } = analysis || {};
    if (!ATS_Friendly_Structure || !Industry_Standards) return null;

    return (
      <Box mb={3}>
        <Typography variant="h6" gutterBottom>ATS-Friendly Structure</Typography>
        <Paper elevation={2} sx={{ p: 2 }}>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle1">Format Score: {ATS_Friendly_Structure.Format_Score}/10</Typography>
              <LinearProgress 
                variant="determinate" 
                value={ATS_Friendly_Structure.Format_Score * 10} 
                sx={{ mt: 1, mb: 2, height: 10, borderRadius: 5 }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle1">File Format Preference</Typography>
              <Typography variant="body2">{Industry_Standards.File_Format_Preference}</Typography>
            </Grid>
          </Grid>
        </Paper>
      </Box>
    );
  };

  const renderIndustrySpecificSuggestions = () => {
    const { Industry_Specific_Suggestions, Industry_Standards } = analysis || {};
    if (!Industry_Specific_Suggestions || !Industry_Standards) return null;

    const radarData = {
      labels: Object.keys(Industry_Standards.Sections_Importance),
      datasets: [
        {
          label: 'Section Importance',
          data: Object.values(Industry_Standards.Sections_Importance),
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1,
        },
      ],
    };

    return (
      <Box mb={3}>
        <Typography variant="h6" gutterBottom>Industry-Specific Analysis</Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Paper elevation={2} sx={{ p: 2, height: '100%' }}>
              <Typography variant="subtitle1" gutterBottom>Inferred Industry: {Industry_Specific_Suggestions.Inferred_Industry}</Typography>
              <Typography variant="subtitle1" gutterBottom>Top Industry Keywords:</Typography>
              <Box display="flex" flexWrap="wrap" gap={1}>
                {Industry_Specific_Suggestions.Industry_Keywords.slice(0, 15).map((keyword, index) => (
                  <Chip key={index} label={keyword} color="primary" size="small" />
                ))}
              </Box>
            </Paper>
          </Grid>
          <Grid item xs={12} md={6}>
            <Paper elevation={2} sx={{ p: 2, height: '100%' }}>
              <Typography variant="subtitle1" gutterBottom>Section Importance</Typography>
              <Box height={250}>
                <Radar data={radarData} options={{ maintainAspectRatio: false }} />
              </Box>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    );
  };

  return (
    <motion.div
      initial={{ 
        opacity: 0,
        y: 20  // Reduced from 40 to make it more subtle
      }}
      animate={{ 
        opacity: 1,
        y: 0
      }}
      transition={{ 
        duration: 0.5,  // Increased from 0.3 to match SuggestKeywords
        ease: "easeOut"  // Simplified easing function to prevent glitch
      }}
      style={{ 
        width: '100%',  // Prevent layout shift
        height: '100%',
        willChange: 'transform'  // Optimize animation performance
      }}
    >
      <Box sx={{
        minHeight: '100vh',
        background: 'linear-gradient(145deg, #f6f8fc 0%, #eef2ff 100%)',
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

        {/* AppBar with exact same positioning */}
        <AppBar position="static" elevation={0} 
          sx={{ 
            background: 'transparent', 
            backdropFilter: 'blur(10px)',
            borderBottom: '1px solid rgba(255, 255, 255, 0.1)'
          }}>
          <Container maxWidth="xl">
            <Toolbar sx={{ px: { xs: 0, sm: 2 } }}>
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
                  '&:hover': {
                    opacity: 0.8
                  }
                }}>
                Resume Helper AI
              </Typography>
              
              {analysis && (
                <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                  <IconButton onClick={handleStartNew} 
                    sx={{ 
                      color: '#1E3A8A',
                      background: 'rgba(255, 255, 255, 0.1)',
                      backdropFilter: 'blur(10px)',
                      mr: 1,
                      '&:hover': { background: 'rgba(255, 255, 255, 0.2)' }
                    }}>
                    <RefreshIcon />
                  </IconButton>
                </motion.div>
              )}

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

        {/* Main content with exact same container settings */}
        <Container maxWidth="xl" sx={{ mt: { xs: 4, md: 8 }, position: 'relative', zIndex: 1 }}>
          {renderUploadSection()}
          {error && (
            <Alert severity="error" sx={{ mt: 2, mb: 4 }}>
              {error}
            </Alert>
          )}
          {loading && renderLoadingState()}
          {analysis && (
            <Fade in={true} timeout={1000}>
              <Box
                sx={{
                  background: 'white',
                  borderRadius: '24px',
                  border: '1px solid rgba(59, 130, 246, 0.1)',
                  boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                  p: 4,
                }}
              >
                {renderATSScore()}
                {renderContentMetrics()}
                {renderStrengthsAndImprovements()}
                <Divider sx={{ my: 4, bgcolor: 'rgba(255, 255, 255, 0.1)' }} />
                {renderKeywordsAnalysis()}
                {renderSectionOrder()}
                {renderATSFriendlyStructure()}
                {renderIndustrySpecificSuggestions()}
                <Accordion sx={{
                  background: 'white',
                  color: '#1E293B',
                  '&.Mui-expanded': {
                    margin: 0,
                  },
                }}>
                  <AccordionSummary expandIcon={<ExpandMoreIcon sx={{ color: '#1E293B' }} />}>
                    <Typography>Overall Assessment</Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Typography variant="body1" sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
                      {analysis.Overall_Assessment}
                    </Typography>
                  </AccordionDetails>
                </Accordion>
              </Box>
            </Fade>
          )}
        </Container>
      </Box>
    </motion.div>
  );
};

export default AnalyzeResumeStructure;
