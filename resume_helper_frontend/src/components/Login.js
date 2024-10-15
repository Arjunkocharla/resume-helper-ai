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
        display: 'flex',
        alignItems: 'center',
        background: 'linear-gradient(135deg, #0F172A 0%, #1E293B 100%)',
        py: 4,
      }}
    >
      <Container maxWidth="sm">
        <Fade in={true} timeout={1000}>
          <Paper
            elevation={3}
            sx={{
              p: 4,
              borderRadius: '24px',
              background: 'rgba(255, 255, 255, 0.05)',
              backdropFilter: 'blur(10px)',
              border: '1px solid rgba(255, 255, 255, 0.1)',
            }}
          >
            <motion.div
              initial={{ y: -20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ duration: 0.5 }}
            >
              <Typography variant="h4" component="h1" gutterBottom align="center" sx={{ color: 'white', fontWeight: 'bold' }}>
                Welcome Back
              </Typography>
              <Typography variant="body1" gutterBottom align="center" sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
                Log in to your Resume Helper AI account
              </Typography>
            </motion.div>
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
                      <FaEnvelope color={theme.palette.primary.main} />
                    </InputAdornment>
                  ),
                }}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    '& fieldset': { borderColor: 'rgba(255, 255, 255, 0.3)' },
                    '&:hover fieldset': { borderColor: 'rgba(255, 255, 255, 0.5)' },
                    '&.Mui-focused fieldset': { borderColor: theme.palette.primary.main },
                  },
                  '& .MuiInputLabel-root': { color: 'rgba(255, 255, 255, 0.7)' },
                  '& .MuiInputBase-input': { color: 'white' },
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
                      <FaLock color={theme.palette.primary.main} />
                    </InputAdornment>
                  ),
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton
                        onClick={() => setShowPassword(!showPassword)}
                        edge="end"
                        sx={{ color: 'rgba(255, 255, 255, 0.7)' }}
                      >
                        {showPassword ? <FaEyeSlash /> : <FaEye />}
                      </IconButton>
                    </InputAdornment>
                  ),
                }}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    '& fieldset': { borderColor: 'rgba(255, 255, 255, 0.3)' },
                    '&:hover fieldset': { borderColor: 'rgba(255, 255, 255, 0.5)' },
                    '&.Mui-focused fieldset': { borderColor: theme.palette.primary.main },
                  },
                  '& .MuiInputLabel-root': { color: 'rgba(255, 255, 255, 0.7)' },
                  '& .MuiInputBase-input': { color: 'white' },
                }}
              />
              <motion.div whileHover={{ scale: 1.03 }} whileTap={{ scale: 0.98 }}>
                <Button
                  fullWidth
                  variant="contained"
                  color="primary"
                  type="submit"
                  disabled={isLoggingIn}
                  sx={{
                    mt: 2,
                    mb: 2,
                    background: 'linear-gradient(45deg, #3b82f6 30%, #8b5cf6 90%)',
                    boxShadow: '0 3px 5px 2px rgba(59, 130, 246, .3)',
                  }}
                >
                  {isLoggingIn ? 'Logging In...' : 'Log In'}
                </Button>
              </motion.div>
            </form>
            <Divider sx={{ my: 2, bgcolor: 'rgba(255, 255, 255, 0.1)' }}>
              <Typography sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>OR</Typography>
            </Divider>
            <motion.div whileHover={{ scale: 1.03 }} whileTap={{ scale: 0.98 }}>
              <Button
                fullWidth
                variant="outlined"
                onClick={handleGoogleLogin}
                disabled={isLoggingIn}
                startIcon={<FaGoogle />}
                sx={{
                  color: 'white',
                  borderColor: 'rgba(255, 255, 255, 0.5)',
                  '&:hover': {
                    borderColor: 'white',
                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                  },
                }}
              >
                {isLoggingIn ? 'Logging in...' : 'Log in with Google'}
              </Button>
            </motion.div>
            <Typography variant="body2" align="center" sx={{ mt: 2, color: 'rgba(255, 255, 255, 0.7)' }}>
              Don't have an account?{' '}
              <Link to="/signup" style={{ color: theme.palette.primary.main }}>
                Sign up
              </Link>
            </Typography>
          </Paper>
        </Fade>
      </Container>
    </Box>
  );
}

export default LoginPage;