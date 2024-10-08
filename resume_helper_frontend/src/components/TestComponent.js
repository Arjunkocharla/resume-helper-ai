import React from 'react';
import { Button, Typography, Box } from '@mui/material';

function TestComponent() {
  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h4">Test Component</Typography>
      <Button variant="contained" color="primary">
        Test Button
      </Button>
    </Box>
  );
}

export default TestComponent;