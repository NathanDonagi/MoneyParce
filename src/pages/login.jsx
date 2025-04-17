import React, { useState } from 'react';
import './login.css';

const LoginForm = () => {
  // 🔸 Variables (state) to track input values
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  // 🔸 Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Username:', username);
    console.log('Password:', password);
    // Add login logic here (API call, validation, etc.)
  };

  return (
    <div className="login-container">
      <div className="logo">moneyparce</div>
      <form onSubmit={handleSubmit} className="login-box">
        <h2 className="login-title">Login</h2>
        <p className="login-subtext">Access your financial information</p>

        <input
          type="text"
          placeholder="Username"
          className="input-field"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          className="input-field"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <div className="forgot-password">Forgot password?</div>

        <button type="submit" className="login-button">
          Login
        </button>

        <div className="signup-text">
          New? <span className="signup-link">Sign up</span>
        </div>
      </form>
    </div>
  );
};

export default LoginForm;