import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { onAuthStateChanged } from 'firebase/auth';
import { auth } from './firebase';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

// Import your components
import AnalyzeResumeLength from './components/AnalyzeResumeLength';
import AnalyzeKeywords from './components/AnalyzeKeywords';
import SuggestKeywords from './components/SuggestKeywords';
import AnalyzeResumeStructure from './components/AnalyzeResumeStructure';
import Login from './components/Login';
import SignUp from './components/Signup';
import Home from './components/home';
import Welcome from './components/Welcome';
import UserProfileComponent from './components/UserProfileComponent'; // Import the UserProfileComponent

// Create a theme instance
const theme = createTheme();

function App() {
  const [user, setUser] = useState(null);
  const [isNewUser, setIsNewUser] = useState(false);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      if (currentUser) {
        setUser(currentUser);
        // Check if the user is new (you might want to store this in your database)
        setIsNewUser(currentUser.metadata.creationTime === currentUser.metadata.lastSignInTime);
      } else {
        setUser(null);
        setIsNewUser(false);
      }
    });
    return unsubscribe;
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/welcome" element={
            user && isNewUser ? <Welcome /> : <Navigate to="/home" />
          } />
          <Route path="/home" element={<Home />} />
          <Route path="/analyze-length" element={<AnalyzeResumeLength />} />
          <Route path="/analyze-keywords" element={<AnalyzeKeywords />} />
          <Route path="/suggest-keywords" element={<SuggestKeywords />} />
          <Route path="/analyze-resume-structure" element={<AnalyzeResumeStructure />} />
          <Route path="/profile" element={<UserProfileComponent />} /> {/* Add this route */}
          <Route path="/" element={
            user ? (isNewUser ? <Navigate to="/welcome" /> : <Navigate to="/home" />)
            : <Navigate to="/login" />
          } />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
