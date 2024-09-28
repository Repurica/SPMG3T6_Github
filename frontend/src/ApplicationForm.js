import React, { useState } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css'; // Import CSS for DatePicker
import './ApplicationForm.css'
// Get date ranges of 2 months before and 3 months after
const getDateRanges = () => {
  const today = new Date();
  const twoMonthsBefore = new Date();
  twoMonthsBefore.setMonth(today.getMonth() - 2);
  const threeMonthsAfter = new Date();
  threeMonthsAfter.setMonth(today.getMonth() + 3);

  return {
    formattedCurrentDate: today.toISOString().split('T')[0],
    formattedTwoMonthsBefore: twoMonthsBefore.toISOString().split('T')[0],
    formattedThreeMonthsAfter: threeMonthsAfter.toISOString().split('T')[0],
  };
};
//TO DO: AXIOS GET PENDING ACCEPTED DATES, BLOCK OFF IN DATEPICKER, IF RECURRING, CHECK FOR THE DATES AND DISALLOW THEM TO SUBMIT IF SO, AXIOS TO BACKEND.
// ideas - filter received dates into blocked (full day wfh), AM & PM
// Need functions for these probabably
// FOR ADHOC: after select date (ONCHANGE), show timing radio, if date in AM, show pm only, if none, show all.
// FOR RECURRING: ONLY SHOW END DATE AFTER START DATE (ONCHANGE)
// IF BOTH HAVE VALUES (ONCHANGE), calc all recurring dates inbetween the dates. Check dates for AM, PM or full day (add counter)
// IF have full day, break loop and disselect end date, notify user with pop up
// If have both AM and PM, same ()
// If only AM/PM, timing radio only for the opposite
// Else, all timing radios avail.

function ApplicationForm() {
  const { formattedTwoMonthsBefore, formattedThreeMonthsAfter } = getDateRanges();
  const [selection, setSelection] = useState('ad-hoc');
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [timing, setTiming] = useState('Full Day')
  const [reason, setReason] = useState('');

  // block out weekends (Saturday and Sunday) and dates that the user has applications pending/accepted
  const isWeekday = (date) => {
    const day = date.getDay();
    // block specific dates (e.g. Sep 30, Oct 2)
    const blockedDates = [ //temp values for now
      new Date(2024, 8, 30), // Sep 30, 2024 (remember month is 0-indexed)
      new Date(2024, 9, 2),  // Oct 2, 2024
    ];

    // return true for weekdays and dates that are not blocked
    return day !== 0 && day !== 6 && !blockedDates.some(d => d.getTime() === date.getTime());
  };

  // for ad-hoc recurring radio
  const handleSelectionChange = (event) => {
    setSelection(event.target.value);
    if (event.target.value === 'ad-hoc') {
      setEndDate(startDate); // Set end date to start date for ad-hoc
    }
  };

  // for wfh timing radio
  const handleTimingChange = (event) => {
    setTiming(event.target.value);
  };

  //check for empty values
  const handleSubmit = (event) => {
    event.preventDefault();
    alert('Selection: ' + selection +
      '\nStart Date: ' + startDate?.toLocaleDateString() +
      '\nEnd Date: ' + (selection === 'recurring' ? endDate?.toLocaleDateString() : startDate?.toLocaleDateString()) +
      '\nReason: ' + reason);
  };

  return (
    //form for application
    <div>
      <h1>Schedule Form</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            <input
              type="radio"
              value="recurring"
              checked={selection === 'recurring'}
              onChange={handleSelectionChange}
            />
            Recurring
          </label>
          <label>
            <input
              type="radio"
              value="ad-hoc"
              checked={selection === 'ad-hoc'}
              onChange={handleSelectionChange}
            />
            Ad-hoc
          </label>
        </div>
        <div>
        <label>
            <input
              type="radio"
              value="Full Day"
              checked={timing === 'Full Day'}
              onChange={handleTimingChange}
            />
            Full Day
          </label>
          <label>
            <input
              type="radio"
              value="AM"
              checked={timing === 'AM'}
              onChange={handleTimingChange}
            />
            AM
          </label>
          <label>
            <input
              type="radio"
              value="PM"
              checked={timing === 'PM'}
              onChange={handleTimingChange}
            />
            PM
          </label>

        </div>
        <div>
          <label>Start Date:</label>
          <DatePicker
            selected={startDate}
            onChange={(date) => {
              setStartDate(date);
              if (selection === 'ad-hoc') {
                setEndDate(date); // sync end date with start date if ad-hoc
              }
            }}
            filterDate={isWeekday}
            minDate={new Date(formattedTwoMonthsBefore)}
            maxDate={new Date(formattedThreeMonthsAfter)}
            placeholderText="Select a start date"
            required
          />
          {selection === 'recurring' && startDate && ( // indicate what day is selected for recurring
          <span className="day-indicator">
            Selected day: {startDate.toLocaleDateString('en-US', { weekday: 'long' })}
          </span>
        )}

        </div>
        {selection === 'recurring' && (
          <div>
            <label>End Date:</label>
            <DatePicker
              selected={endDate}
              onChange={(date) => setEndDate(date) } // TODO: calc the recurring days of WFH and check if with the blocked dates, if have alert user and block out submit 
              filterDate={isWeekday}
              minDate={new Date(startDate)} // end date must be >= start date
              maxDate={new Date(formattedThreeMonthsAfter)}
              placeholderText="Select an end date"
              required
            />
          </div>
        )}

        <div>
          <label>Reason:</label>
          <textarea
            maxLength="300"
            value={reason}
            onChange={(e) => setReason(e.target.value)}
            placeholder="Enter your reason for WFH application here. Max 300 characters"
            required
          />
        </div>

        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default ApplicationForm;
