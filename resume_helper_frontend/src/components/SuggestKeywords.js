import React, { useState, useRef, useEffect } from 'react';
import {
  Container, Typography, Button, TextField, Paper, Box, CircularProgress,
  Alert, Fade, Card, CardContent, Chip, Tooltip, IconButton, useTheme,
  Stepper, Step, StepLabel, StepContent
} from '@mui/material';
import { 
  CloudUpload as CloudUploadIcon,
  CheckCircleOutline,
  ContentCopy,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';

function SuggestKeywords() {
  const [activeStep, setActiveStep] = useState(0);
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [suggestions, setSuggestions] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [expandedKeyword, setExpandedKeyword] = useState(null);
  const fileInputRef = useRef(null);
  const theme = useTheme();

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setActiveStep(1);
  };

  const handleJobDescriptionChange = (e) => {
    setJobDescription(e.target.value);
  };

  useEffect(() => {
    if (jobDescription.length > 0) {
      setActiveStep(2);
    }
  }, [jobDescription]);

  const handleSubmit = async () => {
    setError('');
    setSuggestions(null);
    setLoading(true);

    if (!file || !jobDescription) {
      setError('Please complete both steps before submitting.');
      setLoading(false);
      return;
    }

    const formData = new FormData();
    formData.append('resume', file);
    formData.append('job_description', jobDescription);

    try {
      const response = await fetch('http://127.0.0.1:5000/suggest_keywords', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setSuggestions(data.keyword_suggestions);
      setActiveStep(3);
    } catch (err) {
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
      label: 'Enter Job Description',
      content: (
        <TextField
          fullWidth
          label="Job Description"
          variant="outlined"
          value={jobDescription}
          onChange={handleJobDescriptionChange}
          multiline
          rows={6}
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
      ),
    },
    {
      label: 'Get Suggestions',
      content: (
        <Button
          onClick={handleSubmit}
          variant="contained"
          disabled={loading || !file || !jobDescription}
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
          {loading ? <CircularProgress size={24} /> : 'Get Suggestions'}
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
              AI-Powered Keyword Optimizer
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
              {suggestions && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ duration: 0.5 }}
                >
                  <Typography variant="h5" gutterBottom sx={{ color: theme.palette.primary.main, mt: 4 }}>
                    Suggested Keywords:
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 3 }}>
                    {suggestions.keywords.map((suggestion, index) => (
                      <Chip 
                        key={index} 
                        label={suggestion.keyword} 
                        color="primary"
                        onClick={() => setExpandedKeyword(expandedKeyword === index ? null : index)}
                        sx={{ bgcolor: theme.palette.primary.main }} 
                      />
                    ))}
                  </Box>
                  <Box sx={{ maxHeight: '60vh', overflowY: 'auto', pr: 2 }}>
                    {suggestions.keywords.map((suggestion, index) => (
                      <Card sx={{ mb: 2, bgcolor: 'rgba(255, 255, 255, 0.1)' }} key={index}>
                        <CardContent>
                          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', cursor: 'pointer' }} onClick={() => setExpandedKeyword(expandedKeyword === index ? null : index)}>
                            <Typography variant="h6" sx={{ color: 'white' }}>
                              {suggestion.keyword}
                            </Typography>
                            {expandedKeyword === index ? <ExpandLessIcon sx={{ color: 'white' }} /> : <ExpandMoreIcon sx={{ color: 'white' }} />}
                          </Box>
                          {expandedKeyword === index && (
                            <Box sx={{ mt: 2 }}>
                              <Typography variant="body2" paragraph sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
                                {suggestion.importance}
                              </Typography>
                              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                                <Typography variant="body1" sx={{ fontStyle: 'italic', color: 'white' }}>
                                  {suggestion.suggestion}
                                </Typography>
                                <Tooltip title="Copy to clipboard">
                                  <IconButton onClick={() => copyToClipboard(suggestion.suggestion)} sx={{ color: 'white' }}>
                                    <ContentCopy />
                                  </IconButton>
                                </Tooltip>
                              </Box>
                              <Typography variant="body2" sx={{ mt: 1, color: 'rgba(255, 255, 255, 0.7)' }}>
                                Suggested placement: {suggestion.placement}
                              </Typography>
                            </Box>
                          )}
                        </CardContent>
                      </Card>
                    ))}
                  </Box>
                  {suggestions.overall_strategy && (
                    <Box sx={{ mt: 3 }}>
                      <Typography variant="h6" gutterBottom sx={{ color: theme.palette.primary.main }}>
                        Overall Strategy:
                      </Typography>
                      <Typography variant="body1" sx={{ color: 'white' }}>
                        {suggestions.overall_strategy}
                      </Typography>
                    </Box>
                  )}
                </motion.div>
              )}
            </AnimatePresence>
          </Paper>
        </Fade>
      </Container>
    </Box>
  );
}

export default SuggestKeywords;