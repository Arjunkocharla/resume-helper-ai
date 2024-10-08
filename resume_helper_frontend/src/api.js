// src/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:5000',  // Flask backend URL
  headers: {
    'Content-Type': 'multipart/form-data',
    'Access-Control-Allow-Origin': '*'
  },
  withCredentials: true, // Add this if needed, especially for certain CORS configurations
});

export default api;
