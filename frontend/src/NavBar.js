import React from 'react';
import { Link } from 'react-router-dom';

const NavBar = () => {
  return (
    <nav class="navbar">
      <ul>
        <li><Link to="/StaffScheduler">Schedule</Link></li>
        <li><Link to="/ApplicationForm">Application Form</Link></li>
        <li><Link to="/ViewRequests">ViewWFHRequests</Link></li>
        <li><Link to="/OwnRequests">OwnRequests</Link></li>
        <li><Link to="/WithdrawRequests">WithdrawRequests</Link></li>
      </ul>
    </nav>
  );
};

export default NavBar;
