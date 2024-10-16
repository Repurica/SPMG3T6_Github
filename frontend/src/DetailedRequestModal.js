import React from 'react';
import './DetailedRequestModal.css';

const DetailedRequestModal = ({ isOpen, selectedItem, reason, setReason, handleAccept, handleReject, handleClose }) => {
  if (!isOpen || !selectedItem) {
    return null;
  }

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <button className="close-btn" onClick={handleClose}>X</button>
        <h2>Request Details</h2>
        <p><strong>Staff Name:</strong> {selectedItem.staff_fullname}</p>
        <p><strong>Position ID:</strong> {selectedItem.staff_id}</p>
        <p><strong>Application Date:</strong> {selectedItem.created_at}</p>
        <p><strong>Request Type:</strong> {selectedItem.request_type === 'ad_hoc' ? 'Ad Hoc' : 'Recurring'}</p>
        <p><strong>Start Date:</strong> {selectedItem.starting_date}</p>
        {selectedItem.request_type !== 'ad_hoc' && (
          <p><strong>End Date:</strong> {selectedItem.end_date}</p>
        )}
        <p><strong>Timing:</strong> {selectedItem.timing === 'full_day' ? 'Full Day' : selectedItem.timing}</p>
        <div className="reason-box">
            <p><strong>Reason for request:</strong> {selectedItem.reason}</p>
        </div>


        <label htmlFor="reason">Reason for Approval/Rejection:</label>
        <textarea
          id="reason"
          maxLength="300"
          value={reason}
          onChange={(e) => setReason(e.target.value)}
          rows="4"
          placeholder="Enter reason here (Max 300 characters)"
        />

        {selectedItem.capacity === 'invalid' && (<p class='insufficient-manpower'>Manpower in office is insufficient (&lt;= 50%)</p>)}

        <div className="modal-actions">
          <button className="accept-btn" onClick={handleAccept} disabled ={selectedItem.capacity === 'invalid'}>Accept</button>
          <button className="reject-btn" onClick={handleReject}>Reject</button>
        </div>
      </div>
    </div>
  );
};

export default DetailedRequestModal;