import React from 'react';
import { Routes, Route  } from 'react-router-dom';
import ApplicationForm from './ApplicationForm';
import StaffScheduler from './StaffScheduler';
import NavBar from './NavBar';
import ViewRequests from './ViewRequests'
import './App.css'
import OwnRequests from './OwnRequests';
import WithdrawRequests from './WithdrawRequests';
const App = () => {
  return (
    <div className="content">
      <NavBar />
      <Routes>
        <Route path="/" element={<StaffScheduler />} />
        <Route path="/applicationForm" element={<ApplicationForm />} />
        <Route path="/ViewRequests" element={<ViewRequests />} />
        <Route path="/OwnRequests" element={<OwnRequests />} />
        <Route path="/WithdrawRequests" element={<WithdrawRequests />} />
      </Routes>
    </div>
  );
};
 
export default App;
