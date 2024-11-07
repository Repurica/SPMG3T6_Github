import React, { useState } from 'react';

const LogIn = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async(e) => {
    e.preventDefault();
    let toSend = { 
      "user_id": username,
      "password": password
   }

    // Simulate login process (replace with actual API call)
    try {
      const response = await fetch('https://spm-g3t6-backend-a7e4exepbuewg4hw.southeastasia-01.azurewebsites.net/application/get_role', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(toSend),
      });

      if (response.ok) {
          const jsonResponse = await response.json();
          console.log(jsonResponse);
        // Checking for keys
        if ("error" in jsonResponse) {
          setError('Invalid credentials');
        }

        if ("role" in jsonResponse) {
          sessionStorage.setItem('id', username);
          sessionStorage.setItem('role', jsonResponse.role);
          onLogin()
        }      
      } 
      else {
          console.error('Error:', response.statusText);
          }
  } catch (error) {
      console.error('Error:', error);
  }

  };

  return (
    <div>
      <h2 style={{margin: '20px'}}>Log In</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Username:</label>
          <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} required />
        </div>
        <div>
          <label>Password:</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </div>
        {error && <p style={{ color: 'red', marginTop: '10px', fontWeight: 'bold' }}>{error}</p>}
        <button type="submit">Log In</button>
      </form>
      
    </div>
  );
};

export default LogIn;
