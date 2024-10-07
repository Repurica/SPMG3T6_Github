


from flask import Blueprint, request, jsonify
from supabase_init import supabase
from datetime import datetime, timedelta

schedule = Blueprint('schedule', __name__)

@schedule.route('/staff_schedules', methods=['GET'])
def get_staff_schedules():
    staff_id = request.args.get('staff_id')

    # Fetch staff details
    staff_data = supabase.table('employee') \
        .select('staff_fname, staff_lname, staff_id') \
        .eq('staff_id', staff_id) \
        .execute()

    if not staff_data.data:
        return jsonify({"error": "No staff found with this ID."}), 404

    # Fetch the schedule for the given staff_id
    schedules = supabase.table('schedule') \
        .select("*") \
        .eq('staff_id', staff_id) \
        .execute()

    if not schedules.data:
        return jsonify({"error": "No schedule found for this staff."}), 404

    # Define time ranges based on WFH status
    time_ranges = {
        'AM': ("08:00:00", "12:00:00"),
        'PM': ("12:00:00", "18:00:00"),
        'Whole day': ("08:00:00", "18:00:00"),
        'in-office': ("08:00:00", "18:00:00")
    }

    # Map day names to offsets from the starting date
    day_offsets = {
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
    }

    # Build the schedules list
    schedules_list = []
    for schedule in schedules.data:
        starting_date = datetime.strptime(schedule['starting_date'], '%Y-%m-%d')
        for day, offset in day_offsets.items():
            wfh_status = schedule.get(day)
            if wfh_status:  # If the day has a schedule
                # Get the appropriate start and end times for the WFH status
                start_time, end_time = time_ranges.get(wfh_status, ("08:00:00", "18:00:00"))

                # Calculate the actual date for this day
                day_date = starting_date + timedelta(days=offset)

                # Combine date and time for startDate and endDate
                start_date_str = f"{day_date.strftime('%Y-%m-%d')}T{start_time}+08:00"
                end_date_str = f"{day_date.strftime('%Y-%m-%d')}T{end_time}+08:00"

                schedules_list.append({
                    'staff_id': schedule['staff_id'],
                    'startDate': datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M:%S%z').isoformat(),
                    'endDate': datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M:%S%z').isoformat(),
                    'wfh': wfh_status  # AM/PM/Whole day/in-office
                })

    # Build the staff data list
    staff = staff_data.data[0]
    staff_info = [{
        'staff_name': f"{staff['staff_fname']} {staff['staff_lname']}",
        'staff_id': staff['staff_id']
    }]
    
    # Return both lists within a JSON response
    return jsonify({
        "schedules": schedules_list,
        "staff_data": staff_info
    })



# can test using this in post man - http://127.0.0.1:5000/schedule/staff_schedules?staff_id=140003




