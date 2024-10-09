import React, { useState } from 'react';
import {
  Box, Button, Typography, CircularProgress, Paper, Grid,
  List, ListItem, ListItemIcon, ListItemText, Divider,
  Container, Fade, Alert, LinearProgress, Modal, Tooltip
} from '@mui/material';
import { 
  CloudUpload as CloudUploadIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
  CheckCircleOutline
} from '@mui/icons-material';

const AnalyzeResumeStructure = () => {
  const [file, setFile] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedMetric, setSelectedMetric] = useState(null);

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

  const handleMetricClick = (metric) => {
    console.log("Clicked metric:", metric);
    const industryKey = metric.key.replace(/_/g, ' ');
    const industryValue = analysis['Industry Comparison'][`Typical ${industryKey} Range`];
    setSelectedMetric({
      key: metric.key,
      value: metric.value,
      industryValue: industryValue
    });
    console.log("Set selectedMetric:", {
      key: metric.key,
      value: metric.value,
      industryValue: industryValue
    });
    setModalOpen(true);
  };

  const renderMetrics = () => {
    const { Metrics, 'Industry Comparison': industryComparison } = analysis || {};
    return (
      <Grid container spacing={2}>
        {Metrics && Object.entries(Metrics).map(([key, value]) => {
          const industryValue = industryComparison ? industryComparison[key.replace(/_/g, ' ')] : null;
          console.log(`Metric: ${key}, Value: ${value}, Industry Value: ${industryValue}`);
          const industryRange = industryValue ? industryValue.split('-').map(v => parseFloat(v)) : null;
          const progressValue = industryRange ? ((value - industryRange[0]) / (industryRange[1] - industryRange[0])) * 100 : 0;

          return (
            <Grid item xs={12} sm={6} md={4} key={key}>
              <Tooltip title={`Click for more details on ${key.split('_').join(' ')}`} arrow>
                <Paper 
                  elevation={3} 
                  sx={{ 
                    p: 2, 
                    textAlign: 'center', 
                    height: '100%', 
                    background: 'linear-gradient(135deg, #f6d365 0%, #fda085 100%)',
                    cursor: 'pointer',
                    '&:hover': {
                      boxShadow: 6,
                    }
                  }}
                  onClick={() => handleMetricClick({ 
                    key, 
                    value, 
                    industryValue 
                  })}
                >
                  <Typography variant="h6">{value}</Typography>
                  <Typography variant="body2" color="textSecondary">
                    {key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                  </Typography>
                  {industryValue && (
                    <Box sx={{ mt: 1 }}>
                      <Typography variant="caption" color="textSecondary">
                        Industry Standard: {industryValue}
                      </Typography>
                      <LinearProgress 
                        variant="determinate" 
                        value={Math.min(Math.max(progressValue, 0), 100)} 
                        sx={{ mt: 1 }}
                      />
                    </Box>
                  )}
                </Paper>
              </Tooltip>
            </Grid>
          );
        })}
      </Grid>
    );
  };

  const renderAnalysisSection = (title, items, icon) => (
    <Box mb={3}>
      <Typography variant="h6" gutterBottom>{title}</Typography>
      <List>
        {items && items.map((item, index) => (
          <ListItem key={index}>
            <ListItemIcon>{icon}</ListItemIcon>
            <ListItemText primary={item} />
          </ListItem>
        ))}
      </List>
    </Box>
  );

  const renderContentAnalysis = () => {
    const { Content } = analysis || {};
    return (
      <Grid container spacing={2}>
        {Content && Object.entries(Content).map(([key, value]) => (
          <Grid item xs={12} sm={6} md={4} key={key}>
            <Paper elevation={3} sx={{ 
              p: 2, 
              height: '100%', 
              background: 'linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%)' 
            }}>
              <Typography variant="subtitle1" gutterBottom>
                {key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
              </Typography>
              <Typography variant="body2">{value}</Typography>
            </Paper>
          </Grid>
        ))}
      </Grid>
    );
  };

  const renderIndustryComparison = () => {
    const { 'Industry Comparison': industryComparison } = analysis || {};
    if (!industryComparison) return null;

    return (
      <Box mb={3}>
        <Typography variant="h6" gutterBottom>Industry Comparison</Typography>
        <List>
          {Object.entries(industryComparison).map(([key, value], index) => (
            <ListItem key={index}>
              <ListItemIcon><InfoIcon color="info" /></ListItemIcon>
              <ListItemText 
                primary={`${key}: ${value}`} 
                primaryTypographyProps={{ variant: 'body2' }}
              />
            </ListItem>
          ))}
        </List>
      </Box>
    );
  };

  const renderModalContent = () => {
    console.log("Rendering modal content with selectedMetric:", selectedMetric);
    if (!selectedMetric) return null;
    const { key, value, industryValue } = selectedMetric;
    const industryRange = industryValue ? industryValue.split('-').map(v => parseFloat(v)) : null;
    const isAboveIndustry = industryRange && value > industryRange[1];
    const isBelowIndustry = industryRange && value < industryRange[0];

    const getAdvice = () => {
      if (key === "Number_of_Action_Verbs_Used") {
        if (isAboveIndustry) {
          return "Your resume has a strong use of action verbs, which can make your achievements more impactful. Consider reviewing to ensure all verbs are varied and relevant.";
        } else if (isBelowIndustry) {
          return "Consider incorporating more action verbs to make your achievements more dynamic and impactful. Focus on verbs that showcase your skills and accomplishments.";
        } else {
          return "Your use of action verbs is within the industry standard. To further improve, ensure each verb is impactful and directly relates to your achievements.";
        }
      }
      // Add similar conditions for other metrics
      return "";
    };

    return (
      <Box sx={{ p: 4 }}>
        <Typography variant="h6" gutterBottom>
          {key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
        </Typography>
        <Typography variant="body1" gutterBottom>
          Your Value: {value}
        </Typography>
        <Typography variant="body1" gutterBottom>
          Industry Standard: {industryValue || 'Not available'}
        </Typography>
        {industryRange && (
          <>
            <Typography variant="body2" color={isAboveIndustry ? "success.main" : (isBelowIndustry ? "error.main" : "textSecondary")}>
              {isAboveIndustry ? "Above" : (isBelowIndustry ? "Below" : "Within")} industry standard
            </Typography>
            <Typography variant="body2" sx={{ mt: 2 }}>
              {getAdvice()}
            </Typography>
          </>
        )}
      </Box>
    );
  };

  return (
    <Box sx={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      background: 'linear-gradient(120deg, #8b5cf6 0%, #3b82f6 100%)',
    }}>
      <Container maxWidth="md">
        <Fade in={true}>
          <Paper elevation={3} sx={{ p: 4, borderRadius: '16px' }}>
            <Typography variant="h4" component="h1" gutterBottom align="center">
              Analyze Resume Structure
            </Typography>
            <Box mb={3}>
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
                >
                  Upload Resume
                </Button>
              </label>
              {file && (
                <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                  <CheckCircleOutline sx={{ color: 'green', mr: 1 }} />
                  <Typography variant="body2">{file.name}</Typography>
                </Box>
              )}
            </Box>
            <Button
              variant="contained"
              onClick={handleSubmit}
              disabled={!file || loading}
              sx={{
                bgcolor: '#8b5cf6',
                color: 'white',
                '&:hover': {
                  bgcolor: '#7c3aed',
                },
              }}
            >
              {loading ? <CircularProgress size={24} /> : 'Analyze Resume'}
            </Button>
            {error && (
              <Alert severity="error" sx={{ mt: 2 }}>
                {error}
              </Alert>
            )}
            {analysis && (
              <Fade in={true} timeout={1000}>
                <Box mt={4}>
                  <Typography variant="h5" gutterBottom sx={{ color: '#8b5cf6' }}>
                    Analysis Results
                  </Typography>
                  {renderMetrics()}
                  <Divider sx={{ my: 3 }} />
                  <Typography variant="h6" gutterBottom>Overall Assessment</Typography>
                  <Typography variant="body1" paragraph>{analysis.Overall_Assessment}</Typography>
                  {renderContentAnalysis()}
                  <Divider sx={{ my: 3 }} />
                  {renderAnalysisSection('Strengths', analysis.Strengths, <CheckCircleIcon color="success" />)}
                  {renderAnalysisSection('Areas for Improvement', analysis['Areas for Improvement'], <WarningIcon color="warning" />)}
                  {renderAnalysisSection('Recommendations', analysis.Recommendations, <InfoIcon color="info" />)}
                </Box>
              </Fade>
            )}
          </Paper>
        </Fade>
      </Container>
      <Modal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        aria-labelledby="metric-modal-title"
        aria-describedby="metric-modal-description"
      >
        <Box sx={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: 400,
          bgcolor: 'background.paper',
          boxShadow: 24,
          p: 4,
          borderRadius: '8px'
        }}>
          {renderModalContent()}
        </Box>
      </Modal>
    </Box>
  );
};

export default AnalyzeResumeStructure;