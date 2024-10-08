import React, { useState } from 'react';
import {
  Box, Button, Typography, CircularProgress, Paper, Grid,
  List, ListItem, ListItemIcon, ListItemText, Divider,
  Container, Fade, Alert
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

  const renderMetrics = () => {
    const { metrics } = analysis;
    return (
      <Grid container spacing={2}>
        {Object.entries(metrics).map(([key, value]) => (
          <Grid item xs={6} sm={3} key={key}>
            <Paper elevation={3} sx={{ p: 2, textAlign: 'center', height: '100%' }}>
              <Typography variant="h6">{value}</Typography>
              <Typography variant="body2" color="textSecondary">
                {key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
              </Typography>
            </Paper>
          </Grid>
        ))}
      </Grid>
    );
  };

  const renderAnalysisSection = (title, items, icon) => (
    <Box mb={3}>
      <Typography variant="h6" gutterBottom>{title}</Typography>
      <List>
        {items.map((item, index) => (
          <ListItem key={index}>
            <ListItemIcon>{icon}</ListItemIcon>
            <ListItemText primary={item} />
          </ListItem>
        ))}
      </List>
    </Box>
  );

  const renderContentAnalysis = () => {
    const { content_analysis } = analysis;
    return (
      <Grid container spacing={2}>
        {Object.entries(content_analysis).map(([key, value]) => (
          <Grid item xs={12} sm={4} key={key}>
            <Paper elevation={3} sx={{ p: 2, height: '100%' }}>
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
                  <Typography variant="body1" paragraph>{analysis.overall_assessment}</Typography>
                  {renderContentAnalysis()}
                  <Divider sx={{ my: 3 }} />
                  {renderAnalysisSection('Strengths', analysis.strengths, <CheckCircleIcon color="success" />)}
                  {renderAnalysisSection('Areas for Improvement', analysis.areas_for_improvement, <WarningIcon color="warning" />)}
                  {renderAnalysisSection('Recommendations', analysis.recommendations, <InfoIcon color="info" />)}
                </Box>
              </Fade>
            )}
          </Paper>
        </Fade>
      </Container>
    </Box>
  );
};

export default AnalyzeResumeStructure;