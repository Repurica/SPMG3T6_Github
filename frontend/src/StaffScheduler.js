import 'devextreme/dist/css/dx.light.css';
import { schedules, staffData, onsiteData } from './schedules.js';
 
import { Scheduler, View, Resource } from 'devextreme-react/scheduler';
 
function StaffScheduler() {
    const groups = ['ownerId'];

    return (
        <Scheduler id="scheduler"
            dataSource={schedules}
            textExpr="text"
            allDayExpr="dayLong"
            recurrenceRuleExpr="recurrence"
            defaultCurrentView="timelineDay"
            groups={groups}
            height={700}
            adaptivityEnabled={true}>

            <View
                type="timelineDay"
                name='Day'
                startDayHour={10}
                endDayHour={22}
            />

            <View
                type="timelineWeek"
                name='Week'
                startDayHour={10}
                endDayHour={22}
            />

            <Resource
                fieldExpr="onsite"
                allowMultiple={false}
                dataSource={onsiteData}
                label="Onsite"
            />

            <Resource
                fieldExpr="ownerId"
                allowMultiple={true}
                dataSource={staffData}
                label="Owner"
                useColorAsDefault={true}
            />
        </Scheduler>
    );
}
 
export default StaffScheduler;