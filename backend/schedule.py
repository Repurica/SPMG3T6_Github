# from flask import Blueprint, request
# from supabase_init import supabase


# schedule = Blueprint('schedule', __name__)

# @schedule.route('/all_employee')
# def all_employee():
#     # data = supabase.table('test_employee').select("*").execute()
    
#     # return {"result":data.data}
#     pass

# @schedule.route('/one_schedule')
# def one_employee():
#     # staff_id = request.args.get('id')
#     # data = supabase.table('test_employee').select("*").eq('Staff_ID', staff_id).execute()
#     # data.data
#     # return {"result":data.data}

#     pass
from flask import Blueprint, request
from supabase_init import supabase
from datetime import datetime

schedule = Blueprint('schedule', __name__)

@schedule.route('/schedule_by_date', methods=['GET'])
def get_schedule_by_date():
    """
    Fetch the schedule for a specific staff based on staff_id and date.
    """
    try:
        # Get staff_id and the specific date from query parameters
        staff_id = request.args.get('staff_id')
        date_str = request.args.get('date')  # Date in format 'YYYY-MM-DD'
        specific_date = datetime.strptime(date_str, '%Y-%m-%d').date()

        # Query the Supabase table for schedule data with the given staff_id
        data = supabase.table('schedule').select("*").eq('staff_id', staff_id).execute()

        # Check if data is found
        if not data.data:
            return {"status": "error", "message": "No schedule found for the given staff ID"}, 404

        # Loop through the schedules to find the one where the specific date is within the range
        for record in data.data:
            start_date = datetime.strptime(record['starting_date'], '%Y-%m-%d').date()
            end_date = datetime.strptime(record['end_date'], '%Y-%m-%d').date()

            if start_date <= specific_date <= end_date:
                # Determine the day of the week for the specific date
                day_of_week = specific_date.strftime('%A').lower()  # e.g., 'monday', 'tuesday', etc.

                # Return the schedule for the specific day
                if day_of_week in record:
                    schedule_for_day = record[day_of_week]
                    return {"status": "success", "schedule": schedule_for_day}, 200
                else:
                    return {"status": "error", "message": "No schedule available for this day"}, 404

        return {"status": "error", "message": "No schedule found for the given date"}, 404

    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

# http://127.0.0.1:5000/schedule/schedule_by_date?staff_id=140003&date=2024-10-04 - Can use this to test postman