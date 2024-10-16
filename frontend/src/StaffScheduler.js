import 'devextreme/dist/css/dx.light.css';
import './StaffScheduler.css';
import React, { useState, useEffect, useCallback } from 'react';
import { Scheduler, View, Resource, Editing } from 'devextreme-react/scheduler';
import { fetchWithRetry } from './FetchWithRetry';
import RadioGroup from 'devextreme-react/radio-group';

function StaffScheduler() {
    const [error, setError] = useState(null)
    const [ownSchedule, setOwnSchedule] = useState([]);  
    const [teamSchedule, setTeamSchedule] = useState([]);  
    const [staffData, setStaffData] = useState([]);
    const [startDate, setStartDate] = useState(null);
    const [endDate, setEndDate] = useState(null);

    const resourcesList = ['Own Schedule', 'Team Schedule'];
    const [currentResource, setCurrentResource] = useState(resourcesList[0]);
    const onRadioGroupValueChanged = useCallback((e) => {
      setCurrentResource(e.value);
    }, []);

    const groups = ['staff_id'];

    useEffect(() => {
        const fetchSchedules = async () => {
            try {
                const ownResponse = await fetchWithRetry('http://127.0.0.1:5000/schedule/staff_schedules?staff_id=140525', {
                    method: 'GET'
                }, 3, 1000);  // 3 retries with a 1 second delay
                const ownData = await ownResponse.json();   // Parse JSON data
                setOwnSchedule(ownData.schedules); 

                const teamResponse = await fetchWithRetry('http://127.0.0.1:5000/schedule/team_schedules?staff_id=140525', {
                    method: 'GET'
                }, 3, 1000);  // Fetch Team Schedule
                const teamData = await teamResponse.json();
                setTeamSchedule(teamData.schedules);  
                setStaffData(teamData.staff_data);  
                console.log(teamSchedule)

                setError(null);
            } catch (error) {
                console.log(error.message);
                setError(error.message);  // Display error message
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

    // Choose own/team schedules based on current resource selection
    const getSchedule = () => {
        if (currentResource === 'Own Schedule') {
            return ownSchedule.filter(item => new Date(item.startDate) >= new Date(startDate) 
            && new Date(item.startDate) <= new Date(endDate));  // show only schedules 2m back, 3m forward
        } else if (currentResource === 'Team Schedule') {
            return teamSchedule.filter(item => new Date(item.startDate) >= new Date(startDate) 
            && new Date(item.startDate) <= new Date(endDate));
        }
        return [];
    };

    return (
        <React.Fragment>
            <div className="options">
                <div className="option">
                <RadioGroup
                    items={resourcesList}
                    value={currentResource}
                    layout="horizontal"
                    onValueChanged={onRadioGroupValueChanged}
                />
                </div>
            </div>
            <Scheduler id='scheduler'
                dataSource={getSchedule()}
                groups={groups}
                firstDayOfWeek={1}
                startDayHour={9}
                endDayHour={18}
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
                    dataSource={currentResource == 'Team Schedule' ? staffData : []}
                    label="Staff"
                    valueExpr='staff_id'
                    displayExpr='staff_name'
                    useColorAsDefault={true}
                    // useColorAsDefault={currentResource === 'Room'} need add colour attribute
                />
            </Scheduler>
        </React.Fragment>
    );
}
 
export default StaffScheduler;