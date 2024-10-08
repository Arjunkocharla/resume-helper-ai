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
} from '@mui/material';

function LoginPage() {
  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const navigate = useNavigate();

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
      // Add these lines to always prompt for account selection
      provider.setCustomParameters({
        prompt: 'select_account'
      });
      const result = await signInWithPopup(auth, provider);
      
      // Check if the user is new or existing
      if (result.user.metadata.creationTime === result.user.metadata.lastSignInTime) {
        // New user
        console.log('New user signed up with Google');
        setError('New account created. Redirecting to home...');
      } else {
        // Existing user
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
    <Box sx={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      background: 'linear-gradient(120deg, #3b82f6 0%, #8b5cf6 100%)',
    }}>
      <Container maxWidth="sm">
        <Paper elevation={3} sx={{ p: 4, borderRadius: '16px' }}>
          <Typography variant="h4" component="h1" gutterBottom align="center">
            Welcome Back
          </Typography>
          <Typography variant="body1" gutterBottom align="center">
            Log in to your Resume Helper AI account
          </Typography>
          {error && (
            <Typography color="error" align="center" gutterBottom>
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
                    <FaEnvelope />
                  </InputAdornment>
                ),
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
                    <FaLock />
                  </InputAdornment>
                ),
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      onClick={() => setShowPassword(!showPassword)}
                      edge="end"
                    >
                      {showPassword ? <FaEyeSlash /> : <FaEye />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />
            <Button
              fullWidth
              variant="contained"
              color="primary"
              type="submit"
              disabled={isLoggingIn}
              sx={{ mt: 2, mb: 2 }}
            >
              {isLoggingIn ? 'Logging In...' : 'Log In'}
            </Button>
          </form>
          <Divider sx={{ my: 2 }}>OR</Divider>
          <Button
            fullWidth
            variant="outlined"
            color="primary"
            onClick={handleGoogleLogin}
            disabled={isLoggingIn}
            startIcon={<FaGoogle />}
          >
            {isLoggingIn ? 'Logging in...' : 'Log in with Google'}
          </Button>
          <Typography variant="body2" align="center" sx={{ mt: 2 }}>
            Don't have an account?{' '}
            <Link to="/signup" style={{ color: '#3b82f6' }}>
              Sign up
            </Link>
          </Typography>
        </Paper>
      </Container>
    </Box>
  );
}

export default LoginPage;