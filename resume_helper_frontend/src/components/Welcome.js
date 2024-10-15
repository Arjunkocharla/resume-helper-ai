import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  TextField,
  Button,
  Paper,
  Autocomplete,
  InputAdornment,
} from '@mui/material';
import { motion } from 'framer-motion';
import { CloudUpload as CloudUploadIcon } from '@mui/icons-material';

const Welcome = () => {
  const [formData, setFormData] = useState({
    name: '',
    desiredIndustry: '',
    totalExperience: '',
  });
  const [file, setFile] = useState(null);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevData => ({
      ...prevData,
      [name]: value
    }));
  };

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    // TODO: Implement API call to save user profile and upload resume
    console.log({ ...formData, file });
    navigate('/home');
  };

  const industries = [
    'Software Development',
    'Data Science',
    'Marketing',
    'Finance',
    'Healthcare',
    'Education',
    'Sales',
    'Human Resources',
    'Design',
    'Other'
  ];

  return (
    <Box sx={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      background: 'linear-gradient(135deg, #0F172A 0%, #1E293B 100%)',
      py: 4,
    }}>
      <Container maxWidth="sm">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <Paper elevation={3} sx={{ 
            p: 4, 
            borderRadius: '24px',
            background: 'rgba(255, 255, 255, 0.05)',
            backdropFilter: 'blur(10px)',
            border: '1px solid rgba(255, 255, 255, 0.1)',
          }}>
            <Typography variant="h4" component="h1" gutterBottom align="center" sx={{ mb: 4, color: 'white' }}>
              Welcome to Resume Helper!
            </Typography>
            <Typography variant="body1" sx={{ mb: 4, color: 'rgba(255,255,255,0.7)', textAlign: 'center' }}>
              Let's get your resume optimized for your dream job. Ready to start?
            </Typography>
            <form onSubmit={handleSubmit}>
              <TextField
                fullWidth
                label="What's your name?"
                name="name"
                value={formData.name}
                onChange={handleChange}
                variant="outlined"
                required
                sx={{ ...textFieldStyle, mb: 3 }}
              />
              <Autocomplete
                options={industries}
                renderInput={(params) => (
                  <TextField
                    {...params}
                    label="Desired industry"
                    required
                    sx={textFieldStyle}
                  />
                )}
                value={formData.desiredIndustry}
                onChange={(event, newValue) => {
                  setFormData(prevData => ({ ...prevData, desiredIndustry: newValue }));
                }}
                sx={{ mb: 3 }}
              />
              <TextField
                fullWidth
                label="Total years of experience"
                name="totalExperience"
                type="number"
                value={formData.totalExperience}
                onChange={handleChange}
                variant="outlined"
                required
                InputProps={{
                  endAdornment: <InputAdornment position="end">years</InputAdornment>,
                }}
                sx={{ ...textFieldStyle, mb: 3 }}
              />
              <Box sx={{ mt: 3, mb: 3 }}>
                <input
                  accept=".pdf,.doc,.docx"
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
                    sx={{
                      color: 'white',
                      borderColor: 'rgba(255, 255, 255, 0.3)',
                      '&:hover': { borderColor: 'white' }
                    }}
                  >
                    {file ? file.name : 'Upload your current resume'}
                  </Button>
                </label>
              </Box>
              <Button
                type="submit"
                variant="contained"
                fullWidth
                sx={buttonStyle}
              >
                Optimize My Resume!
              </Button>
            </form>
          </Paper>
        </motion.div>
      </Container>
    </Box>
  );
};

const textFieldStyle = {
  '& .MuiOutlinedInput-root': {
    '& fieldset': { borderColor: 'rgba(255, 255, 255, 0.3)' },
    '&:hover fieldset': { borderColor: 'rgba(255, 255, 255, 0.5)' },
    '&.Mui-focused fieldset': { borderColor: 'primary.main' },
  },
  '& .MuiInputLabel-root': { color: 'rgba(255, 255, 255, 0.7)' },
  '& .MuiInputBase-input': { color: 'white' },
};

const buttonStyle = {
  bgcolor: 'primary.main',
  color: 'white',
  '&:hover': { bgcolor: 'primary.dark' },
  py: 1.5,
  fontSize: '1.1rem',
};

export default Welcome;
