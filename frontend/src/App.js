import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ApplicationForm from './ApplicationForm';
import SchedulerTest from './SchedulerTest';
import NavBar from './NavBar';
import './App.css'
const App = () => {
  return (
    <div className="content">
      <NavBar />
      <Routes>
        <Route path="/" element={<SchedulerTest />} />
        <Route path="/applicationForm" element={<ApplicationForm />} />
      </Routes>
    </div>
  );
};

export default App;
