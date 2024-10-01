import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ApplicationForm from './ApplicationForm';
import StaffScheduler from './StaffScheduler';
import NavBar from './NavBar';
import './App.css'
const App = () => {
  return (
    <div className="content">
      <NavBar />
      <Routes>
        <Route path="/" element={<StaffScheduler />} />
        <Route path="/applicationForm" element={<ApplicationForm />} />
      </Routes>
    </div>
  );
};

export default App;
