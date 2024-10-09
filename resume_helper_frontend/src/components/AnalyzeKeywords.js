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
  Chip,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  IconButton,
  Tooltip,
} from '@mui/material';
import { CloudUpload as CloudUploadIcon, CheckCircleOutline, Add, ContentCopy } from '@mui/icons-material';

function AnalyzeKeywords() {
  const [file, setFile] = useState(null);
  const [jobCategory, setJobCategory] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleJobCategoryChange = (e) => {
    setJobCategory(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setAnalysis(null);
    setLoading(true);

    if (!file || !jobCategory) {
      setError('Please select a resume file and enter a job category.');
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
      setAnalysis(data);
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
              Analyze Resume Keywords
            </Typography>
            <form onSubmit={handleSubmit}>
              <Box sx={{ mb: 2 }}>
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
                label="Job Category"
                variant="outlined"
                value={jobCategory}
                onChange={handleJobCategoryChange}
                sx={{ mb: 2 }}
              />
              <Button
                type="submit"
                variant="contained"
                disabled={loading}
                sx={{
                  bgcolor: '#8b5cf6',
                  color: 'white',
                  '&:hover': {
                    bgcolor: '#7c3aed',
                  },
                }}
              >
                {loading ? <CircularProgress size={24} /> : 'Analyze'}
              </Button>
            </form>
            {error && (
              <Alert severity="error" sx={{ mt: 2 }}>
                {error}
              </Alert>
            )}
            {analysis && analysis.analysis && (
              <Fade in={true} timeout={1000}>
                <Box sx={{ mt: 4 }}>
                  <Typography variant="h5" gutterBottom sx={{ color: '#8b5cf6' }}>
                    Analysis Result for {analysis.job_category}
                  </Typography>
                  {analysis.analysis.keywords && analysis.analysis.keywords.length > 0 && (
                    <>
                      <Typography variant="h6" gutterBottom>
                        Relevant Keywords:
                      </Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
                        {analysis.analysis.keywords.map((keyword, index) => (
                          <Chip key={index} label={keyword} color="primary" sx={{ bgcolor: '#8b5cf6' }} />
                        ))}
                      </Box>
                    </>
                  )}
                  {analysis.analysis.bullet_points && analysis.analysis.bullet_points.length > 0 && (
                    <>
                      <Typography variant="h6" gutterBottom>
                        Suggested Bullet Points to Add:
                      </Typography>
                      <List>
                        {analysis.analysis.bullet_points.map((point, index) => (
                          <ListItem key={index} 
                            secondaryAction={
                              <Tooltip title="Copy to clipboard">
                                <IconButton edge="end" aria-label="copy" onClick={() => copyToClipboard(point)}>
                                  <ContentCopy />
                                </IconButton>
                              </Tooltip>
                            }>
                            <ListItemIcon>
                              <Add sx={{ color: '#8b5cf6' }} />
                            </ListItemIcon>
                            <ListItemText primary={point} />
                          </ListItem>
                        ))}
                      </List>
                    </>
                  )}
                </Box>
              </Fade>
            )}
          </Paper>
        </Fade>
      </Container>
    </Box>
  );
}

export default AnalyzeKeywords;