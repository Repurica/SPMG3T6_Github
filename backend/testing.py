
from supabase_init import supabase

from datetime import datetime

def get_current_manpower(date, test_manager_id):
   try:
      date_obj = datetime.strptime(date, "%Y-%m-%d")
      day_of_week = date_obj.strftime("%A").lower()
      response_employee = supabase.table("employee").select("staff_id", "staff_fname", "staff_lname").eq("reporting_manager", test_manager_id).execute()
      list_of_staff_ids = []
      
      for staff_id_dict in response_employee.data:
         list_of_staff_ids.append(staff_id_dict["staff_id"])
      print(list_of_staff_ids)
      schedule_response = supabase.table("schedule").select('*').lte('starting_date', date).gte("end_date", date).eq(day_of_week, "in_office").in_("staff_id", list_of_staff_ids).execute()
      count_in_office = len(schedule_response.data) - 1
      max_capacity_response = supabase.table("schedule").select('*').lte('starting_date', date).gte("end_date", date).in_("staff_id", list_of_staff_ids).execute()
      max_capacity = len(max_capacity_response.data)
      percentage_capacity = count_in_office / max_capacity * 100
      formatted_capacity = round(percentage_capacity, 2)  
      if formatted_capacity < 50:
         return {"status": "invalid"}, 200
      else:
         return {"status": "valid"}, 200
   except Exception as e:
      return {"info": repr(e)}, 500
   
status = get_current_manpower("2024-10-08", 140894)
print(status)
   
