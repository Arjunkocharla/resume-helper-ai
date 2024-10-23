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
      description: "Get a comprehensive analysis of your resume's structure and content",
      color: '#10B981',
      primary: true,
    },
    {
      title: 'Keyword Analysis',
      icon: <KeywordIcon fontSize="large" />,
      path: '/analyze-keywords',
      description: "Identify key terms to improve your resume's relevance",
      color: '#F59E0B',
    },
  ];

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: 'linear-gradient(to right, #F8FAFC 0%, #E2E8F0 30%, #CBD5E1 70%, #94A3B8 100%)',
        // Alternative options if you'd like to try:
        // background: 'linear-gradient(to right, #F8FAFC 0%, #E2E8F0 40%, #BAC7DA 75%, #94A3B8 100%)',
        // background: 'linear-gradient(to right, #FFFFFF 0%, #EEF2FF 35%, #C7D2FE 70%, #A5B4FC 100%)',
        display: 'flex',
        flexDirection: 'column',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      <AppBar
        position="static"
        elevation={0}
        sx={{
          background: 'transparent',
          backdropFilter: 'blur(10px)',
          borderBottom: '1px solid rgba(255, 255, 255, 0.1)'
        }}
      >
        <Toolbar>
          <Typography
            variant="h6"
            sx={{
              flexGrow: 1,
              background: 'linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              fontWeight: '700',
              letterSpacing: '-0.5px'
            }}
          >
            Resume Helper AI
          </Typography>
          <IconButton
            onClick={handleProfileClick}
            sx={{
              color: '#1E3A8A',
              background: 'rgba(255, 255, 255, 0.1)',
              backdropFilter: 'blur(10px)',
              mr: 1,
              '&:hover': { background: 'rgba(255, 255, 255, 0.2)' }
            }}
          >
            <ProfileIcon />
          </IconButton>
          <IconButton
            onClick={handleLogout}
            sx={{
              color: '#1E3A8A',
              background: 'rgba(255, 255, 255, 0.1)',
              backdropFilter: 'blur(10px)',
              '&:hover': { background: 'rgba(255, 255, 255, 0.2)' }
            }}
          >
            <LogoutIcon />
          </IconButton>
        </Toolbar>
      </AppBar>

      <Container
        maxWidth="lg"
        sx={{
          mt: 8,
          mb: 4,
          flexGrow: 1,
          display: 'flex',
          flexDirection: 'column',
          position: 'relative',
          zIndex: 1,
        }}
      >
        <Box sx={{ textAlign: 'center', mb: 8 }}>
          <Typography
            variant="h2"
            gutterBottom
            sx={{
              background: 'linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%)', // Updated to match SuggestKeywords
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              fontWeight: '700',
              letterSpacing: '-1px',
              mb: 2,
              fontSize: { xs: '2.5rem', md: '3.5rem' },
            }}
          >
            Elevate Your Resume
          </Typography>
          <Typography
            variant="h5"
            sx={{
              color: '#64748B', // Changed to solid color like SuggestKeywords
              fontWeight: '400',
              fontSize: { xs: '1.1rem', md: '1.25rem' },
              lineHeight: 1.6,
            }}
          >
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
                  background: option.primary
                    ? `linear-gradient(135deg, ${option.color}15, ${option.color}25)`
                    : 'rgba(255, 255, 255, 0.7)',
                  backdropFilter: 'blur(10px)',
                  border: `1px solid ${
                    option.primary ? `${option.color}22` : 'rgba(0, 0, 0, 0.1)'
                  }`,
                  transition: 'all 0.3s ease',
                  cursor: 'pointer',
                  overflow: 'hidden',
                  position: 'relative',
                  transform: hoveredCard === index ? 'scale(1.05)' : 'scale(1)',
                  zIndex: hoveredCard === index ? 2 : 1,
                  boxShadow:
                    hoveredCard === index
                      ? `0 20px 40px ${option.color}15`
                      : '0 4px 6px rgba(0, 0, 0, 0.1)',
                  filter: hoveredCard !== null && hoveredCard !== index ? 'blur(2px)' : 'none',
                  opacity: hoveredCard !== null && hoveredCard !== index ? 0.6 : 1,
                  '&:hover': {
                    boxShadow: `0 20px 40px ${option.color}20`,
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
                    background: `radial-gradient(circle, ${option.color}10 0%, transparent 70%)`,
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
                <Typography
                  variant="h5"
                  component="h2"
                  sx={{
                    color: '#1E293B', // Changed to solid color for consistency
                    fontWeight: 'bold',
                    mb: 2,
                    textAlign: 'center',
                    zIndex: 1,
                  }}
                >
                  {option.title}
                </Typography>
                <Typography
                  variant="body1"
                  sx={{
                    color: '#64748B', // Changed to solid color for consistency
                    mb: 3,
                    textAlign: 'center',
                    zIndex: 1,
                  }}
                >
                  {option.description}
                </Typography>
                <Button
                  variant={option.primary ? 'contained' : 'outlined'}
                  size="large"
                  sx={{
                    bgcolor: option.primary ? option.color : 'transparent',
                    color: option.primary ? 'white' : option.color,
                    borderColor: option.color,
                    '&:hover': {
                      bgcolor: option.primary ? option.color : `${option.color}15`,
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
