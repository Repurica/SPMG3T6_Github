from flask import Blueprint, request
from supabase_init import supabase


schedule = Blueprint('schedule', __name__)

@schedule.route('/all_employee')
def all_employee():
    # data = supabase.table('test_employee').select("*").execute()
    
    # return {"result":data.data}
    pass

@schedule.route('/one_schedule')
def one_employee():
    # staff_id = request.args.get('id')
    # data = supabase.table('test_employee').select("*").eq('Staff_ID', staff_id).execute()
    # data.data
    # return {"result":data.data}

    pass