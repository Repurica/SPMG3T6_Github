# 14-10 HT edited time_ranges



from flask import Blueprint, request, jsonify
from supabase_init import supabase
from datetime import datetime, timedelta

schedule = Blueprint('schedule', __name__)

@schedule.route('/staff_schedules', methods=['GET'])
def get_staff_schedules():
    staff_id = request.args.get('staff_id')

    # Fetch staff details including department, position, and reporting manager
    staff_data = supabase.table('employee') \
        .select('staff_fname, staff_lname, staff_id, dept, position, reporting_manager') \
        .eq('staff_id', staff_id) \
        .execute()

    if not staff_data.data:
        return jsonify({"error": "No staff found with this ID."}), 404

    # Fetch reporting manager's name
    reporting_manager_id = staff_data.data[0]['reporting_manager']
    reporting_manager_data = supabase.table('employee') \
        .select('staff_fname, staff_lname') \
        .eq('staff_id', reporting_manager_id) \
        .execute()

    if not reporting_manager_data.data:
        reporting_manager_name = "No reporting manager found"
    else:
        reporting_manager_name = f"{reporting_manager_data.data[0]['staff_fname']} {reporting_manager_data.data[0]['staff_lname']}"

    # Fetch the schedule for the given staff_id
    schedules = supabase.table('schedule') \
        .select("*") \
        .eq('staff_id', staff_id) \
        .execute()

    if not schedules.data:
        return jsonify({"error": "No schedule found for this staff."}), 404

    # Define time ranges based on WFH status
    time_ranges = {
        'AM': ("09:00:00", "13:00:00"),
        'PM': ("14:00:00", "18:00:00"),
        'Whole day': ("09:00:00", "18:00:00"),
        'in-office': ("09:00:00", "18:00:00")
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
                start_time, end_time = time_ranges.get(wfh_status, ("09:00:00", "18:00:00"))

                # Calculate the actual date for this day
                day_date = starting_date + timedelta(days=offset)

                # Combine date and time for startDate and endDate
                start_date_str = f"{day_date.strftime('%Y-%m-%d')}T{start_time}+08:00"
                end_date_str = f"{day_date.strftime('%Y-%m-%d')}T{end_time}+08:00"

                schedules_list.append({
                    'staff_id': schedule['staff_id'],
                    'dept': staff_data.data[0]['dept'],  # Adding department
                    'position': staff_data.data[0]['position'],  # Adding position
                    'startDate': datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M:%S%z').isoformat(),
                    'endDate': datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M:%S%z').isoformat(),
                    'wfh': wfh_status,  # AM/PM/Whole day/in-office
                    'reporting_manager': reporting_manager_name  # Adding reporting manager name
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












@schedule.route('/team_schedules', methods=['GET'])
def get_team_schedules():
    # Get staff ID from the query parameters
    staff_id = request.args.get('staff_id')
    
    # Fetch staff data for the given staff_id to get the reporting manager and department
    staff_data = supabase.table('employee') \
        .select('staff_fname, staff_lname, staff_id, position, role, dept, reporting_manager') \
        .eq('staff_id', staff_id) \
        .execute()

    # Check if the staff exists
    if not staff_data.data:
        return jsonify({"error": "No staff found with this ID."}), 404

    # Get the reporting manager of the staff member
    reporting_manager_id = staff_data.data[0]['reporting_manager']

    # Fetch the reporting manager's name
    manager_data = supabase.table('employee') \
        .select('staff_fname, staff_lname') \
        .eq('staff_id', reporting_manager_id) \
        .execute()

    if not manager_data.data:
        return jsonify({"error": "No reporting manager found for this staff."}), 404

    # Construct the manager's full name
    reporting_manager_name = f"{manager_data.data[0]['staff_fname']} {manager_data.data[0]['staff_lname']}"

    # Fetch all team members who have the same reporting manager
    team_members = supabase.table('employee') \
        .select('staff_fname, staff_lname, staff_id, position, role, dept') \
        .eq('reporting_manager', reporting_manager_id) \
        .execute()

    # Check if any team members are found
    if not team_members.data:
        return jsonify({"error": "No team members found for this reporting manager."}), 404

    # Define work-from-home time ranges
    time_ranges = {
        'AM': ("09:00:00", "13:00:00"),
        'PM': ("14:00:00", "18:00:00"),
        'Whole day': ("09:00:00", "18:00:00"),
        'in-office': ("09:00:00", "18:00:00")
    }

    # Define day offsets for weekdays
    day_offsets = {
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
    }

    # Initialize the final output lists
    all_schedules = []
    all_staff_data = []

    # Loop over each team member
    for member in team_members.data:
        member_id = member['staff_id']

        # Fetch schedules for this team member
        schedules = supabase.table('schedule') \
            .select("*") \
            .eq('staff_id', member_id) \
            .execute()

        # If schedules are found, process them
        if schedules.data:
            schedules_list = []
            for schedule in schedules.data:
                starting_date = datetime.strptime(schedule['starting_date'], '%Y-%m-%d')

                # Loop over each weekday in the schedule
                for day, offset in day_offsets.items():
                    wfh_status = schedule.get(day)
                    if wfh_status:
                        start_time, end_time = time_ranges.get(wfh_status, ("09:00:00", "18:00:00"))
                        day_date = starting_date + timedelta(days=offset)

                        start_date_str = f"{day_date.strftime('%Y-%m-%d')}T{start_time}+08:00"
                        end_date_str = f"{day_date.strftime('%Y-%m-%d')}T{end_time}+08:00"

                        # Append this day's schedule to the list as a single list for each staff
                        schedules_list.append({
                            'staff_id': member['staff_id'],
                            'dept': member['dept'],  # Adding department
                            'position': member['position'],  # Adding position
                            'startDate': datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M:%S%z').isoformat(),
                            'endDate': datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M:%S%z').isoformat(),
                            'wfh': wfh_status,
                            'reporting_manager': reporting_manager_name  # Adding reporting manager's name
                        })

            # Add schedules for this team member as a single long list
            all_schedules.append(schedules_list)

        # Determine if the member is a manager based on the role
        is_manager = member['role'] == 3  # Role 3 means Manager

        # Append the staff data for this member, including dept and position
        all_staff_data.append({
            'staff_name': f"{member['staff_fname']} {member['staff_lname']}",
            'staff_id': member['staff_id'],
            'dept': member['dept'],  # Adding department
            'position': member['position'],  # Adding position
            'manager': is_manager,
            'reporting_manager': reporting_manager_name  # Adding reporting manager's name
        })

    # Flatten the schedules to ensure each staff has one long list
    flattened_schedules = [schedule for sublist in all_schedules for schedule in sublist]

    # Return the final result as JSON
    return jsonify({
        "schedules": flattened_schedules,
        "staff_data": all_staff_data
    })



# use http://127.0.0.1:5000/schedule/team_schedules?staff_id=140003 for testing
