# # # 14-10 HT edited time_ranges




from flask import Blueprint, request, jsonify
from supabase_init import supabase
from datetime import datetime, timedelta

schedule = Blueprint('schedule', __name__)

# Helper function to fetch employee details
def fetch_employee_details(staff_id):
    return supabase.table('employee') \
        .select('staff_fname, staff_lname, staff_id, dept, position, reporting_manager') \
        .eq('staff_id', staff_id) \
        .execute()

# Helper function to fetch schedules for an employee
def fetch_schedules(staff_id):
    return supabase.table('schedule') \
        .select("*") \
        .eq('staff_id', staff_id) \
        .execute()

# Helper function to fetch reporting manager's name
def fetch_reporting_manager(reporting_manager_id):
    manager_data = supabase.table('employee') \
        .select('staff_fname, staff_lname') \
        .eq('staff_id', reporting_manager_id) \
        .execute()
    if manager_data.data:
        return f"{manager_data.data[0]['staff_fname']} {manager_data.data[0]['staff_lname']}"
    return "No reporting manager found"

# Mapping for WFH wording conversion
wfh_wording = {
    "AM": "AM WFH",
    "PM": "PM WFH",
    "full_day": "Full Day WFH"
}

@schedule.route('/staff_schedules', methods=['GET'])
def get_staff_schedules():
    staff_id = request.args.get('staff_id')
    staff_data = fetch_employee_details(staff_id)

    if not staff_data.data:
        return jsonify({"error": "No staff found with this ID."}), 404

    reporting_manager_id = staff_data.data[0]['reporting_manager']
    reporting_manager_name = fetch_reporting_manager(reporting_manager_id)

    schedules = fetch_schedules(staff_id)

    if not schedules.data:
        return jsonify({"error": "No schedule found for this staff."}), 404

    time_ranges = {
        'AM': ("09:00:00", "13:00:00"),
        'PM': ("14:00:00", "18:00:00"),
        'full_day': ("09:00:00", "18:00:00"),
        'in_office': ("09:00:00", "18:00:00")
    }

    day_offsets = {
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
    }

    schedules_list = []
    for schedule in schedules.data:
        starting_date = datetime.strptime(schedule['starting_date'], '%Y-%m-%d')
        for day, offset in day_offsets.items():
            wfh_status = schedule.get(day)
            if wfh_status and wfh_status != "in_office":
                # Convert wfh_status to the desired wording
                wfh_display = wfh_wording.get(wfh_status, wfh_status)
                
                start_time, end_time = time_ranges.get(wfh_status, ("09:00:00", "18:00:00"))
                day_date = starting_date + timedelta(days=offset)
                start_date_str = f"{day_date.strftime('%Y-%m-%d')}T{start_time}+08:00"
                end_date_str = f"{day_date.strftime('%Y-%m-%d')}T{end_time}+08:00"

                schedules_list.append({
                    'staff_id': schedule['staff_id'],
                    'dept': staff_data.data[0]['dept'],
                    'position': staff_data.data[0]['position'],
                    'startDate': datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M:%S%z').isoformat(),
                    'endDate': datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M:%S%z').isoformat(),
                    'wfh': wfh_display,
                    'reporting_manager': reporting_manager_name
                })

    staff_info = [{
        'staff_name': f"{staff_data.data[0]['staff_fname']} {staff_data.data[0]['staff_lname']}",
        'staff_id': staff_data.data[0]['staff_id']
    }]

    return jsonify({"schedules": schedules_list, "staff_data": staff_info})





# test http://127.0.0.1:5000/schedule/staff_schedules?staff_id=140003






