from flask import Blueprint, request
from supabase_init import supabase


sample = Blueprint('sample', __name__)

@sample.route('/all_employee')
def all_employee():
    data = supabase.table('employee').select("*").execute()
    
    return {"result":data.data}

@sample.route('/one_employee')
def one_employee():
    staff_id = request.args.get('id')
    data = supabase.table('employee').select("*").eq('Staff_ID', staff_id).execute()
    data.data
    return {"result":data.data}