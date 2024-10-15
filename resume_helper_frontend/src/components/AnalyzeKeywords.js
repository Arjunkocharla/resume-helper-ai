import React, { useState, useRef } from 'react';
import {
  Container, Typography, Button, TextField, Paper, Box, CircularProgress,
  Alert, Fade, Card, CardContent, Chip, Tooltip, IconButton, useTheme,
  Stepper, Step, StepLabel, StepContent, List, ListItem, ListItemIcon, ListItemText
} from '@mui/material';
import { 
  CloudUpload as CloudUploadIcon,
  CheckCircleOutline,
  ContentCopy,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
  Add
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';

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

  const handleSubmit = async () => {
    setError('');
    setAnalysis(null);
    setLoading(true);

    if (!file || !jobCategory) {
      setError('Please complete both steps before submitting.');
      setLoading(false);
      return;
    }

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
      setAnalysis(data.analysis);
      setActiveStep(3);
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
            startIcon={<CloudUploadIcon />}
            onClick={() => fileInputRef.current.click()}
            fullWidth
            sx={{ color: 'white', borderColor: 'white' }}
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
            fullWidth
            label="Job Category"
            variant="outlined"
            value={jobCategory}
            onChange={handleJobCategoryChange}
            sx={{ 
              mt: 2,
              '& .MuiOutlinedInput-root': {
                '& fieldset': { borderColor: 'rgba(255, 255, 255, 0.3)' },
                '&:hover fieldset': { borderColor: 'rgba(255, 255, 255, 0.5)' },
                '&.Mui-focused fieldset': { borderColor: theme.palette.primary.main },
              },
              '& .MuiInputLabel-root': { color: 'rgba(255, 255, 255, 0.7)' },
              '& .MuiInputBase-input': { color: 'white' },
            }}
          />
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

  return (
    <Box sx={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      background: 'linear-gradient(135deg, #0F172A 0%, #1E293B 100%)',
      py: 4,
    }}>
      <Container maxWidth="md">
        <Fade in={true}>
          <Paper elevation={3} sx={{ 
            p: 4, 
            borderRadius: '24px',
            background: 'rgba(255, 255, 255, 0.05)',
            backdropFilter: 'blur(10px)',
            border: '1px solid rgba(255, 255, 255, 0.1)',
          }}>
            <Typography variant="h4" component="h1" gutterBottom align="center" sx={{ mb: 4, color: 'white' }}>
              Analyze Resume Keywords
            </Typography>
            <Stepper activeStep={activeStep} orientation="vertical">
              {steps.map((step, index) => (
                <Step key={step.label}>
                  <StepLabel>
                    <Typography sx={{ color: 'white' }}>{step.label}</Typography>
                  </StepLabel>
                  <StepContent>
                    {step.content}
                  </StepContent>
                </Step>
              ))}
            </Stepper>
            {error && (
              <Alert severity="error" sx={{ mt: 2 }}>
                {error}
              </Alert>
            )}
            <AnimatePresence>
              {analysis && analysis.keywords && analysis.keywords.length > 0 && (
                <>
                  <Typography variant="h6" gutterBottom sx={{ color: 'white' }}>
                    Relevant Keywords and Suggestions for {analysis.job_category}:
                  </Typography>
                  <Box sx={{ maxHeight: '60vh', overflowY: 'auto', pr: 2 }}>
                    {analysis.keywords.map((keyword, index) => (
                      <Card sx={{ mb: 2, bgcolor: 'rgba(255, 255, 255, 0.1)' }} key={index}>
                        <CardContent>
                          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', cursor: 'pointer' }} onClick={() => setExpandedKeyword(expandedKeyword === index ? null : index)}>
                            <Typography variant="h6" sx={{ color: 'white' }}>
                              {keyword.keyword}
                            </Typography>
                            {expandedKeyword === index ? <ExpandLessIcon sx={{ color: 'white' }} /> : <ExpandMoreIcon sx={{ color: 'white' }} />}
                          </Box>
                          {expandedKeyword === index && (
                            <Box sx={{ mt: 2 }}>
                              <Typography variant="body2" paragraph sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
                                {keyword.importance}
                              </Typography>
                              <Typography variant="subtitle1" sx={{ color: 'white', mt: 2, mb: 1 }}>
                                Suggested Bullet Points:
                              </Typography>
                              <List>
                                {keyword.bullet_points.map((point, bulletIndex) => (
                                  <ListItem key={bulletIndex} 
                                    secondaryAction={
                                      <Tooltip title="Copy to clipboard">
                                        <IconButton edge="end" aria-label="copy" onClick={() => copyToClipboard(point.point)} sx={{ color: 'white' }}>
                                          <ContentCopy />
                                        </IconButton>
                                      </Tooltip>
                                    }>
                                    <ListItemIcon>
                                      <Add sx={{ color: theme.palette.primary.main }} />
                                    </ListItemIcon>
                                    <ListItemText 
                                      primary={point.point} 
                                      secondary={point.explanation}
                                      primaryTypographyProps={{ color: 'white' }}
                                      secondaryTypographyProps={{ color: 'rgba(255, 255, 255, 0.7)' }}
                                    />
                                  </ListItem>
                                ))}
                              </List>
                            </Box>
                          )}
                        </CardContent>
                      </Card>
                    ))}
                  </Box>
                </>
              )}
            </AnimatePresence>
          </Paper>
        </Fade>
      </Container>
    </Box>
  );
}

export default AnalyzeKeywords;
