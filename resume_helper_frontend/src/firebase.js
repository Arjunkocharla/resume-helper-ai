// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";
import { getAnalytics } from "firebase/analytics";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDBTfe2vs6WkYQV5-F_NIqSXgNGeS5CuTM",
  authDomain: "resumehelperapp.firebaseapp.com",
  projectId: "resumehelperapp",
  storageBucket: "resumehelperapp.appspot.com",
  messagingSenderId: "75145676789",
  appId: "1:75145676789:web:a301aca05059efbab902bc",
  measurementId: "G-G17B764E0K"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

// Initialize Firebase Authentication and provider
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

export { auth, provider, analytics };
