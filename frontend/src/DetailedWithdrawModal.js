import React from 'react';
import './DetailedRequestModal.css';

const DetailedWithdrawModal = ({ isOpen, selectedItem, reason, setReason, handleAccept, handleReject, handleClose }) => {
  if (!isOpen || !selectedItem) {
    return null;
  }

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <button className="close-btn" onClick={handleClose}>X</button>
        <h2>Request Details</h2>
        <p><strong>Staff Name:</strong> {selectedItem.staff_name}</p>
        <p><strong>Staff ID:</strong> {selectedItem.staff_id}</p>
        <p><strong>Dates to Withdraw:</strong> {selectedItem.withdrawn_dates.dates.join(", ")}</p>

        <p><strong>Timing:</strong> {selectedItem.wfh_timing === 'full_day' ? 'Full Day' : selectedItem.wfh_timing}</p>
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


        <div className="modal-actions">
          <button className="accept-btn" onClick={handleAccept}>Accept</button>
          <button className="reject-btn" onClick={handleReject}>Reject</button>
        </div>
      </div>
    </div>
  );
};

export default DetailedWithdrawModal;