import React, { useEffect, useState } from 'react';
import { Routes, Route  } from 'react-router-dom';
import ApplicationForm from './ApplicationForm';
import StaffScheduler from './StaffScheduler';
import NavBar from './NavBar';
import ViewRequests from './ViewRequests'
import './App.css'
import OwnRequests from './OwnRequests';
import WithdrawRequests from './WithdrawRequests';
import LogIn from './LogIn';
import { useNavigate } from 'react-router-dom';

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    // Check if there is session data for logged in user
    const sessionData = sessionStorage.getItem('userLogin');
    setIsLoggedIn(!!sessionData); // Set to true if session data exists
  }, []);

  const handleLogin = () => {
    setIsLoggedIn(true); // Update the logged-in state
    sessionStorage.setItem('userLogin', true); // Set session data
    console.log(sessionStorage.getItem('role'));
    console.log(sessionStorage.getItem('id'));
    navigate('/StaffScheduler'); // Replace with your target route

  };

  const handleLogout = () => {
    sessionStorage.removeItem('id');
    sessionStorage.removeItem('role');
    sessionStorage.removeItem('userLogin');
    setIsLoggedIn(false); // Update the logged-in state
    navigate('/'); // Replace with your target route
  };

  return (
    <div className="content">
      {isLoggedIn && <NavBar onLogout={handleLogout} />} {/* Pass logout function */}
      <Routes>
        <Route path="/" element={<LogIn onLogin={handleLogin} />} />
        <Route path="/StaffScheduler" element={<StaffScheduler />} />
        <Route path="/applicationForm" element={<ApplicationForm />} />
        <Route path="/OwnRequests" element={<OwnRequests />} />
        <Route path="/ViewRequests" element={<ViewRequests />} />
        <Route path="/WithdrawRequests" element={<WithdrawRequests />} />
      </Routes>
    </div>
  );
};

export default App;
