import 'devextreme/dist/css/dx.light.css';
import { schedules, staffData } from './schedules.js';
import { useState, useEffect } from 'react';
import { Scheduler, View, Resource, Editing } from 'devextreme-react/scheduler';
import { fetchWithRetry } from './FetchWithRetry';

function StaffScheduler() {
    const [error, setError] = useState(null)
    const [schedules, setSchedules] = useState([]);
    const [staffData, setStaffData] = useState([]);
    const [startDate, setStartDate] = useState(null);
    const [endDate, setEndDate] = useState(null);

    const groups = ['staff_id'];

    useEffect(() => {
        const fetchSchedules = async () => {
            try {
                const response = await fetchWithRetry('http://127.0.0.1:5000/schedule/staff_schedules?staff_id=140525', {
                    method: 'GET'
                }, 3, 1000);  // 3 retries with a 1 second delay
                const data = await response.json();  // Parse JSON data
                setSchedules(data.schedules);
                setStaffData(data.staff_data);
                setError(null);
            } catch (error) {
                console.log(error.message);
                setError(error.message); // Display error message
            }
        };
    
        fetchSchedules();
    }, []);

    useEffect(() => {
      const currentDate = new Date();
      currentDate.setMonth(currentDate.getMonth() - 2); 
      setStartDate(currentDate.toDateString()); 
    }, []);

    useEffect(() => {
        const currentDate = new Date();
        currentDate.setMonth(currentDate.getMonth() + 3); 
        setEndDate(currentDate.toDateString()); 
      }, []);

    return (
        <Scheduler id='scheduler'
            // dataSource={schedules}
            dataSource={schedules.filter(item => new Date(item.startDate) >= new Date(startDate) 
                && new Date(item.startDate) <= new Date(endDate))}
            groups={groups}
            firstDayOfWeek={1}
            startDayHour={8}
            endDayHour={17}
            textExpr="wfh"
            defaultCurrentView="timelineDay"
            min={startDate}
            max={endDate}
            height={700}>
            
            <Editing
                allowAdding={false}
                allowDeleting={false}
                allowDragging={false}
                allowResizing={false}
                allowTimeZoneEditing={false}
                allowUpdating={false}
            />

            <View
                type="timelineDay"
                name='Day'
                cellDuration={60}
            />

            <View
                type="timelineWeek"
                name='Week'
                cellDuration={270}
            />

            <Resource
                fieldExpr='staff_id'
                dataSource={staffData}
                label="Staff"
                valueExpr='staff_id'
                displayExpr='staff_name'
                useColorAsDefault={true}
            />
        </Scheduler>
    );
}
 
export default StaffScheduler;