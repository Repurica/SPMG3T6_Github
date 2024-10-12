


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




@schedule.route('/team_schedules_by_staff', methods=['GET'])
def get_team_schedules_by_staff():
    # Get the staff_id from the request
    staff_id = request.args.get('staff_id')
    
    # Fetch the staff data based on the given staff_id
    staff_data = supabase.table('employee') \
        .select('staff_fname, staff_lname, staff_id, position, role') \
        .eq('staff_id', staff_id) \
        .execute()

    # Check if the staff exists
    if not staff_data.data:
        return jsonify({"error": "Staff not found."}), 404
    
    # Get the position and role of the given staff
    position = staff_data.data[0]['position']
    role = staff_data.data[0]['role']
    
    # Fetch all staff members with the same position (the team)
    team_data = supabase.table('employee') \
        .select('staff_fname, staff_lname, staff_id, position, role') \
        .eq('position', position) \
        .execute()

    # Check if any team members found
    if not team_data.data:
        return jsonify({"error": "No team members found with this position."}), 404

    # Initialize list to hold all staff data with their schedules
    team_schedule_data = []

    # Fetch schedules for each team member
    for staff in team_data.data:
        team_member_id = staff['staff_id']

        # Fetch schedules for each team member
        schedules = supabase.table('schedule') \
            .select("*") \
            .eq('staff_id', team_member_id) \
            .execute()

        # Prepare the list of schedules for this team member
        staff_schedules = []
        if schedules.data:
            starting_date = datetime.strptime(schedules.data[0]['starting_date'], '%Y-%m-%d')

            # Iterate through each schedule and build schedule entries
            for schedule in schedules.data:
                for day, offset in day_offsets.items():
                    wfh_status = schedule.get(day)
                    if wfh_status:
                        start_time, end_time = time_ranges.get(wfh_status, ("08:00:00", "18:00:00"))
                        day_date = starting_date + timedelta(days=offset)

                        start_date_str = f"{day_date.strftime('%Y-%m-%d')}T{start_time}+08:00"
                        end_date_str = f"{day_date.strftime('%Y-%m-%d')}T{end_time}+08:00"

                        staff_schedules.append({
                            'startDate': datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M:%S%z').isoformat(),
                            'endDate': datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M:%S%z').isoformat(),
                            'wfh': wfh_status
                        })

        # Add team member's data and their schedules to the final list
        team_schedule_data.append({
            'staff_name': f"{staff['staff_fname']} {staff['staff_lname']}",
            'staff_id': staff['staff_id'],
            'position': staff['position'],
            'role': staff['role'],  # Include the role if necessary
            'schedules': staff_schedules
        })

    # Return the final list of team members with their schedules
    return jsonify(team_schedule_data)


