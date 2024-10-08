import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { createUserWithEmailAndPassword, signInWithPopup, GoogleAuthProvider } from 'firebase/auth';
import { auth } from '../firebase';
import { FaGoogle, FaEnvelope, FaLock, FaEye, FaEyeSlash, FaUser } from 'react-icons/fa';
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

function SignUpPage() {
  const [showPassword, setShowPassword] = useState(false);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isSigningUp, setIsSigningUp] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsSigningUp(true);
    try {
      await createUserWithEmailAndPassword(auth, email, password);
      // You might want to update the user's profile with their name here
      navigate('/home');
    } catch (error) {
      setError(error.message);
    } finally {
      setIsSigningUp(false);
    }
  };

  const handleGoogleAuth = async () => {
    setIsSigningUp(true);
    try {
      const provider = new GoogleAuthProvider();
      provider.setCustomParameters({
        prompt: 'select_account'
      });
      const result = await signInWithPopup(auth, provider);
      
      // The logic here remains the same, but we're not explicitly calling it "sign up"
      if (result.user.metadata.creationTime === result.user.metadata.lastSignInTime) {
        console.log('New user authenticated with Google');
        navigate('/home');
      } else {
        console.log('Existing user authenticated with Google');
        navigate('/home');
      }
    } catch (error) {
      if (error.code !== 'auth/popup-closed-by-user') {
        setError('Failed to authenticate with Google. Please try again.');
        console.error('Google authentication error:', error);
      }
    } finally {
      setIsSigningUp(false);
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
            Join Resume Helper AI
          </Typography>
          <Typography variant="body1" gutterBottom align="center">
            Create your account to get started
          </Typography>
          {error && (
            <Typography color="error" align="center" gutterBottom>
              {error}
            </Typography>
          )}
          <form onSubmit={handleSubmit}>
            <TextField
              fullWidth
              label="Full Name"
              variant="outlined"
              margin="normal"
              value={name}
              onChange={(e) => setName(e.target.value)}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <FaUser />
                  </InputAdornment>
                ),
              }}
            />
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
              disabled={isSigningUp}
              sx={{ mt: 2, mb: 2 }}
            >
              {isSigningUp ? 'Signing Up...' : 'Sign Up'}
            </Button>
          </form>
          <Divider sx={{ my: 2 }}>OR</Divider>
          <Button
            fullWidth
            variant="outlined"
            color="primary"
            onClick={handleGoogleAuth}
            disabled={isSigningUp}
            startIcon={<FaGoogle />}
          >
            {isSigningUp ? 'Authenticating...' : 'Continue with Google'}
          </Button>
          <Typography variant="body2" align="center" sx={{ mt: 2 }}>
            Already have an account?{' '}
            <Link to="/login" style={{ color: '#3b82f6' }}>
              Log in
            </Link>
          </Typography>
        </Paper>
      </Container>
    </Box>
  );
}

export default SignUpPage;