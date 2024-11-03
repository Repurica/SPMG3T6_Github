import 'devextreme/dist/css/dx.material.blue.light.css';
import './StaffScheduler.css';
import React, { useState, useEffect, useCallback } from 'react';
import { Scheduler, View, Resource } from 'devextreme-react/scheduler';
import { fetchWithRetry } from './FetchWithRetry';
import RadioGroup from 'devextreme-react/radio-group';
import SelectBox from 'devextreme-react/select-box';

function StaffScheduler() {
    const [ownSchedule, setOwnSchedule] = useState([]);  
    const [teamSchedule, setTeamSchedule] = useState([]);  
    const [staffData, setStaffData] = useState([]);
    const [startDate, setStartDate] = useState(null);
    const [endDate, setEndDate] = useState(null);

    const id = sessionStorage.getItem('id');
    const role = sessionStorage.getItem('role');

    const resourcesList = ['Own Schedule', 'Team Schedule'];
    const [currentResource, setCurrentResource] = useState(resourcesList[0]);
    const onRadioGroupValueChanged = useCallback((e) => {
        setCurrentResource(e.value);
    }, []);

    const deptList = ['All', 'Sales', 'Engineering', 'HR', 'Finance', 'Consultancy', 'Solutioning', 'IT']
    const [selectedDept, setSelectedDept] = useState('All');
    const handleSelectionChange = useCallback((e) => {
        setSelectedDept(e.value);
    }, []);

    const [currentView, setCurrentView] = useState('Day');


    const groups = ['staff_id'];

    useEffect(() => {
        const fetchSchedules = async () => {
            try {                
                const url = `http://127.0.0.1:5000/schedule/staff_schedules?staff_id=${id}`;
                const ownResponse = await fetchWithRetry(url, {
                        method: 'GET'
                    }, 3, 1000);  // 3 retries with a 1 second delay
                const ownData = await ownResponse.json();   // Parse JSON data
                setOwnSchedule(ownData.schedules); 
            } catch (error) {
                console.log('Error fetching own schedules:', error.message);
            }

            try {
                let teamResponse;
                if (role === '1') {
                    teamResponse = await fetchWithRetry('http://127.0.0.1:5000/schedule/all_schedules', {
                        method: 'GET'
                    }, 3, 1000);  // Fetch Team Schedule
                } else {
                    const url = `http://127.0.0.1:5000/schedule/team_schedules?staff_id=${id}`;
                    teamResponse = await fetchWithRetry(url, {
                            method: 'GET'
                        }, 3, 1000);  // 3 retries with a 1 second delay
                }
                const teamData = await teamResponse.json();
                setTeamSchedule(teamData.schedules);  
                setStaffData(teamData.staff_data);  
                console.log(teamSchedule)
            } catch (error) {
                console.log('Error fetching own schedules:', error.message);
            }
        };
        fetchSchedules();
    }, [id]);

    useEffect(() => {
    //   const currentDate = new Date();
      const currentDate = new Date('2024-10-20'); // for testing
      currentDate.setHours(0, 0, 0, 0)
      currentDate.setMonth(currentDate.getMonth() - 2); 
      setStartDate(currentDate.toDateString()); 
    }, []);

    useEffect(() => {
        // const currentDate = new Date();
        const currentDate = new Date('2024-10-20'); // for testing
        currentDate.setHours(0, 0, 0, 0)
        currentDate.setMonth(currentDate.getMonth() + 3); 
        setEndDate(currentDate.toDateString()); 
        // console.log(endDate)
      }, []);

    // Choose own/team schedules based on current resource selection
    const getSchedule = () => {
        let schedule

        if (currentResource === 'Own Schedule') {
            schedule = ownSchedule.filter(item => new Date(item.startDate).setHours(0, 0, 0, 0) >= new Date(startDate).setHours(0, 0, 0, 0)
            && new Date(item.startDate).setHours(0, 0, 0, 0) <= new Date(endDate).setHours(0, 0, 0, 0));  // show only schedules 2m back, 3m forward
        } else if (currentResource === 'Team Schedule') {
            schedule = teamSchedule.filter(item => new Date(item.startDate).setHours(0, 0, 0, 0) >= new Date(startDate).setHours(0, 0, 0, 0) 
            && new Date(item.startDate).setHours(0, 0, 0, 0) <= new Date(endDate).setHours(0, 0, 0, 0));
        }

        if (selectedDept === 'All') {
            return schedule
        } else {
            return schedule.filter(item => item.dept === selectedDept)
        }
    };

    const getStaff = () => {
        let staff

        staff = staffData.map(item => ({  
            ...item,
            staff_display: `${item.staff_name} (${item.position})`
          }));

        if (selectedDept === 'All') {
            return staff
        } else {
            return staff.filter(item => item.dept === selectedDept)
        }
    }

    const [selectedDate, setSelectedDate] = useState(new Date());
    const handleDateChange = (newDate) => {
        setSelectedDate(newDate);
        console.log(newDate)
    };

    const isSameDay = (date1, date2) => {
        return (
            date1.getFullYear() === date2.getFullYear() &&
            date1.getMonth() === date2.getMonth() &&
            date1.getDate() === date2.getDate()
        );
    };

    return (
        <React.Fragment>
            <div className="utility">
                {currentView === 'Day' && currentResource === 'Team Schedule' && (
                    <div className="ppl_count">
                        <p>AM Count: {getStaff().length - getSchedule().filter(item => (item.wfh === 'AM WFH' || item.wfh === 'Full Day WFH') && isSameDay(selectedDate, new Date(item.startDate))).length} In Office, {getSchedule().filter(item => (item.wfh === 'AM WFH' || item.wfh === 'Full Day WFH') && isSameDay(selectedDate, new Date(item.startDate))).length} WFH</p>
                        <p>PM Count: {getStaff().length - getSchedule().filter(item => (item.wfh === 'PM WFH' || item.wfh === 'Full Day WFH') && isSameDay(selectedDate, new Date(item.startDate))).length} In Office, {getSchedule().filter(item => (item.wfh === 'PM WFH' || item.wfh === 'Full Day WFH') && isSameDay(selectedDate, new Date(item.startDate))).length} WFH</p>
                    </div>
                )}

                {role === '1' && currentResource === 'Team Schedule' && (
                    <div className="dept">
                        Filter Department:
                        <SelectBox
                            items={deptList}
                            value={selectedDept}
                            onValueChanged={handleSelectionChange}
                            placeholder="All"
                            searchEnabled={true}
                        />
                    </div>
                )}

                <div className="option">
                    <RadioGroup
                        items={resourcesList}
                        value={currentResource}
                        layout="horizontal"
                        onValueChanged={onRadioGroupValueChanged}
                    />
                </div>

                <div className="dept">

                </div>
            </div>
            <Scheduler id='scheduler'
                dataSource={getSchedule()}
                groups={groups}
                firstDayOfWeek={1}
                startDayHour={9}
                endDayHour={18}
                textExpr='wfh'
                defaultCurrentView="timelineDay"
                min={startDate}
                max={endDate}
                height={700}
                onCurrentViewChange={(view) => {
                    setCurrentView(view)
                }}
                onCurrentDateChange={handleDateChange}
                maxAppointmentsPerCell={'unlimited'}
                editing={false}
                crossScrollingEnabled={true}>

                <View
                    type="timelineDay"
                    name='Day'
                    cellDuration={60}
                    groupOrientation='vertical'
                />

                <View
                    type="timelineWeek"
                    name='Week'
                    cellDuration={270}
                />

                <Resource
                    fieldExpr="wfh"
                    dataSource={[
                        { id: 'AM WFH', text: 'AM WFH', color: '#76C1FA' },
                        { id: 'PM WFH', text: 'WFH PM', color: '#FF8C00' },
                        { id: 'Full Day WFH', text: 'Full Day WFH', color: '#8000FC' }
                    ]}
                    label="WFH Status"
                    useColorAsDefault={true}
                />

                <Resource
                    fieldExpr='staff_id'
                    dataSource={currentResource === 'Team Schedule' ? getStaff() : []}
                    label="Staff"
                    valueExpr='staff_id'
                    displayExpr='staff_display'
                    useColorAsDefault={true}
                />
            </Scheduler>
        </React.Fragment>
    );
}
 
export default StaffScheduler;