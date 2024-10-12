import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ApplicationForm from './ApplicationForm';
import StaffScheduler from './StaffScheduler';
import NavBar from './NavBar';
import ViewRequests from './ViewRequests'
import './App.css'
const App = () => {
  return (
    <div className="content">
      <NavBar />
      <Routes>
        <Route path="/" element={<StaffScheduler />} />
        <Route path="/applicationForm" element={<ApplicationForm />} />
        <Route path="/ViewRequests" element={<ViewRequests />} />
      </Routes>
    </div>
  );
};
 
export default App;
