from flask import Blueprint
from supabase_init import supabase


sample = Blueprint('sample', __name__)

@sample.route('/get_data')
def get_data():
    data = supabase.table('employee').select("*").execute()
    row1 = data.data[0]
    return row1