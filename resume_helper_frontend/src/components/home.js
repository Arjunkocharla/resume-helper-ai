import React from 'react';
import { useNavigate } from 'react-router-dom';
import { auth } from '../firebase';
import { signOut } from 'firebase/auth';
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  IconButton,
  Box,
  Avatar,
} from '@mui/material';
import {
  AssessmentOutlined as AssessmentIcon,
  SearchOutlined as SearchIcon,
  DescriptionOutlined as DescriptionIcon,
  ExitToAppOutlined as LogoutIcon,
} from '@mui/icons-material';

function Home() {
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await signOut(auth);
      navigate('/login');
    } catch (error) {
      console.error('Error signing out:', error);
    }
  };

  const analysisOptions = [
    { 
      title: 'Analyze Resume Structure', 
      icon: <AssessmentIcon fontSize="large" />, 
      path: '/analyze-resume-structure', 
      description: 'Get a comprehensive analysis of your resume\'s structure and content' 
    },
    { 
      title: 'Analyze Keywords', 
      icon: <SearchIcon fontSize="large" />, 
      path: '/analyze-keywords', 
      description: 'Identify key terms to improve your resume\'s relevance' 
    },
    { 
      title: 'Suggest Keywords', 
      icon: <DescriptionIcon fontSize="large" />, 
      path: '/suggest-keywords', 
      description: 'Get tailored keyword suggestions for your target job' 
    },
  ];

  return (
    <Box sx={{
      minHeight: '100vh',
      background: 'linear-gradient(120deg, #3b82f6 0%, #8b5cf6 100%)',
      display: 'flex',
      flexDirection: 'column',
    }}>
      <AppBar position="static" sx={{ background: 'transparent', boxShadow: 'none' }}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, color: 'white' }}>
            Resume Helper AI
          </Typography>
          <IconButton color="inherit" onClick={handleLogout}>
            <LogoutIcon />
          </IconButton>
        </Toolbar>
      </AppBar>
      <Container maxWidth="lg" sx={{ mt: 8, mb: 4, flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
        <Typography variant="h3" gutterBottom sx={{ color: 'white', fontWeight: 'bold', textAlign: 'center', mb: 4 }}>
          Welcome to Resume Helper AI
        </Typography>
        <Typography variant="h5" gutterBottom sx={{ color: 'white', textAlign: 'center', mb: 6 }}>
          What would you like to do today?
        </Typography>
        <Grid container spacing={3} sx={{ mt: 2 }}>
          {analysisOptions.map((option, index) => (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <Card 
                sx={{ 
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  background: 'linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%)',
                  transition: '0.3s',
                  '&:hover': {
                    transform: 'scale(1.05)',
                  },
                }}
              >
                <CardContent sx={{ flexGrow: 1, textAlign: 'center' }}>
                  <Avatar sx={{ bgcolor: 'white', color: '#FE6B8B', width: 60, height: 60, margin: '0 auto 16px' }}>
                    {option.icon}
                  </Avatar>
                  <Typography gutterBottom variant="h5" component="h2" sx={{ color: 'white', fontWeight: 'bold' }}>
                    {option.title}
                  </Typography>
                  <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.8)' }}>
                    {option.description}
                  </Typography>
                </CardContent>
                <CardActions sx={{ justifyContent: 'center', pb: 2 }}>
                  <Button
                    variant="contained"
                    onClick={() => navigate(option.path)}
                    sx={{
                      bgcolor: 'white',
                      color: '#FE6B8B',
                      '&:hover': {
                        bgcolor: 'rgba(255,255,255,0.9)',
                      },
                    }}
                  >
                    Get Started
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>
    </Box>
  );
}

export default Home;