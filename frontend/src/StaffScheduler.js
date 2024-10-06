import 'devextreme/dist/css/dx.light.css';
import { schedules, staff_data } from './schedules.js';
import { useState, useEffect } from 'react';
import { Scheduler, View, Resource, Editing } from 'devextreme-react/scheduler';

function StaffScheduler() {
    const groups = ['staff_id'];

    const [startDate, setStartDate] = useState(null);
    const [endDate, setEndDate] = useState(null);

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
            dataSource={schedules.filter(item => new Date(item.startDate).getDate() >= new Date(startDate).getDate() 
                && new Date(item.startDate).getDate() <= new Date(endDate).getDate())}
            groups={groups}
            firstDayOfWeek={1}
            startDayHour={8}
            endDayHour={17}
            textExpr="wfh"
            defaultCurrentView="timelineDay"
            min={startDate}
            max={endDate}>
            
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
                dataSource={staff_data}
                label="Staff"
                valueExpr='staff_id'
                displayExpr='staff_name'
                useColorAsDefault={true}
            />
        </Scheduler>
    );
}
 
export default StaffScheduler;