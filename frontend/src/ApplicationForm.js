import React, { useState, useEffect } from 'react';
import DatePicker from 'react-datepicker';
import ApplicationNotificationModal from './ApplicationNotificationModal';
import 'react-datepicker/dist/react-datepicker.css'; // Import CSS for DatePicker
import './ApplicationForm.css'
// Get date ranges of 2 months before and 3 months after
const getDateRanges = () => {
  const today = new Date();
  const twoMonthsBefore = new Date();
  twoMonthsBefore.setMonth(today.getMonth() - 2).toLocaleString("en-US", { timeZone: "Asia/Singapore" });
  const threeMonthsAfter = new Date();
  threeMonthsAfter.setMonth(today.getMonth() + 3).toLocaleString("en-US", { timeZone: "Asia/Singapore" });
  return {
    formattedCurrentDate: today.toISOString().split('T')[0],
    formattedTwoMonthsBefore: twoMonthsBefore.toISOString().split('T')[0],
    formattedThreeMonthsAfter: threeMonthsAfter.toISOString().split('T')[0],
  };
};
//TO DO: FETCH DATA FROM BACKEND AND SEND DATA TO BACKEND
function ApplicationForm() {
  const [error, setError] = useState(null)
  const [data, setData] = useState([]);
  const { formattedTwoMonthsBefore, formattedThreeMonthsAfter } = getDateRanges();
  const [selection, setSelection] = useState('ad_hoc');
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [timing, setTiming] = useState('')
  const [reason, setReason] = useState('');
  const [checkAM, setCheckAM] = useState("");
  const [checkPM, setCheckPM] = useState("");
  const [checkFullDay, setCheckFullDay] = useState("");
  const [notification, setNotification] = useState('');

  //temp staff id for now
  const staffId = 140002


  // fetch data from application.py
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:5000/application/available_dates', {
          method: 'POST', 
          headers: {
            'Content-Type': 'application/json', // Send JSON data
          },
          body: JSON.stringify({ staff_id: staffId }), // Data to be sent on page load
        });

        if (!response.ok) {
          throw new Error('Failed to fetch data');

        }

        const result = await response.json();
        setData(result['results']);
        setError(null)
      } catch (err) {
        console.log(err.message);
         // display error message for now
         setError(err.message)
      }

    };

    fetchData();
  }, []);

    //when both start and end date present
    useEffect(() => {
      if (startDate && endDate) {  // Ensure both dates are set
        let recurringDays = findRecurringDays(startDate, endDate);
        let amCounter = 0;
        let pmCounter = 0;
        let fullDayCounter = 0;
        
        for (let i = 0; i < recurringDays.length; i++) {
          let checkDate = new Date(recurringDays[i]);
          
          if (blockedAM.some(d => d.getTime() === checkDate.getTime())) {
            amCounter++;
          } else if (blockedPM.some(d => d.getTime() === checkDate.getTime())) {
            pmCounter++;
          } else if (blockedFull.some(d => d.getTime() === checkDate.getTime())) {
            fullDayCounter++;
          }
        }

        if ((amCounter > 0 && pmCounter > 0) || fullDayCounter > 0) {
          alert('Selected date ranges have conflicting dates that are already applied for')
          setEndDate(null)
        }
        else if (amCounter > 0){
          setCheckPM("")
          setCheckFullDay("")
          setCheckAM("Yes")
        }
        else if (pmCounter > 0){
          setCheckPM("Yes")
          setCheckAM("")
          setCheckFullDay("")
      
        }
        else {
          setCheckFullDay("Yes")
          setCheckAM("")
          setCheckPM("")
      
        }
      }
    }, [startDate,endDate]);

  // only start date present   
  useEffect(() => {
    if (startDate) {
      if (selection === 'ad_hoc') {
        if (blockedAM.some(d => d.getTime() === startDate.getTime())){
          setCheckAM("Yes")
          setCheckPM("")
          setCheckFullDay("")
        }

        else if (blockedPM.some(d => d.getTime() === startDate.getTime())){
          setCheckAM("")
          setCheckPM("Yes")
          setCheckFullDay("")
        }
        else {
          setCheckAM("")
          setCheckPM("")
          setCheckFullDay("Yes")
        }
      }

    }

  }, [startDate])



  const blockedFull = []
  const blockedAM = []
  const blockedPM = []

  //filter wfh timings into respective arrays
  for (let i = 0; i < data.length; i++){
    if (data[i]["wfh_timing"] === "AM"){
      blockedAM.push(new Date(data[i]["date"] + "T00:00:00+08:00")) //SGT
    }

    else if (data[i]["wfh_timing"] === "PM"){
      blockedPM.push(new Date(data[i]["date"] + "T00:00:00+08:00"))

    }

    else {
      blockedFull.push(new Date(data[i]["date"] + "T00:00:00+08:00"))
    }
  }

    // find recurring days
    const findRecurringDays = (start, end) => {
      let result = [];
      let currentDate = new Date(start);
      const endDateObj = new Date(end);
      const startDayOfWeek = currentDate.getDay(); // Day of the week of the start date
  
      // Loop through the date range
      while (currentDate <= endDateObj) {
        if (currentDate.getDay() === startDayOfWeek) {
          result.push(new Date(currentDate)); // Store a copy of the date
        }
  
        // Move to the next day
        currentDate.setDate(currentDate.getDate() + 1);
      }
      return result;
    }


  // block out weekends (Saturday and Sunday) and dates that the user has applications pending/accepted
  const isWeekday = (date) => {
    const sgtDate = new Date(date.toLocaleString("en-US", { timeZone: "Asia/Singapore" }));
    const day = sgtDate.getDay();

    // return true for weekdays and dates that are not blocked
    return day !== 0 && day !== 6 && !blockedFull.some(d => d.getTime() === date.getTime());
  };


  //reset all selections
  const handleSelectionChange = (event) => {
    setTiming('')
    setCheckAM("")
    setCheckPM("")
    setCheckFullDay("")
    setStartDate(null)
    setEndDate(null)

    setSelection(event.target.value);


  };

  // for wfh timing radio
  const handleTimingChange = (event) => {
    setTiming(event.target.value);
  };

  
  //check for empty values
  const handleSubmit = async (event) => {
    event.preventDefault();
    if (timing === ''){
      alert('Please select a timing')
    }
    else {
      let toSend = {}
      if (endDate){
        toSend = { 
          "request_type" : selection,
          "starting_date" : startDate.toLocaleDateString("en-CA"), // yyyy-mm-dd format
          "end_date" : endDate.toLocaleDateString("en-CA"),
          "reason" : reason,
          "timing" : timing,
          "staff_id" : staffId
       }          
      }
      else {
        toSend = { 
          "request_type" : selection,
          "starting_date" : startDate.toLocaleDateString("en-CA"),
          "end_date" : endDate,
          "reason" : reason,
          "timing" : timing,
          "staff_id" : staffId
       }  
      }
      //submit
 
      try {
        const response = await fetch('http://localhost:5000/application/store_application', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(toSend),
        });

        if (response.ok) {
            const jsonResponse = await response.json();
            console.log('Success:', jsonResponse);
            setNotification(`Form submitted successfully!`);
        } else {
            console.error('Error:', response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }
    }
  };

  // notification modal
  const handleClose = () => {
    window.location.reload(); // Refresh Page
  };
  if (error){
    return (<h1>Error occured fetching data. Refresh the page</h1>)
  }
  else {
 
  return (
    //form for application
    <div>
      <h1>WFH Application Form</h1>
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
              value="ad_hoc"
              checked={selection === 'ad_hoc'}
              onChange={handleSelectionChange}
            />
            Ad hoc
          </label>
        </div>
        <div>
          <label>Start Date:</label>
          <DatePicker
            selected={startDate}
            onChange={(date) => {
              setTiming('');
              setStartDate(date)
              if (selection === "recurring"){
                if (startDate < endDate){
                  setEndDate(null)
                  setCheckAM("")
                  setCheckPM("")
                  setCheckFullDay("")                 
                }
              };
            }}
            filterDate={isWeekday}
            minDate={formattedTwoMonthsBefore}
            maxDate={formattedThreeMonthsAfter}
            placeholderText="Select a start date"
            required
          />
          {selection === 'recurring' && startDate && ( // indicate what day is selected for recurring
          <span className="day-indicator">
            Selected day: {startDate.toLocaleDateString('en-US', { weekday: 'long' })}
          </span>
        )}

        </div>
        {selection === 'recurring' && startDate && (
          <div>
            <label>End Date:</label>
            <DatePicker
              selected={endDate}
              onChange={(date) => {setTiming('');setEndDate(date);
              } } // TODO: calc the recurring days of WFH and check if with the blocked dates, if have alert user and block out submit 
              filterDate={isWeekday}
              minDate={startDate} // end date must be >= start date
              maxDate={formattedThreeMonthsAfter}
              placeholderText="Select an end date"
              required
            />
          </div>
        )}
        <div>
        {/* Timing radios that checks for timing days applied and prevent them to apply on those days */}
        {checkFullDay === "Yes" && ( 
        <label>
            <input
              type="radio"
              value="full_day"
              checked={timing === 'full_day'}
              onChange={handleTimingChange}
            />
            Full Day
          </label>
          )}

          {(checkPM === "Yes" || checkFullDay === "Yes") && (
          <label>
            <input
              type="radio"
              value="AM"
              checked={timing === 'AM'}
              onChange={handleTimingChange}
            />
            AM
          </label>
          )}
          
          {(checkAM === "Yes" || checkFullDay === "Yes") && (
          <label>
            <input
              type="radio"
              value="PM"
              checked={timing === 'PM'}
              onChange={handleTimingChange}
            />
            PM
          </label>
          )}
        </div>

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
      <ApplicationNotificationModal message={notification} onClose={handleClose} /> 

    </div>
  );
}
}

export default ApplicationForm;
