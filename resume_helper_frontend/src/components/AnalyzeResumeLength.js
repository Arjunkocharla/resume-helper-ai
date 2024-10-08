import React, { useState } from 'react';
import {
  Container,
  Typography,
  Button,
  Paper,
  Box,
  CircularProgress,
  Alert,
} from '@mui/material';
import { CloudUpload as CloudUploadIcon } from '@mui/icons-material';

function AnalyzeResumeLength() {
  const [file, setFile] = useState(null);
  const [analysis, setAnalysis] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setAnalysis('');
    setLoading(true);

    if (!file) {
      setError('Please select a resume file.');
      setLoading(false);
      return;
    }

    const formData = new FormData();
    formData.append('resume', file);

    try {
      const response = await fetch('http://127.0.0.1:5000/analyze_resume_length', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        console.log('API Response:', result);
        setAnalysis(result.analysis);
      } else {
        const errorData = await response.json();
        throw new Error(errorData.error || 'An error occurred.');
      }
    } catch (err) {
      console.error('API Error:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md">
      <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
        <Typography variant="h4" gutterBottom>
          Analyze Resume Length
        </Typography>
        <form onSubmit={handleSubmit}>
          <Box sx={{ mb: 2 }}>
            <Button
              variant="contained"
              component="label"
              startIcon={<CloudUploadIcon />}
            >
              Upload Resume
              <input
                type="file"
                hidden
                accept=".pdf,.docx"
                onChange={handleFileChange}
              />
            </Button>
            {file && <Typography variant="body2">{file.name}</Typography>}
          </Box>
          <Button
            type="submit"
            variant="contained"
            color="primary"
            disabled={loading}
          >
            {loading ? <CircularProgress size={24} /> : 'Analyze'}
          </Button>
        </form>
        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}
        {analysis && (
          <Box sx={{ mt: 4 }}>
            <Typography variant="h5" gutterBottom>
              Analysis Result
            </Typography>
            <Typography>{analysis}</Typography>
          </Box>
        )}
      </Paper>
    </Container>
  );
}

export default AnalyzeResumeLength;
