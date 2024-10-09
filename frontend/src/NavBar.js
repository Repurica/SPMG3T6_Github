import React from 'react';
import { Link } from 'react-router-dom';

const NavBar = () => {
  return (
    <nav class="navbar">
      <ul>
        <li><Link to="/">Schedule</Link></li>
        <li><Link to="/ApplicationForm">Application Form</Link></li>
        <li><Link to="/ViewRequests">ViewRequests - temp route for now</Link></li>
      </ul>
    </nav>
  );
};

export default NavBar;
