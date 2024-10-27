import React, {useState, useEffect} from 'react';
import './WithdrawalModal.css';

const WithdrawalModal = ({ isOpen, selectedItem, reason, setReason, handleApply, handleClose }) => {
  const [selectedDates, setSelectedDates] = useState({});

  useEffect(() => {
    if (!isOpen) {
      setSelectedDates({}); // Reset selected dates when modal closes
    }
  }, [isOpen]);

  if (!isOpen || !selectedItem) {
    return null;
  }
  const dates = selectedItem.applied_dates.dates;
  const pending_withdrawal_dates = selectedItem.pending_withdrawal_dates
 // to check amount of dates avail to be withdrawn (if no dates, apply button disabled)
 const checkAvailDatesWithdraw = () => {
  let count = dates.length  
  dates.forEach(element => {
    if (pending_withdrawal_dates.includes(element)){
      count--
    }

  });
  if (count === 0){
    return true
    }
  return false
 }
 // Handle checkbox change
 const handleCheckboxChange = (date) => {
  setSelectedDates((prev) => ({
    ...prev,
    [date]: !prev[date],
  }));
};  

const handleSubmit = (e) => {
  e.preventDefault();
  const isAnySelected = Object.values(selectedDates).some((isSelected) => isSelected);

  if (!isAnySelected) {

    alert("Please select at least one date.");
  } 
  else if (reason.trim() === ''){
    alert('Please enter a empty reason for request')
  }  
  else {
    handleApply(selectedDates); // Pass selected dates to handleApply
    
  }
};

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <button className="close-btn" onClick={handleClose}>X</button>
        <h2>Withdraw Dates</h2>
        <form onSubmit={handleSubmit}>
          <div className="date-grid">
            {dates.map((date) => (
              <div key={date}>
                <label>
                  <input
                    type="checkbox"
                    checked={selectedDates[date] || false}
                    onChange={() => handleCheckboxChange(date)}
                    disabled={pending_withdrawal_dates.includes(date)} // Disable if date is in pending list of witthdrawal dates
                  />
                  &nbsp;{date}
                </label>
              </div>
            ))}
          </div>
        <label>Reason:</label>
        <textarea
          maxLength="300"
          value={reason}
          onChange={(e) => setReason(e.target.value)}
          rows="4"
          placeholder="Enter reason here (Max 300 characters)"
        />
        
        <button type="submit" disabled={checkAvailDatesWithdraw()}>Apply</button>
        </form>

      </div>
    </div>
  );
};

export default WithdrawalModal;