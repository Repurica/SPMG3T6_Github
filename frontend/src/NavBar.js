import React from 'react';
import { Link } from 'react-router-dom';

const NavBar = ({ onLogout }) => {

  const handleLogoutClick = () => {
    // Call the onLogout function passed from App
    onLogout();
  };

  return (
    <nav class="navbar">
      <ul>
        <li><Link to="/StaffScheduler">Schedule</Link></li>
        <li><Link to="/ApplicationForm">Application Form</Link></li>
        <li><Link to="/OwnRequests">OwnRequests</Link></li>
        
        {(sessionStorage.getItem('role') === '1' || sessionStorage.getItem('role') === '3') && (
        <>
        <li><Link to="/ViewRequests">ViewRequests</Link></li>
        <li><Link to="/WithdrawRequests">WithdrawRequests</Link></li>
        </>
      )}        
        <li>
          <button onClick={handleLogoutClick} className="logout-button">Log Out</button>
        </li>
      </ul>
    </nav>
  );
};

export default NavBar;
