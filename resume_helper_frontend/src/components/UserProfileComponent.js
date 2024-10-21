import React, { useState } from 'react';
import {
  Box, Typography, Button, TextField, Select, MenuItem, Avatar,
  Grid, Card, CardContent, LinearProgress, List, ListItem, ListItemIcon, ListItemText
} from '@mui/material';
import {
  CloudUpload as CloudUploadIcon, Lock as LockIcon, Delete as DeleteIcon,
  Person as PersonIcon, Security as SecurityIcon, Settings as SettingsIcon,
  Edit as EditIcon, Work as WorkIcon, School as SchoolIcon
} from '@mui/icons-material';

const UserProfileComponent = () => {
  const [activeSection, setActiveSection] = useState('profile');
  const [newResume, setNewResume] = useState(null);
  const [userInfo, setUserInfo] = useState({
    name: 'John Doe',
    email: 'john.doe@example.com',
    primaryIndustry: 'Software Development',
    totalExperience: '5',
    resumeScore: 75
  });

  const handleFileChange = (e) => {
    setNewResume(e.target.files[0]);
  };

  const handleUserInfoChange = (e) => {
    const { name, value } = e.target;
    setUserInfo({ ...userInfo, [name]: value });
  };

  const renderProfileSection = () => (
    <Grid container spacing={4}>
      <Grid item xs={12} md={4}>
        <Card elevation={0} sx={{ background: 'rgba(255, 255, 255, 0.05)', backdropFilter: 'blur(10px)', borderRadius: '16px' }}>
          <CardContent sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', p: 4 }}>
            <Avatar sx={{ width: 120, height: 120, mb: 2 }}>{userInfo.name[0]}</Avatar>
            <Typography variant="h5" sx={{ color: 'white', mb: 1 }}>{userInfo.name}</Typography>
            <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>{userInfo.email}</Typography>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12} md={8}>
        <Card elevation={0} sx={{ background: 'rgba(255, 255, 255, 0.05)', backdropFilter: 'blur(10px)', borderRadius: '16px' }}>
          <CardContent sx={{ p: 4 }}>
            <Typography variant="h6" sx={{ color: 'white', mb: 3 }}>Profile Information</Typography>
            <Grid container spacing={3}>
              <Grid item xs={12} sm={6}>
                <Select
                  fullWidth
                  value={userInfo.primaryIndustry}
                  onChange={handleUserInfoChange}
                  name="primaryIndustry"
                  sx={{ mb: 3, color: 'white', '.MuiOutlinedInput-notchedOutline': { borderColor: 'rgba(255, 255, 255, 0.3)' } }}
                >
                  <MenuItem value="Software Development">Software Development</MenuItem>
                  <MenuItem value="Data Science">Data Science</MenuItem>
                  <MenuItem value="Marketing">Marketing</MenuItem>
                </Select>
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Total Experience (years)"
                  name="totalExperience"
                  type="number"
                  value={userInfo.totalExperience}
                  onChange={handleUserInfoChange}
                  variant="outlined"
                  sx={{ mb: 3, input: { color: 'white' }, label: { color: 'rgba(255, 255, 255, 0.7)' }, '.MuiOutlinedInput-notchedOutline': { borderColor: 'rgba(255, 255, 255, 0.3)' } }}
                />
              </Grid>
            </Grid>
            <Box sx={{ mt: 3 }}>
              <Typography variant="h6" sx={{ color: 'white', mb: 2 }}>Resume Score</Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Box sx={{ width: '100%', mr: 2 }}>
                  <LinearProgress variant="determinate" value={userInfo.resumeScore} sx={{ height: 10, borderRadius: 5 }} />
                </Box>
                <Typography variant="body2" sx={{ color: 'white', minWidth: 35 }}>{`${userInfo.resumeScore}%`}</Typography>
              </Box>
              <Button variant="contained" color="primary">Improve Your Score</Button>
            </Box>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12}>
        <Card elevation={0} sx={{ background: 'rgba(255, 255, 255, 0.05)', backdropFilter: 'blur(10px)', borderRadius: '16px' }}>
          <CardContent sx={{ p: 4 }}>
            <Typography variant="h6" sx={{ color: 'white', mb: 3 }}>Upload/Change Resume</Typography>
            <input
              type="file"
              accept=".pdf,.docx"
              onChange={handleFileChange}
              style={{ display: 'none' }}
              id="upload-resume"
            />
            <label htmlFor="upload-resume">
              <Button variant="outlined" component="span" startIcon={<CloudUploadIcon />} sx={{ color: 'white', borderColor: 'rgba(255, 255, 255, 0.3)', '&:hover': { borderColor: 'white' } }}>
                {newResume ? newResume.name : 'Choose File'}
              </Button>
            </label>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );

  const renderSecuritySection = () => (
    <Card elevation={0} sx={{ background: 'rgba(255, 255, 255, 0.05)', backdropFilter: 'blur(10px)', borderRadius: '16px' }}>
      <CardContent sx={{ p: 4 }}>
        <Typography variant="h6" sx={{ color: 'white', mb: 3 }}>Change Password</Typography>
        <TextField fullWidth label="New Password" type="password" variant="outlined" sx={{ mb: 3, input: { color: 'white' }, label: { color: 'rgba(255, 255, 255, 0.7)' }, '.MuiOutlinedInput-notchedOutline': { borderColor: 'rgba(255, 255, 255, 0.3)' } }} />
        <Button variant="contained" color="primary" startIcon={<LockIcon />}>Update Password</Button>
      </CardContent>
    </Card>
  );

  const renderAccountSection = () => (
    <Card elevation={0} sx={{ background: 'rgba(255, 255, 255, 0.05)', backdropFilter: 'blur(10px)', borderRadius: '16px' }}>
      <CardContent sx={{ p: 4 }}>
        <Typography variant="h6" sx={{ color: 'white', mb: 3 }}>Account Management</Typography>
        <Button variant="outlined" color="secondary" startIcon={<DeleteIcon />} sx={{ mr: 2 }}>Disable Account</Button>
        <Button variant="contained" color="error" startIcon={<DeleteIcon />}>Remove Account</Button>
      </CardContent>
    </Card>
  );

  return (
    <Box sx={{ minHeight: '100vh', background: 'linear-gradient(135deg, #0F172A 0%, #1E293B 100%)', p: 4 }}>
      <Grid container spacing={4}>
        <Grid item xs={12} md={3}>
          <Card elevation={0} sx={{ background: 'rgba(255, 255, 255, 0.05)', backdropFilter: 'blur(10px)', borderRadius: '16px' }}>
            <CardContent>
              <List>
                <ListItem button selected={activeSection === 'profile'} onClick={() => setActiveSection('profile')}>
                  <ListItemIcon><PersonIcon sx={{ color: 'white' }} /></ListItemIcon>
                  <ListItemText primary="Profile" sx={{ color: 'white' }} />
                </ListItem>
                <ListItem button selected={activeSection === 'security'} onClick={() => setActiveSection('security')}>
                  <ListItemIcon><SecurityIcon sx={{ color: 'white' }} /></ListItemIcon>
                  <ListItemText primary="Security" sx={{ color: 'white' }} />
                </ListItem>
                <ListItem button selected={activeSection === 'account'} onClick={() => setActiveSection('account')}>
                  <ListItemIcon><SettingsIcon sx={{ color: 'white' }} /></ListItemIcon>
                  <ListItemText primary="Account" sx={{ color: 'white' }} />
                </ListItem>
              </List>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={9}>
          {activeSection === 'profile' && renderProfileSection()}
          {activeSection === 'security' && renderSecuritySection()}
          {activeSection === 'account' && renderAccountSection()}
        </Grid>
      </Grid>
    </Box>
  );
};

export default UserProfileComponent;
