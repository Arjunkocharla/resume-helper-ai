import React, { useState } from 'react';
import {
  Container,
  Typography,
  Button,
  TextField,
  Paper,
  Box,
  CircularProgress,
  Alert,
  Fade,
  Card,
  CardContent,
  Chip,
  Tooltip,
  IconButton,
  Grid,
  Divider,
} from '@mui/material';
import { 
  CloudUpload as CloudUploadIcon,
  CheckCircleOutline,
  ContentCopy,
  Info as InfoIcon,
} from '@mui/icons-material';

function SuggestKeywords() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [suggestions, setSuggestions] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleJobDescriptionChange = (e) => {
    setJobDescription(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuggestions(null);
    setLoading(true);

    if (!file || !jobDescription) {
      setError('Please select a resume file and enter a job description.');
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
    } catch (err) {
      setError(err.message || 'An error occurred.');
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <Box sx={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      background: 'linear-gradient(120deg, #8b5cf6 0%, #3b82f6 100%)',
      py: 4,
    }}>
      <Container maxWidth="lg">
        <Fade in={true}>
          <Paper elevation={3} sx={{ p: 4, borderRadius: '16px' }}>
            <Typography variant="h4" component="h1" gutterBottom align="center" sx={{ mb: 4 }}>
              Optimize Your Resume with AI-Powered Keyword Suggestions
            </Typography>
            <Grid container spacing={4}>
              <Grid item xs={12} md={6}>
                <form onSubmit={handleSubmit}>
                  <Box sx={{ mb: 3 }}>
                    <input
                      accept=".pdf,.docx"
                      style={{ display: 'none' }}
                      id="raised-button-file"
                      type="file"
                      onChange={handleFileChange}
                    />
                    <label htmlFor="raised-button-file">
                      <Button
                        variant="outlined"
                        component="span"
                        startIcon={<CloudUploadIcon />}
                        fullWidth
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
                  <TextField
                    fullWidth
                    label="Job Description"
                    variant="outlined"
                    value={jobDescription}
                    onChange={handleJobDescriptionChange}
                    multiline
                    rows={6}
                    sx={{ mb: 3 }}
                  />
                  <Button
                    type="submit"
                    variant="contained"
                    disabled={loading}
                    fullWidth
                    sx={{
                      bgcolor: '#8b5cf6',
                      color: 'white',
                      '&:hover': {
                        bgcolor: '#7c3aed',
                      },
                    }}
                  >
                    {loading ? <CircularProgress size={24} /> : 'Get Suggestions'}
                  </Button>
                </form>
                {error && (
                  <Alert severity="error" sx={{ mt: 2 }}>
                    {error}
                  </Alert>
                )}
              </Grid>
              <Grid item xs={12} md={6}>
                {suggestions ? (
                  <Fade in={true} timeout={1000}>
                    <Box>
                      <Typography variant="h5" gutterBottom sx={{ color: '#8b5cf6' }}>
                        Suggested Keywords:
                      </Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 3 }}>
                        {suggestions.map((suggestion, index) => (
                          <Chip 
                            key={index} 
                            label={suggestion.keyword} 
                            color="primary" 
                            sx={{ bgcolor: '#8b5cf6' }} 
                          />
                        ))}
                      </Box>
                      <Box sx={{ maxHeight: '60vh', overflowY: 'auto', pr: 2 }}>
                        {suggestions.map((suggestion, index) => (
                          <Card key={index} sx={{ mb: 2, bgcolor: '#f3f4f6' }}>
                            <CardContent>
                              <Typography variant="h6" gutterBottom>
                                {suggestion.keyword}
                              </Typography>
                              <Typography variant="body2" paragraph>
                                {suggestion.explanation}
                              </Typography>
                              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                                <Typography variant="body1" sx={{ fontStyle: 'italic' }}>
                                  {suggestion.suggestion}
                                </Typography>
                                <Tooltip title="Copy to clipboard">
                                  <IconButton onClick={() => copyToClipboard(suggestion.suggestion)}>
                                    <ContentCopy />
                                  </IconButton>
                                </Tooltip>
                              </Box>
                            </CardContent>
                          </Card>
                        ))}
                      </Box>
                    </Box>
                  </Fade>
                ) : (
                  <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
                    <InfoIcon sx={{ fontSize: 60, color: '#8b5cf6', mb: 2 }} />
                    <Typography variant="h6" align="center" sx={{ color: '#4b5563' }}>
                      Upload your resume and paste the job description to get AI-powered keyword suggestions
                    </Typography>
                  </Box>
                )}
              </Grid>
            </Grid>
          </Paper>
        </Fade>
      </Container>
    </Box>
  );
}

export default SuggestKeywords;