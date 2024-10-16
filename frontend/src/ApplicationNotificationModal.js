import React from 'react';
import './ApplicationNotificationModal.css';

const ApplicationNotificationModal = ({ message, onClose }) => {
  if (!message) return null;

  return (
    <div className="modal-overlay">
      <div className="modal">
        <h2>{message}</h2>
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
};

export default ApplicationNotificationModal;