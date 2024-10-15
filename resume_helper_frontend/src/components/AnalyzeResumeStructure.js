import React, { useState, useEffect } from 'react';
import {
  Box, Button, Typography, CircularProgress, Paper, Grid,
  List, ListItem, ListItemIcon, ListItemText, Divider,
  Container, Fade, Alert, LinearProgress, Tooltip,
  Accordion, AccordionSummary, AccordionDetails, Chip,
  Card, CardContent, Step, Stepper, StepLabel, StepContent, useTheme
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
  Lightbulb as LightbulbIcon
} from '@mui/icons-material';
import { Radar } from 'react-chartjs-2';
import { Chart as ChartJS, RadialLinearScale, PointElement, LineElement, Filler, Tooltip as ChartTooltip, Legend } from 'chart.js';

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, ChartTooltip, Legend);

const AnalyzeResumeStructure = () => {
  const [file, setFile] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeStep, setActiveStep] = useState(0);
  const theme = useTheme();

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

  const renderLoadingState = () => (
    <Box sx={{ maxWidth: 400, margin: 'auto', mt: 4 }}>
      <Stepper activeStep={activeStep} orientation="vertical">
        {loadingSteps.map((step, index) => (
          <Step key={step.label}>
            <StepLabel
              icon={
                <Box
                  sx={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    width: 40,
                    height: 40,
                    borderRadius: '50%',
                    bgcolor: index === activeStep ? 'primary.main' : 'rgba(255, 255, 255, 0.1)',
                    color: index === activeStep ? 'white' : 'rgba(255, 255, 255, 0.5)',
                  }}
                >
                  {index === activeStep ? (
                    <CircularProgress size={24} sx={{ color: 'white' }} />
                  ) : (
                    index < activeStep ? <CheckCircleIcon /> : step.icon
                  )}
                </Box>
              }
            >
              <Typography sx={{ color: 'white' }}>{step.label}</Typography>
            </StepLabel>
            <StepContent>
              <Typography sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>{step.description}</Typography>
              {index === activeStep && (
                <Box sx={{ mt: 1, mb: 1 }}>
                  <LinearProgress />
                </Box>
              )}
            </StepContent>
          </Step>
        ))}
      </Stepper>
    </Box>
  );

  const renderUploadSection = () => (
    <Box
      sx={{
        position: 'relative',
        overflow: 'hidden',
        borderRadius: '24px',
        background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%)',
        backdropFilter: 'blur(10px)',
        border: '1px solid rgba(255, 255, 255, 0.1)',
        p: 4,
        mb: 4,
      }}
    >
      <Box
        sx={{
          position: 'absolute',
          top: '-50%',
          left: '-50%',
          width: '200%',
          height: '200%',
          background: 'radial-gradient(circle, rgba(16, 185, 129, 0.1) 0%, rgba(59, 130, 246, 0.1) 50%, transparent 70%)',
          animation: 'pulse 15s infinite',
        }}
      />
      <Box sx={{ position: 'relative', zIndex: 1 }}>
        <Typography variant="h4" gutterBottom sx={{ color: 'white', fontWeight: 'bold' }}>
          Analyze Your Resume Structure
        </Typography>
        <Typography variant="body1" paragraph sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
          Upload your resume and get an in-depth analysis of its structure and ATS compatibility.
        </Typography>
        <Box sx={{ my: 3 }}>
          <Stepper activeStep={file ? 1 : 0} alternativeLabel>
            <Step>
              <StepLabel StepIconProps={{ style: { color: theme.palette.primary.main } }}>Upload Resume</StepLabel>
            </Step>
            <Step>
              <StepLabel StepIconProps={{ style: { color: theme.palette.primary.main } }}>Analyze</StepLabel>
            </Step>
          </Stepper>
        </Box>
        <Box display="flex" justifyContent="center" alignItems="center" flexWrap="wrap" gap={2}>
          <input
            accept=".pdf,.docx"
            style={{ display: 'none' }}
            id="contained-button-file"
            type="file"
            onChange={handleFileChange}
          />
          <label htmlFor="contained-button-file">
            <Button
              variant="outlined"
              component="span"
              startIcon={<CloudUploadIcon />}
              sx={{
                color: theme.palette.primary.main,
                borderColor: theme.palette.primary.main,
                '&:hover': {
                  borderColor: theme.palette.primary.main,
                  bgcolor: 'rgba(16, 185, 129, 0.1)',
                },
              }}
            >
              {file ? 'Change Resume' : 'Upload Resume'}
            </Button>
          </label>
          <Button
            variant="contained"
            onClick={handleSubmit}
            disabled={!file || loading}
            sx={{
              bgcolor: theme.palette.primary.main,
              color: 'white',
              '&:hover': {
                bgcolor: theme.palette.primary.dark,
              },
            }}
          >
            {loading ? 'Analyzing...' : 'Analyze Resume'}
          </Button>
        </Box>
        {file && (
          <Typography variant="body2" sx={{ mt: 2, color: 'rgba(255, 255, 255, 0.7)' }}>
            Selected file: {file.name}
          </Typography>
        )}
      </Box>
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
    <Box sx={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #0F172A 0%, #1E293B 100%)',
      py: 4,
    }}>
      <Container maxWidth="lg">
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
                background: 'rgba(255, 255, 255, 0.05)',
                backdropFilter: 'blur(20px)',
                borderRadius: '24px',
                border: '1px solid rgba(255, 255, 255, 0.1)',
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
                background: 'rgba(255, 255, 255, 0.05)',
                color: 'white',
                '&.Mui-expanded': {
                  margin: 0,
                },
              }}>
                <AccordionSummary expandIcon={<ExpandMoreIcon sx={{ color: 'white' }} />}>
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
  );
};

export default AnalyzeResumeStructure;