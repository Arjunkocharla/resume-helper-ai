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
import { motion, AnimatePresence } from 'framer-motion';
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
  const [retryCount, setRetryCount] = useState(0);
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
      setError('Please upload a resume file');
      return;
    }

    setError('');
    setAnalysis(null);
    setLoading(true);

    try {
      // First attempt
      const data = await callAnalyzeAPI(false);
      setAnalysis(data);
    } catch (err) {
      console.error('First attempt failed:', err);
      try {
        // Retry with retry=true if first attempt fails
        const retryData = await callAnalyzeAPI(true);
        setAnalysis(retryData);
      } catch (retryErr) {
        console.error('Retry attempt failed:', retryErr);
        setError('Failed to analyze resume after multiple attempts. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const callAnalyzeAPI = async (retry = false) => {
    const formData = new FormData();
    formData.append('resume', file);
    formData.append('retry', retry.toString());

    const response = await fetch('http://127.0.0.1:5000/analyze_resume_structure', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) throw new Error('Failed to analyze resume');
    return await response.json();
  };

  const handleHomeClick = () => navigate('/');
  const handleProfileClick = () => navigate('/profile');
  const handleRestart = () => {
    setFile(null);
    setAnalysis(null);
    setActiveStep(0);
    setError(null);
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
    <Box
      sx={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'rgba(255, 255, 255, 0.9)',
        backdropFilter: 'blur(8px)',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
        p: 3
      }}
    >
      {/* Animated Logo or Icon */}
      <motion.div
        animate={{
          scale: [1, 1.1, 1],
          rotate: [0, 360],
        }}
        transition={{
          duration: 2,
          repeat: Infinity,
          ease: "easeInOut"
        }}
        style={{ marginBottom: '2rem' }}
      >
        <DescriptionIcon sx={{ fontSize: 48, color: '#3B82F6' }} />
      </motion.div>

      {/* Steps Progress */}
      <Box sx={{ 
        maxWidth: '800px',
        width: '100%',
        background: 'white',
        borderRadius: '24px',
        p: { xs: 3, md: 4 },
        boxShadow: '0 4px 20px rgba(0, 0, 0, 0.1)'
      }}>
        {/* Current Step Info */}
        <Box sx={{ mb: 4, textAlign: 'center' }}>
          <Typography variant="h5" sx={{ color: '#1E3A8A', mb: 1, fontWeight: 600 }}>
            {loadingSteps[activeStep].label}
          </Typography>
          <Typography sx={{ color: '#64748B' }}>
            {loadingSteps[activeStep].description}
          </Typography>
        </Box>

        {/* Progress Steps */}
        <Box sx={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          mb: 4,
          position: 'relative'
        }}>
          {loadingSteps.map((step, index) => (
            <Box
              key={step.label}
              sx={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                position: 'relative',
                zIndex: 1
              }}
            >
              <motion.div
                animate={index <= activeStep ? {
                  scale: [1, 1.2, 1],
                  transition: { duration: 0.5 }
                } : {}}
              >
                <Box sx={{
                  width: 40,
                  height: 40,
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  bgcolor: index <= activeStep ? '#3B82F6' : 'rgba(203, 213, 225, 0.2)',
                  color: index <= activeStep ? 'white' : '#94A3B8',
                  transition: 'all 0.3s ease',
                  mb: 1
                }}>
                  {index === activeStep ? (
                    <CircularProgress size={24} sx={{ color: 'white' }} />
                  ) : index < activeStep ? (
                    <CheckCircleIcon />
                  ) : (
                    step.icon
                  )}
                </Box>
              </motion.div>
              <Typography 
                variant="caption" 
                sx={{ 
                  color: index <= activeStep ? '#1E3A8A' : '#94A3B8',
                  fontWeight: index === activeStep ? 600 : 400
                }}
              >
                {step.label}
              </Typography>
            </Box>
          ))}

          {/* Progress Line */}
          <Box sx={{
            position: 'absolute',
            top: 20,
            left: 40,
            right: 40,
            height: 2,
            bgcolor: 'rgba(203, 213, 225, 0.2)',
            zIndex: 0
          }}>
            <Box sx={{
              width: `${(activeStep / (loadingSteps.length - 1)) * 100}%`,
              height: '100%',
              bgcolor: '#3B82F6',
              transition: 'width 0.3s ease'
            }} />
          </Box>
        </Box>

        {/* Overall Progress */}
        <Box sx={{ textAlign: 'center' }}>
          <Typography variant="h4" sx={{ color: '#1E3A8A', fontWeight: 700 }}>
            {Math.round((activeStep + 1) * (100 / loadingSteps.length))}%
          </Typography>
          <Typography variant="body2" sx={{ color: '#64748B' }}>
            Analysis Complete
          </Typography>
        </Box>
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
        p: { xs: 3, md: 4 },
        mb: 4,
        maxWidth: '800px',
        mx: 'auto',
      }}
    >
      <Grid container spacing={3}>
        {/* Header Section */}
        <Grid item xs={12} sx={{ textAlign: 'center', mb: 1 }}>
          <Typography 
            variant="h5" 
            sx={{ 
              fontWeight: 700,
              background: 'linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              mb: 1
            }}
          >
            Resume Structure Analysis
          </Typography>
          <Typography variant="body2" sx={{ color: '#64748B', maxWidth: '500px', margin: '0 auto' }}>
            Get instant feedback on your resume's effectiveness and ATS compatibility
          </Typography>
        </Grid>

        {/* Process Steps */}
        <Grid item xs={12}>
          <Box sx={{ 
            display: 'flex', 
            justifyContent: 'center', 
            gap: { xs: 2, md: 3 }, 
            flexWrap: 'wrap', 
            mb: 3
          }}>
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
                  width: { xs: '140px', md: '160px' }
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
            maxWidth: '350px',
            margin: '0 auto',
            p: { xs: 2, md: 3 },
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
    const { Keywords_Analysis, Industry_Specific_Suggestions } = analysis || {};
    if (!Keywords_Analysis) return null;

    const chipStyles = {
      background: '#3B82F6',
      color: 'white',
      fontWeight: 500,
      '&:hover': {
        transform: 'translateY(-2px)',
        boxShadow: '0 4px 12px rgba(59, 130, 246, 0.2)'
      },
      transition: 'all 0.2s ease-in-out'
    };

    return (
      <Box mb={4}>
        <Typography variant="h6" gutterBottom>Key Terms</Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} mb={2}>
            <Typography variant="subtitle1" sx={{ color: '#3B82F6', fontWeight: 500 }}>
              Inferred Industry: {Industry_Specific_Suggestions?.Inferred_Industry}
            </Typography>
          </Grid>
          <Grid item xs={12} md={6}>
            <Paper 
              elevation={0} 
              sx={{ 
                p: 3,
                background: 'linear-gradient(145deg, #ffffff, #f3f4f6)',
                borderRadius: '16px',
                boxShadow: '0 4px 15px rgba(0, 0, 0, 0.05)'
              }}
            >
              <Typography variant="subtitle1" gutterBottom>Present Keywords</Typography>
              <Box display="flex" flexWrap="wrap" gap={1}>
                {Keywords_Analysis.Present_Keywords.map((keyword, index) => (
                  <Chip
                    key={index}
                    label={keyword}
                    sx={chipStyles}
                  />
                ))}
              </Box>
            </Paper>
          </Grid>
          <Grid item xs={12} md={6}>
            <Paper 
              elevation={0} 
              sx={{ 
                p: 3,
                background: 'linear-gradient(145deg, #ffffff, #f3f4f6)',
                borderRadius: '16px',
                boxShadow: '0 4px 15px rgba(0, 0, 0, 0.05)'
              }}
            >
              <Typography variant="subtitle1" gutterBottom>Suggested Keywords</Typography>
              <Box display="flex" flexWrap="wrap" gap={1}>
                {Keywords_Analysis.Missing_Keywords.map((keyword, index) => (
                  <Chip
                    key={index}
                    label={keyword}
                    sx={chipStyles}
                  />
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

  const renderImprovements = () => (
    <Box sx={{ mt: 4 }}>
      <Typography 
        variant="h5" 
        sx={{ 
          mb: 3,
          color: '#1E293B',
          fontWeight: 600,
          fontSize: '1.5rem'
        }}
      >
        Recommended Improvements
      </Typography>
      <Grid container spacing={2}>
        {analysis?.Tailored_Improvement_Plan?.map((improvement, index) => (
          <Grid item xs={12} key={index}>
            <Box
              sx={{
                background: 'rgba(59, 130, 246, 0.02)',
                borderRadius: '12px',
                p: 2.5,
                border: '1px solid rgba(59, 130, 246, 0.1)',
                transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
                '&:hover': {
                  transform: 'translateY(-2px)',
                  boxShadow: '0 4px 12px rgba(59, 130, 246, 0.08)'
                }
              }}
            >
              <Box sx={{ display: 'flex', gap: 2, alignItems: 'flex-start' }}>
                <BuildIcon sx={{ 
                  color: '#3B82F6',
                  fontSize: 20,
                  mt: 0.5
                }} />
                <Box>
                  <Typography 
                    sx={{ 
                      color: '#1E293B',
                      fontWeight: 500,
                      fontSize: '0.95rem',
                      mb: 0.5
                    }}
                  >
                    {improvement.action || improvement}
                  </Typography>
                  {improvement.reason && (
                    <Typography 
                      sx={{ 
                        color: '#64748B',
                        lineHeight: 1.5,
                        fontSize: '0.875rem'
                      }}
                    >
                      {improvement.reason}
                    </Typography>
                  )}
                </Box>
              </Box>
            </Box>
          </Grid>
        ))}
      </Grid>
    </Box>
  );

  const getRadarData = (analysis) => {
    const { Industry_Standards } = analysis || {};
    if (!Industry_Standards?.Sections_Importance) return null;

    return {
      labels: Object.keys(Industry_Standards.Sections_Importance),
      datasets: [
        {
          label: 'Section Importance',
          data: Object.values(Industry_Standards.Sections_Importance),
          backgroundColor: 'rgba(59, 130, 246, 0.2)',
          borderColor: '#3B82F6',
          borderWidth: 2,
          pointBackgroundColor: '#3B82F6',
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: '#3B82F6'
        }
      ]
    };
  };

  const renderAnalysisResults = () => {
    const radarData = getRadarData(analysis);

    return (
      <Box sx={{
        background: 'white',
        borderRadius: '24px',
        border: '1px solid rgba(59, 130, 246, 0.1)',
        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
        p: 4,
      }}>
        {/* Header with Title and Restart Button */}
        <Box 
          sx={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center',
            mb: 4 
          }}
        >
          <Typography 
            variant="h5" 
            sx={{ 
              fontWeight: 600,
              color: '#1E3A8A'
            }}
          >
            Resume Analysis Results
          </Typography>
          
          <Button
            onClick={handleRestart}
            startIcon={<RefreshIcon />}
            variant="outlined"
            sx={{
              borderColor: '#3B82F6',
              color: '#3B82F6',
              borderRadius: '12px',
              px: 3,
              py: 1,
              '&:hover': {
                borderColor: '#2563EB',
                background: 'rgba(59, 130, 246, 0.05)'
              }
            }}
          >
            New Analysis
          </Button>
        </Box>

        {/* Main Score Card and Stats */}
        <Grid container spacing={4}>
          <Grid item xs={12} md={6}>
            <Paper 
              elevation={0} 
              sx={{ 
                p: 4,
                background: 'linear-gradient(135deg, #EBF3FF 0%, #D6E8FF 100%)',
                borderRadius: '20px',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                gap: 2
              }}
            >
              <Typography variant="h5" sx={{ fontWeight: 600, mb: 2 }}>Resume Score</Typography>
              <Box sx={{ position: 'relative', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                <CircularProgress 
                  variant="determinate" 
                  value={analysis?.ATS_Compatibility_Score || 0}
                  size={200}
                  thickness={4}
                  sx={{
                    color: '#3B82F6',
                    '& .MuiCircularProgress-circle': {
                      strokeLinecap: 'round',
                      filter: 'drop-shadow(0px 4px 8px rgba(59, 130, 246, 0.3))'
                    }
                  }}
                />
                <Typography 
                  variant="h2" 
                  sx={{ 
                    position: 'absolute',
                    fontWeight: 700,
                    color: '#1E3A8A'
                  }}
                >
                  {analysis?.ATS_Compatibility_Score}%
                </Typography>
              </Box>
            </Paper>
          </Grid>

          {/* Quick Stats Cards */}
          <Grid item xs={12} md={6}>
            <Grid container spacing={2}>
              {[
                { 
                  label: 'Keywords Match', 
                  value: `${analysis?.Keywords_Analysis?.Present_Keywords?.length || 0}/${(analysis?.Keywords_Analysis?.Present_Keywords?.length || 0) + (analysis?.Keywords_Analysis?.Missing_Keywords?.length || 0)}`,
                  icon: <CheckCircleIcon sx={{ color: '#3B82F6' }} />
                },
                { 
                  label: 'Format Score', 
                  value: `${analysis?.ATS_Friendly_Structure?.Format_Score || 0}/10`,
                  icon: <DescriptionIcon sx={{ color: '#3B82F6' }} />
                },
                { 
                  label: 'Keyword Density', 
                  value: analysis?.Keywords_Analysis?.Keyword_Density || '0%',
                  icon: <AnalyticsIcon sx={{ color: '#3B82F6' }} />
                },
                { 
                  label: 'Sections', 
                  value: analysis?.ATS_Friendly_Structure?.Section_Order?.length || 0,
                  icon: <CompareArrowsIcon sx={{ color: '#3B82F6' }} />
                }
              ].map((stat, index) => (
                <Grid item xs={6} key={index}>
                  <Paper 
                    elevation={0} 
                    sx={{ 
                      p: 3,
                      height: '100%',
                      borderRadius: '16px',
                      border: '1px solid rgba(59, 130, 246, 0.1)',
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'center',
                      gap: 1
                    }}
                  >
                    {stat.icon}
                    <Typography variant="h4" sx={{ fontWeight: 700, color: '#1E3A8A' }}>
                      {stat.value}
                    </Typography>
                    <Typography variant="body2" sx={{ color: '#64748B' }}>
                      {stat.label}
                    </Typography>
                  </Paper>
                </Grid>
              ))}
            </Grid>
          </Grid>
        </Grid>

        {/* Keywords Analysis with Inferred Industry */}
        {renderKeywordsAnalysis()}
        
        {/* Section Order with animated flow */}
        {renderSectionOrder()}
        
        {/* Improvements at the bottom */}
        {renderImprovements()}
      </Box>
    );
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Box sx={{ 
        minHeight: '100vh', 
        background: 'linear-gradient(135deg, #FFFFFF 0%, #EBF3FF 35%, #D6E8FF 65%, #B6DCFE 100%)',
        position: 'relative',
        overflow: 'hidden'
      }}>
        {/* Add the floating background elements */}
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

        {/* Keep existing AppBar */}
        <AppBar position="static" sx={{ background: 'transparent', boxShadow: 'none' }}>
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
                  <IconButton onClick={handleRestart} 
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

        {/* Main Content */}
        <Container maxWidth="lg" sx={{ mt: { xs: 4, md: 6 }, position: 'relative', zIndex: 1 }}>
          <AnimatePresence mode="wait">
            {!analysis ? (
              <motion.div
                key="upload"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.5 }}
              >
                {renderUploadSection()}
              </motion.div>
            ) : (
              <motion.div
                key="results"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
              >
                {renderAnalysisResults()}
              </motion.div>
            )}
          </AnimatePresence>

          {error && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {error}
            </Alert>
          )}
          
          {loading && renderLoadingState()}
        </Container>
      </Box>
    </motion.div>
  );
};

export default AnalyzeResumeStructure;
