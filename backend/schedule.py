# from flask import Blueprint, request
# from supabase_init import supabase


# schedule = Blueprint('schedule', __name__)

# # @schedule.route('/all_employee')
# # def all_employee():
# #     # data = supabase.table('test_employee').select("*").execute()
    
# #     # return {"result":data.data}
# #     pass

# # @schedule.route('/one_schedule')
# # def one_employee():
# #     # staff_id = request.args.get('id')
# #     # data = supabase.table('test_employee').select("*").eq('Staff_ID', staff_id).execute()
# #     # data.data
# #     # return {"result":data.data}

# #     pass
# from flask import Blueprint, request
# from supabase_init import supabase
# from datetime import datetime

# schedule = Blueprint('schedule', __name__)

# @schedule.route('/schedule_by_date', methods=['GET'])
# def get_schedule_by_date():
#     """
#     Fetch the schedule for a specific staff based on staff_id and date.
#     """
#     try:
#         # Get staff_id and the specific date from query parameters
#         staff_id = request.args.get('staff_id')
#         date_str = request.args.get('date')  # Date in format 'YYYY-MM-DD'
#         specific_date = datetime.strptime(date_str, '%Y-%m-%d').date()

#         # Query the Supabase table for schedule data with the given staff_id
#         data = supabase.table('schedule').select("*").eq('staff_id', staff_id).execute()

#         # Check if data is found
#         if not data.data:
#             return {"status": "error", "message": "No schedule found for the given staff ID"}, 404

#         # Loop through the schedules to find the one where the specific date is within the range
#         for record in data.data:
#             start_date = datetime.strptime(record['starting_date'], '%Y-%m-%d').date()
#             end_date = datetime.strptime(record['end_date'], '%Y-%m-%d').date()

#             if start_date <= specific_date <= end_date:
#                 # Determine the day of the week for the specific date
#                 day_of_week = specific_date.strftime('%A').lower()  # e.g., 'monday', 'tuesday', etc.

#                 # Return the schedule for the specific day
#                 if day_of_week in record:
#                     schedule_for_day = record[day_of_week]
#                     return {"status": "success", "schedule": schedule_for_day}, 200
#                 else:
#                     return {"status": "error", "message": "No schedule available for this day"}, 404

#         return {"status": "error", "message": "No schedule found for the given date"}, 404

#     except Exception as e:
#         return {"status": "error", "message": str(e)}, 500

# # http://127.0.0.1:5000/schedule/schedule_by_date?staff_id=140003&date=2024-10-04 - Can use this to test postman



# # Endpoint to get team schedule based on position (team members)
# @schedule.route('/team_schedule')
# def team_schedule():
#     # Get the staff_id and date from query parameters
#     staff_id = request.args.get('staff_id')
#     date_str = request.args.get('date')  

#     # Convert date string to a proper date object
#     try:
#         date = datetime.strptime(date_str, '%Y-%m-%d').date()
#     except ValueError:
#         return {"error": "Invalid date format. Use YYYY-MM-DD."}, 400

#     # Query to get the position of the staff making the request
#     staff_position_data = supabase.table('employee') \
#         .select('position') \
#         .eq('staff_id', staff_id) \
#         .single() \
#         .execute()

#     if not staff_position_data.data:
#         return {"error": "Staff not found."}, 404

#     # Extract the position of the querying staff member
#     position = staff_position_data.data['position']

#     # Query to get all team members with the same position and role=2 (staff)
#     team_members = supabase.table('employee') \
#         .select('staff_id', 'staff_fname', 'staff_lname') \
#         .eq('position', position) \
#         .eq('role', 2) \
#         .execute()

#     if not team_members.data:
#         return {"error": "No team members found."}, 404

#     # For each team member, get their schedule for the given date
#     results = []
#     for member in team_members.data:
#         member_id = member['staff_id']

#         # Query for the team member's schedule based on staff_id and date
#         schedule_data = supabase.table('schedule') \
#             .select("*") \
#             .eq('staff_id', member_id) \
#             .lte('starting_date', date) \
#             .gte('end_date', date) \
#             .execute()

#         if schedule_data.data:
#             # Extract the schedule for the specific day
#             day_of_week = date.strftime('%A').lower()  # e.g., 'monday', 'tuesday'
#             member_schedule = schedule_data.data[0].get(day_of_week, "No schedule")

#             # Add the member's schedule to the result list
#             results.append({
#                 "staff_id": member_id,
#                 "name": f"{member['staff_fname']} {member['staff_lname']}",
#                 "schedule": member_schedule
#             })
#         else:
#             # If no schedule is found for the member on that date
#             results.append({
#                 "staff_id": member_id,
#                 "name": f"{member['staff_fname']} {member['staff_lname']}",
#                 "schedule": "No schedule"
#             })

 
#     return {"team_schedule": results}


#     # can test in postman using http://127.0.0.1:5000/schedule/team_schedule?staff_id=140003&date=2024-10-01



# from flask import jsonify
# from datetime import datetime

# @schedule.route('/staff_schedules', methods=['GET'])
# def get_staff_schedules():
#     staff_id = request.args.get('staff_id')
    
#     # Fetch staff details
#     staff_data = supabase.table('employee') \
#         .select('staff_fname, staff_lname, staff_id') \
#         .eq('staff_id', staff_id) \
#         .execute()
    
#     if not staff_data.data:
#         return jsonify({"error": "No staff found with this ID."}), 404

#     # Fetch the schedule for the given staff_id
#     schedules = supabase.table('schedule') \
#         .select("*") \
#         .eq('staff_id', staff_id) \
#         .execute()

#     if not schedules.data:
#         return jsonify({"error": "No schedule found for this staff."}), 404

#     # Define time ranges based on WFH status
#     time_ranges = {
#         'AM': ("08:00:00", "12:00:00"),
#         'PM': ("12:00:00", "18:00:00"),
#         'Whole day': ("08:00:00", "18:00:00"),
#         'in-office': ("08:00:00", "18:00:00")
#     }

#     # Build the schedules list
#     schedules_list = []
#     for schedule in schedules.data:
#         for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
#             wfh_status = schedule.get(day)
#             if wfh_status:  # If the day has a schedule
#                 # Get the appropriate start and end times for the WFH status
#                 start_time, end_time = time_ranges.get(wfh_status, ("08:00:00", "18:00:00"))

#                 # Combine date and time for startDate and endDate
#                 start_date_str = f"{schedule['starting_date']}T{start_time}+08:00"
#                 end_date_str = f"{schedule['end_date']}T{end_time}+08:00"

#                 schedules_list.append({
#                     'staff_id': schedule['staff_id'],
#                     'startDate': datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M:%S%z').isoformat(),
#                     'endDate': datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M:%S%z').isoformat(),
#                     'wfh': wfh_status  # AM/PM/Whole day/in-office
#                 })

#     # Build the staff data list
#     staff = staff_data.data[0]
#     staff_info = [{
#         'staff_name': f"{staff['staff_fname']} {staff['staff_lname']}",
#         'staff_id': staff['staff_id']
#     }]
    
#     # Return both lists within a JSON response
#     return jsonify({
#         "schedules": schedules_list,
#         "staff_data": staff_info
#     })




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








