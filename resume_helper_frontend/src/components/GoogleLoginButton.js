import React from 'react';
import { useNavigate } from 'react-router-dom';
import { auth, provider } from '../firebase';
import { signInWithPopup } from "firebase/auth";

function GoogleLoginButton() {
  const navigate = useNavigate();

  const signInWithGoogle = async () => {
    try {
      const result = await signInWithPopup(auth, provider);
      console.log(result.user); // Here, you can handle user data.
      navigate("/home"); // Redirect to home page after login
    } catch (error) {
      console.error("Error during sign-in: ", error);
    }
  };

  return (
    <button onClick={signInWithGoogle}>
      Sign in with Google
    </button>
  );
}

export default GoogleLoginButton;
