import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { signInWithEmailAndPassword, signInWithPopup, GoogleAuthProvider } from 'firebase/auth';
import { auth } from '../firebase';
import { FaGoogle, FaEnvelope, FaLock, FaEye, FaEyeSlash } from 'react-icons/fa';
import {
  Box,
  Container,
  Typography,
  TextField,
  Button,
  IconButton,
  InputAdornment,
  Paper,
  Divider,
  Fade,
  useTheme,
  Grid,
} from '@mui/material';
import { motion } from 'framer-motion';

function LoginPage() {
  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const navigate = useNavigate();
  const theme = useTheme();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoggingIn(true);
    try {
      await signInWithEmailAndPassword(auth, email, password);
      navigate('/home');
    } catch (error) {
      setError(error.message);
    } finally {
      setIsLoggingIn(false);
    }
  };

  const handleGoogleLogin = async () => {
    setIsLoggingIn(true);
    try {
      const provider = new GoogleAuthProvider();
      provider.setCustomParameters({
        prompt: 'select_account'
      });
      const result = await signInWithPopup(auth, provider);
      
      if (result.user.metadata.creationTime === result.user.metadata.lastSignInTime) {
        console.log('New user signed up with Google');
        setError('New account created. Redirecting to home...');
      } else {
        console.log('Existing user logged in with Google');
      }
      setTimeout(() => navigate('/home'), 2000);
    } catch (error) {
      if (error.code !== 'auth/popup-closed-by-user') {
        setError('Failed to log in with Google. Please try again.');
        console.error('Google login error:', error);
      }
    } finally {
      setIsLoggingIn(false);
    }
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: 'linear-gradient(145deg, #f6f8fc 0%, #eef2ff 100%)',
        position: 'relative',
        overflow: 'hidden'
      }}
    >
      {/* Background Elements */}
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

      <Container maxWidth="lg" sx={{ pt: 8, position: 'relative', zIndex: 1 }}>
        <Grid container spacing={4} alignItems="center">
          {/* Left side - Product Info */}
          <Grid item xs={12} md={6}>
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
            >
              <Typography 
                variant="h3" 
                sx={{ 
                  fontWeight: 700, 
                  color: '#1E293B',
                  mb: 3,
                  background: 'linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                }}>
                Resume Helper AI
              </Typography>
              <Typography variant="h5" sx={{ color: '#475569', mb: 4 }}>
                Your AI-powered resume optimization companion
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mb: 4 }}>
                {[
                  'Smart keyword optimization for ATS systems',
                  'Personalized resume improvement suggestions',
                  'Real-time analysis and feedback',
                  'Industry-specific recommendations'
                ].map((feature, index) => (
                  <Box key={index} sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <Box sx={{
                      width: 24,
                      height: 24,
                      borderRadius: '50%',
                      bgcolor: 'rgba(59, 130, 246, 0.1)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center'
                    }}>
                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ delay: index * 0.1 }}
                      >
                        <Box sx={{
                          width: 8,
                          height: 8,
                          borderRadius: '50%',
                          bgcolor: '#3B82F6'
                        }} />
                      </motion.div>
                    </Box>
                    <Typography sx={{ color: '#64748B' }}>
                      {feature}
                    </Typography>
                  </Box>
                ))}
              </Box>
            </motion.div>
          </Grid>

          {/* Right side - Login Form */}
          <Grid item xs={12} md={6}>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              <Paper
                elevation={0}
                sx={{
                  p: 4,
                  borderRadius: '24px',
                  background: 'white',
                  border: '1px solid rgba(59, 130, 246, 0.1)',
                  boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                }}
              >
                <Typography variant="h4" component="h1" gutterBottom align="center" 
                  sx={{ 
                    color: '#1E293B', // Changed from white to dark color
                    fontWeight: 'bold',
                    mb: 3 
                  }}>
                  Welcome Back
                </Typography>
                <Typography variant="body1" gutterBottom align="center" 
                  sx={{ 
                    color: '#64748B', // Changed from white to gray
                    mb: 4 
                  }}>
                  Log in to your Resume Helper AI account
                </Typography>
                
                {error && (
                  <Typography color="error" align="center" sx={{ mb: 2 }}>
                    {error}
                  </Typography>
                )}
                
                <form onSubmit={handleSubmit}>
                  <TextField
                    fullWidth
                    label="Email"
                    variant="outlined"
                    margin="normal"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <FaEnvelope color="#3B82F6" />
                        </InputAdornment>
                      ),
                    }}
                    sx={{
                      '& .MuiOutlinedInput-root': {
                        '& fieldset': { borderColor: 'rgba(59, 130, 246, 0.2)' },
                        '&:hover fieldset': { borderColor: 'rgba(59, 130, 246, 0.4)' },
                        '&.Mui-focused fieldset': { borderColor: '#3B82F6' },
                      },
                      '& .MuiInputLabel-root': { color: '#64748B' },
                      '& .MuiInputBase-input': { color: '#1E293B' }, // Changed text color
                    }}
                  />
                  
                  <TextField
                    fullWidth
                    label="Password"
                    variant="outlined"
                    margin="normal"
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <FaLock color="#3B82F6" />
                        </InputAdornment>
                      ),
                      endAdornment: (
                        <InputAdornment position="end">
                          <IconButton
                            onClick={() => setShowPassword(!showPassword)}
                            edge="end"
                            sx={{ color: '#64748B' }}
                          >
                            {showPassword ? <FaEyeSlash /> : <FaEye />}
                          </IconButton>
                        </InputAdornment>
                      ),
                    }}
                    sx={{
                      '& .MuiOutlinedInput-root': {
                        '& fieldset': { borderColor: 'rgba(59, 130, 246, 0.2)' },
                        '&:hover fieldset': { borderColor: 'rgba(59, 130, 246, 0.4)' },
                        '&.Mui-focused fieldset': { borderColor: '#3B82F6' },
                      },
                      '& .MuiInputLabel-root': { color: '#64748B' },
                      '& .MuiInputBase-input': { color: '#1E293B' }, // Changed text color
                    }}
                  />

                  <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                    <Button
                      fullWidth
                      variant="contained"
                      type="submit"
                      disabled={isLoggingIn}
                      sx={{
                        mt: 3,
                        mb: 2,
                        py: 1.5,
                        background: 'linear-gradient(135deg, #3B82F6 0%, #2563EB 100%)',
                        borderRadius: '12px',
                        textTransform: 'none',
                        fontSize: '1rem',
                        fontWeight: 500,
                        '&:hover': {
                          background: 'linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%)',
                        },
                      }}
                    >
                      {isLoggingIn ? 'Logging In...' : 'Log In'}
                    </Button>
                  </motion.div>
                </form>

                <Divider sx={{ 
                  my: 3,
                  '&::before, &::after': {
                    borderColor: 'rgba(59, 130, 246, 0.2)',
                  }
                }}>
                  <Typography sx={{ color: '#64748B', px: 2 }}>or</Typography>
                </Divider>

                <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                  <Button
                    fullWidth
                    variant="outlined"
                    onClick={handleGoogleLogin}
                    disabled={isLoggingIn}
                    startIcon={<FaGoogle />}
                    sx={{
                      py: 1.5,
                      color: '#1E293B',
                      borderColor: 'rgba(59, 130, 246, 0.3)',
                      borderRadius: '12px',
                      textTransform: 'none',
                      fontSize: '1rem',
                      fontWeight: 500,
                      '&:hover': {
                        borderColor: '#3B82F6',
                        background: 'rgba(59, 130, 246, 0.05)',
                      },
                    }}
                  >
                    {isLoggingIn ? 'Logging in...' : 'Continue with Google'}
                  </Button>
                </motion.div>

                <Typography variant="body2" align="center" 
                  sx={{ 
                    mt: 3,
                    color: '#64748B'
                  }}>
                  Don't have an account?{' '}
                  <Link 
                    to="/signup" 
                    style={{ 
                      color: '#3B82F6',
                      textDecoration: 'none',
                      fontWeight: 500
                    }}>
                    Sign up
                  </Link>
                </Typography>
              </Paper>
            </motion.div>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}

export default LoginPage;
