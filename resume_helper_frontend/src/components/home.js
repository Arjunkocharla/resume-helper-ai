import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { auth } from '../firebase';
import { signOut } from 'firebase/auth';
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Grid,
  Box,
  Button,
  IconButton,
  useMediaQuery,
  useTheme,
} from '@mui/material';
import {
  BarChart as AnalyzeIcon,
  Search as KeywordIcon,
  Lightbulb as SuggestIcon,
  ExitToApp as LogoutIcon,
  AccountCircle as ProfileIcon,
} from '@mui/icons-material';

function Home() {
  const navigate = useNavigate();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const [hoveredCard, setHoveredCard] = useState(null);

  const handleLogout = async () => {
    try {
      await signOut(auth);
      navigate('/login');
    } catch (error) {
      console.error('Error signing out:', error);
    }
  };

  const handleProfileClick = () => {
    navigate('/profile');
  };

  const analysisOptions = [
    { 
      title: 'Suggest Keywords', 
      icon: <SuggestIcon fontSize="large" />, 
      path: '/suggest-keywords', 
      description: 'Get tailored keyword suggestions for your target job',
      color: '#3B82F6',
    },
    { 
      title: 'Analyze Resume Structure', 
      icon: <AnalyzeIcon fontSize="large" />, 
      path: '/analyze-resume-structure', 
      description: 'Get a comprehensive analysis of your resume\'s structure and content',
      color: '#10B981',
      primary: true
    },
    { 
      title: 'Keyword Analysis', 
      icon: <KeywordIcon fontSize="large" />, 
      path: '/analyze-keywords', 
      description: 'Identify key terms to improve your resume\'s relevance',
      color: '#F59E0B',
    },
  ];

  const cubStyle = {
    position: 'absolute',
    width: '60px',
    height: '60px',
    borderRadius: '12px',
    background: 'rgba(0, 0, 0, 0.02)',
    backdropFilter: 'blur(5px)',
    border: '1px solid rgba(0, 0, 0, 0.05)',
    animation: 'float 6s ease-in-out infinite',
  };

  return (
    <Box sx={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #E0E0E0 0%, #C7D2FE 100%)', // Adjusted gradient for a slightly darker shade
      display: 'flex',
      flexDirection: 'column',
      position: 'relative',
      overflow: 'hidden',
    }}>
      {/* Floating Cubes */}
      <Box sx={{
        ...cubStyle,
        top: '10%',
        left: '5%',
        animationDelay: '0s',
        background: 'rgba(59, 130, 246, 0.05)',
      }} />
      <Box sx={{
        ...cubStyle,
        top: '70%',
        left: '10%',
        animationDelay: '1s',
        background: 'rgba(16, 185, 129, 0.05)',
      }} />
      <Box sx={{
        ...cubStyle,
        top: '20%',
        right: '5%',
        animationDelay: '2s',
        background: 'rgba(245, 158, 11, 0.05)',
      }} />
      <Box sx={{
        ...cubStyle,
        bottom: '15%',
        right: '10%',
        animationDelay: '3s',
        background: 'rgba(59, 130, 246, 0.05)',
      }} />

      <AppBar 
        position="static" 
        elevation={0}
        sx={{ 
          background: 'transparent', // Set background to transparent
          boxShadow: 'none',          // Remove any box shadow
          borderBottom: 'none',      // Remove bottom border
        }}
      >
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, color: '#1E3A8A', fontWeight: 'bold' }}>
            Resume Helper AI
          </Typography>
          <IconButton color="primary" sx={{ mr: 2 }} onClick={handleProfileClick}>
            <ProfileIcon />
          </IconButton>
          <IconButton color="primary" onClick={handleLogout}>
            <LogoutIcon />
          </IconButton>
        </Toolbar>
      </AppBar>
      
      <Container maxWidth="lg" sx={{ mt: 8, mb: 4, flexGrow: 1, display: 'flex', flexDirection: 'column', position: 'relative', zIndex: 1 }}>
        <Box sx={{ textAlign: 'center', mb: 8 }}>
          <Typography variant="h2" gutterBottom sx={{ color: '#1E3A8A', fontWeight: 'bold', mb: 2 }}>
            Elevate Your Resume
          </Typography>
          <Typography variant="h5" sx={{ color: '#4B5563' }}>
            Optimize your resume with AI-powered structure analysis and keyword suggestions
          </Typography>
        </Box>
        
        <Grid container spacing={4} justifyContent="center" alignItems="center">
          {analysisOptions.map((option, index) => (
            <Grid item xs={12} md={4} key={index}>
              <Box
                onMouseEnter={() => setHoveredCard(index)}
                onMouseLeave={() => setHoveredCard(null)}
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center',
                  padding: 4,
                  borderRadius: '24px',
                  background: option.primary ? `linear-gradient(135deg, ${option.color}22, ${option.color}44)` : 'rgba(255, 255, 255, 0.9)',
                  backdropFilter: 'blur(10px)',
                  border: `1px solid ${option.primary ? `${option.color}33` : 'rgba(0, 0, 0, 0.05)'}`,
                  transition: 'all 0.3s ease',
                  cursor: 'pointer',
                  overflow: 'hidden',
                  position: 'relative',
                  transform: hoveredCard === index ? 'scale(1.05)' : 'scale(1)',
                  zIndex: hoveredCard === index ? 2 : 1,
                  boxShadow: hoveredCard === index 
                    ? `0 10px 20px rgba(0, 0, 0, 0.1)` 
                    : '0 4px 6px rgba(0, 0, 0, 0.05)',
                  filter: hoveredCard !== null && hoveredCard !== index ? 'blur(2px)' : 'none',
                  opacity: hoveredCard !== null && hoveredCard !== index ? 0.8 : 1,
                  '&:hover': {
                    boxShadow: `0 10px 20px rgba(0, 0, 0, 0.1)`,
                    zIndex: 2,
                    '& .icon-bg': {
                      transform: 'scale(1.2)',
                    },
                  },
                }}
                onClick={() => navigate(option.path)}
              >
                <Box
                  className="icon-bg"
                  sx={{
                    position: 'absolute',
                    top: '-20%',
                    left: '-20%',
                    width: '140%',
                    height: '140%',
                    background: `radial-gradient(circle, ${option.color}22 0%, transparent 70%)`,
                    transition: 'all 0.3s ease',
                  }}
                />
                <Box
                  sx={{
                    bgcolor: option.color,
                    color: 'white',
                    borderRadius: '50%',
                    p: 2,
                    mb: 3,
                    zIndex: 1,
                  }}
                >
                  {option.icon}
                </Box>
                <Typography variant="h5" component="h2" sx={{ color: '#1E3A8A', fontWeight: 'bold', mb: 2, textAlign: 'center', zIndex: 1 }}>
                  {option.title}
                </Typography>
                <Typography variant="body1" sx={{ color: '#4B5563', mb: 3, textAlign: 'center', zIndex: 1 }}>
                  {option.description}
                </Typography>
                <Button
                  variant={option.primary ? "contained" : "outlined"}
                  size="large"
                  sx={{
                    bgcolor: option.primary ? option.color : 'transparent',
                    color: option.primary ? 'white' : option.color,
                    borderColor: option.color,
                    '&:hover': {
                      bgcolor: option.primary ? option.color : `${option.color}22`,
                      borderColor: option.color,
                    },
                    zIndex: 1,
                  }}
                >
                  Get Started
                </Button>
              </Box>
            </Grid>
          ))}
        </Grid>
      </Container>
      
      <style jsx global>{`
        @keyframes float {
          0% {
            transform: translateY(0px) rotate(0deg);
          }
          50% {
            transform: translateY(-20px) rotate(10deg);
          }
          100% {
            transform: translateY(0px) rotate(0deg);
          }
        }
      `}</style>
    </Box>
  );
}

export default Home;
