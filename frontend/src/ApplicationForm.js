import React, { useState, useEffect } from 'react';
import DatePicker from 'react-datepicker';
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
  const { formattedTwoMonthsBefore, formattedThreeMonthsAfter } = getDateRanges();
  const [selection, setSelection] = useState('ad-hoc');
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [timing, setTiming] = useState('')
  const [reason, setReason] = useState('');
  const [checkAM, setCheckAM] = useState("");
  const [checkPM, setCheckPM] = useState("");
  const [checkFullDay, setCheckFullDay] = useState("");


  const json = [{"date":"2024-09-30","wfh_timing":"AM"}, {"date":"2024-10-07","wfh_timing":"AM"}, {"date":"2024-10-11","wfh_timing":"PM"}, {"date":"2024-10-09","wfh_timing":"Full Day"}]
  const blockedFull = []
  const blockedAM = []
  const blockedPM = []
  for (let i = 0; i < json.length; i++){
    if (json[i]["wfh_timing"] === "AM"){
      blockedAM.push(new Date(json[i]["date"] + "T00:00:00+08:00")) //SGT
    }

    else if (json[i]["wfh_timing"] === "PM"){
      blockedPM.push(new Date(json[i]["date"] + "T00:00:00+08:00"))

    }

    else {
      blockedFull.push(new Date(json[i]["date"] + "T00:00:00+08:00"))
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
    //when both start and end date present
    useEffect(() => {
      if (startDate && endDate) {  // Ensure both dates are set
        let recurringDays = findRecurringDays(startDate, endDate);
        console.log(startDate)
        console.log(endDate)
        console.log(recurringDays)
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
        console.log(amCounter)
        console.log(pmCounter)
        console.log(fullDayCounter)
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



  useEffect(() => {
    if (startDate) {
      if (selection === 'ad-hoc') {
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
  const handleSubmit = (event) => {
    event.preventDefault();
    if (timing === ''){
      alert('Please select a timing')
    }
    else {
      //submit
      console.log(startDate)
      console.log(endDate)
      console.log(selection)
      console.log(timing)
      console.log(reason)
    }
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
              value="Full Day"
              checked={timing === 'Full Day'}
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
    </div>
  );
}

export default ApplicationForm;