@schedule.route('/team_schedules', methods=['GET'])
def get_team_schedules():
    staff_id = request.args.get('staff_id')
    staff_data = fetch_employee_details(staff_id)

    if not staff_data.data:
        return jsonify({"error": "No staff found with this ID."}), 404

    reporting_manager_id = staff_data.data[0]['reporting_manager']
    reporting_manager_name = fetch_reporting_manager(reporting_manager_id)

    team_members = supabase.table('employee') \
        .select('staff_fname, staff_lname, staff_id, position, role, dept') \
        .eq('reporting_manager', reporting_manager_id) \
        .execute()

    if not team_members.data:
        return jsonify({"error": "No team members found for this reporting manager."}), 404

    # Define time ranges and WFH status mappings
    time_ranges = {
        'AM': ("09:00:00", "13:00:00"),
        'PM': ("14:00:00", "18:00:00"),
        'full_day': ("09:00:00", "18:00:00"),
        'in_office': ("09:00:00", "18:00:00")
    }
    wfh_status_mappings = {
        'AM': "AM WFH",
        'PM': "PM WFH",
        'full_day': "Full Day WFH"
    }

    day_offsets = {
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
    }

    all_schedules = []
    all_staff_data = []

    for member in team_members.data:
        member_id = member['staff_id']
        schedules = fetch_schedules(member_id)

        if schedules.data:
            schedules_list = []
            for schedule in schedules.data:
                starting_date = datetime.strptime(schedule['starting_date'], '%Y-%m-%d')
                for day, offset in day_offsets.items():
                    wfh_status = schedule.get(day)
                    if wfh_status and wfh_status != "in_office":
                        start_time, end_time = time_ranges.get(wfh_status, ("09:00:00", "18:00:00"))
                        day_date = starting_date + timedelta(days=offset)
                        start_date_str = f"{day_date.strftime('%Y-%m-%d')}T{start_time}+08:00"
                        end_date_str = f"{day_date.strftime('%Y-%m-%d')}T{end_time}+08:00"

                        # Map the WFH status to the appropriate wording
                        formatted_wfh_status = wfh_status_mappings.get(wfh_status, wfh_status)

                        schedules_list.append({
                            'staff_id': member['staff_id'],
                            'dept': member['dept'],
                            'position': member['position'],
                            'startDate': datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M:%S%z').isoformat(),
                            'endDate': datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M:%S%z').isoformat(),
                            'wfh': formatted_wfh_status,
                            'reporting_manager': reporting_manager_name
                        })

            all_schedules.append(schedules_list)
            all_staff_data.append({
                'staff_name': f"{member['staff_fname']} {member['staff_lname']}",
                'staff_id': member['staff_id']
            })

    return jsonify({"schedules": all_schedules, "staff_data": all_staff_data})


# test http://127.0.0.1:5000/schedule/team_schedules?staff_id=140003








@schedule.route('/all_schedules', methods=['GET'])
def get_all_schedules():
    employee_data = supabase.table('employee') \
        .select('staff_fname, staff_lname, staff_id, position, role, dept, reporting_manager') \
        .execute()

    if not employee_data.data or len(employee_data.data) == 0:
        return jsonify({"error": "No employees found."}), 404

    all_schedules = []
    all_staff_data = []

    # Define time ranges and WFH status mappings
    time_ranges = {
        'AM': ("09:00:00", "13:00:00"),
        'PM': ("14:00:00", "18:00:00"),
        'full_day': ("09:00:00", "18:00:00"),
        'in_office': ("09:00:00", "18:00:00")
    }
    wfh_status_mappings = {
        'AM': "AM WFH",
        'PM': "PM WFH",
        'full_day': "Full Day WFH"
    }

    day_offsets = {
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
    }

    for employee in employee_data.data:
        member_id = employee['staff_id']
        schedules = fetch_schedules(member_id)

        if schedules.data:
            schedules_list = []
            for schedule in schedules.data:
                starting_date = datetime.strptime(schedule['starting_date'], '%Y-%m-%d')
                for day, offset in day_offsets.items():
                    wfh_status = schedule.get(day)
                    if wfh_status and wfh_status != "in_office":
                        start_time, end_time = time_ranges.get(wfh_status, ("09:00:00", "18:00:00"))
                        day_date = starting_date + timedelta(days=offset)
                        start_date_str = f"{day_date.strftime('%Y-%m-%d')}T{start_time}+08:00"
                        end_date_str = f"{day_date.strftime('%Y-%m-%d')}T{end_time}+08:00"

                        # Map the WFH status to the appropriate wording
                        formatted_wfh_status = wfh_status_mappings.get(wfh_status, wfh_status)

                        schedules_list.append({
                            'staff_id': member_id,
                            'dept': employee['dept'],
                            'position': employee['position'],
                            'startDate': datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M:%S%z').isoformat(),
                            'endDate': datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M:%S%z').isoformat(),
                            'wfh': formatted_wfh_status,
                            'reporting_manager': fetch_reporting_manager(employee['reporting_manager'])
                        })

            all_schedules.append(schedules_list)
            all_staff_data.append({
                'staff_name': f"{employee['staff_fname']} {employee['staff_lname']}",
                'staff_id': employee['staff_id']
            })

    return jsonify({"schedules": all_schedules, "staff_data": all_staff_data})



# #  test using http://127.0.0.1:5000/schedule/all_schedules
