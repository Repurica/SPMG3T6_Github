from flask import request, Blueprint
from supabase_init import supabase
import traceback
from datetime import datetime, timedelta, date

application = Blueprint('application', __name__)

# Helper function to get_dates_between_2_dates
def get_dates_on_same_weekday(start_date_str, end_date_str):
   start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
   end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

   # List to store dates that fall on the same weekday
   same_day_dates = []

   delta = timedelta(weeks=1)

   # Looping through the dates between start_date and end_date
   current_date = start_date
   while current_date <= end_date:
      same_day_dates.append(current_date)
      current_date += delta

   return same_day_dates

def get_matching_weekday_dates(start_date, end_date):
   # Convert the input strings to datetime objects
   start_date = datetime.strptime(start_date, "%Y-%m-%d")
   end_date = datetime.strptime(end_date, "%Y-%m-%d")
   
   # Get the weekday of the start date (0 = Monday, 6 = Sunday)
   start_weekday = start_date.weekday()
   
   # Initialize an empty list to hold the matching dates
   matching_dates = []
   
   # Iterate over the date range
   current_date = start_date
   while current_date <= end_date:
      if current_date.weekday() == start_weekday:
         matching_dates.append(current_date.strftime("%Y-%m-%d"))
      current_date += timedelta(days=1)
   
   return matching_dates

@application.route('/available_dates', methods=['POST'])
# Function that returns all dates at which requests have already been made
def return_available_dates():
   json_sent = request.get_json()
   # staff id comes in from front-end, so staff_id is hardcoded for now
   staff_id = json_sent["staff_id"]
   # extract from supabase the dates where the staff is WFH
   results = []
   # Looping through 
   try:
      data_recurring = supabase.table("application").select("starting_date", "end_date", "timing").eq("staff_id", staff_id).eq("request_type", "recurring").neq("status","rejected").execute()
      data_ad_hoc = supabase.table("application").select("starting_date", "timing").eq("staff_id", staff_id).neq("status","rejected").eq("request_type", "ad_hoc").execute() 
      adhoc_results = data_ad_hoc.data   
      recurring_results = data_recurring.data
      results = []
      for result in recurring_results:
         start_date = result["starting_date"]
         end_date = result["end_date"]
         wfh_timing = result["timing"]
         dates_list = get_dates_on_same_weekday(start_date, end_date)
         print(dates_list)
         for date in dates_list:
            results.append({"date": date.strftime("%Y-%m-%d"),
                        "wfh_timing": wfh_timing})
      # print(results)
      for result2 in adhoc_results:
         start_date = result2["starting_date"]
         wfh_timing_adhoc = result2["timing"]
         results.append({"date": start_date, "wfh_timing": wfh_timing_adhoc})
      return {"results": results}, 200
   except Exception as e:
      return {"results": results,
            "info": repr(e)}, 500

@application.route('/store_application', methods=['POST'])
def store_application():
   json_sent = request.get_json()

   try:
      count_records = supabase.table("application").select("*", count="exact").execute()
      json_sent["application_id"] = count_records.count + 1
      json_sent["status"] = "pending"
      response = supabase.table("application").insert(json_sent).execute()
      if response and response.data:
         return {"count": count_records.count, "status": "success"}, 200
      else:
         return {"status": "error", "message": "could not insert into database"}, 404
   except Exception as e:
      return {"info": repr(e)}, 500

@application.route('/retrieve_pending_requests', methods=['POST'])
def retrieve_pending_requests():
   json_sent = request.get_json()
   print(json_sent["manager_id"])
   try:
      response_employee = supabase.table("employee").select("staff_id", "staff_fname", "staff_lname").eq("reporting_manager", json_sent["manager_id"]).execute()
      list_of_staff_ids = []
      dict_staff_ids_names = {}
      
      for staff_id_dict in response_employee.data:
         list_of_staff_ids.append(staff_id_dict["staff_id"])
      for staff_id_dict in response_employee.data:
         dict_staff_ids_names[staff_id_dict["staff_id"]] = staff_id_dict["staff_fname"] + " " + staff_id_dict["staff_lname"]
         
      response_application = supabase.table("application").select("application_id", "staff_id", "created_at", "starting_date", "end_date", "timing", "request_type", "reason").in_("staff_id", list_of_staff_ids).eq("status", "pending").execute()
      returned_result = response_application.data
      # print(dict_staff_ids_names)
      for record in returned_result:
         record_staff_id = record["staff_id"]
         record["staff_fullname"] = dict_staff_ids_names[record_staff_id]
         starting_date = record["starting_date"]
         end_date = record["end_date"]
         request_type = record["request_type"]
         if request_type == "recurring":
            dates_between = get_matching_weekday_dates(starting_date, end_date)
            for date in dates_between:
               print(date)
               response = get_current_manpower(date, json_sent["manager_id"])
               if response[0]["status"] == "invalid":
                  record["capacity"] = "invalid"
                  break
               record["capacity"] = "valid"
         else:
            response = get_current_manpower(starting_date, json_sent["manager_id"])
            print(response)
            status = response[0]["status"]
            record["capacity"] = status

      sorted_data = sorted(returned_result, key=lambda x: datetime.fromisoformat(x["created_at"]))
      for item in sorted_data:
         created_at_datetime = datetime.fromisoformat(item["created_at"])
         item["created_at"] = created_at_datetime.strftime("%Y-%m-%d")

      result_dict = {item["application_id"]: {key: value for key, value in item.items()} for item in sorted_data}
      return result_dict, 200

   except Exception as e:
      return {"info": repr(e), "traceback": traceback.format_exc()}, 500



@application.route("/store_approval_rejection", methods=['POST'])
def store_approval_rejection():
    json_sent = request.get_json()
    
    try:
        sent_id = json_sent["id"]
        sent_outcome = json_sent["outcome"]
        outcome_reason = json_sent.get("outcome_reason", "")
        
        if sent_outcome == "approved":
            # Update application table with approval
            application_response = supabase.table("application").update(
                {"status": "approved", "outcome_reason": outcome_reason}
            ).eq("application_id", sent_id).execute()

            employee_id_response = supabase.table("application").select(
                "staff_id", "starting_date", "end_date", "request_type", "timing"
            ).eq("application_id", sent_id).execute()

            employee_id_data = employee_id_response.data
            request_type = employee_id_data[0]["request_type"]
            staff_id = employee_id_data[0]["staff_id"]
            timing = employee_id_data[0]["timing"]

            if request_type == "recurring":
                starting_date = employee_id_data[0]["starting_date"]
                end_date = employee_id_data[0]["end_date"]
                dates_between = get_matching_weekday_dates(starting_date, end_date)

                for date in dates_between:
                    date = datetime.strptime(date, "%Y-%m-%d")
                    day = date.weekday()
                    weekDaysMapping = (
                        "monday", "tuesday", "wednesday", "thursday",
                        "friday", "saturday", "sunday"
                    )
                    schedule_response = supabase.table("schedule").update(
                        {weekDaysMapping[day]: timing}
                    ).lte('starting_date', date).gte("end_date", date).eq("staff_id", staff_id).execute()

            elif request_type == "ad_hoc":
                adhoc_date = employee_id_data[0]["starting_date"]
                adhoc_date = datetime.strptime(adhoc_date, "%Y-%m-%d")
                adhoc_day = adhoc_date.weekday()
                weekDaysMapping = (
                    "monday", "tuesday", "wednesday", "thursday",
                    "friday", "saturday", "sunday"
                )
                schedule_response = supabase.table("schedule").update(
                    {weekDaysMapping[adhoc_day]: timing}
                ).lte('starting_date', adhoc_date).gte("end_date", adhoc_date).eq("staff_id", staff_id).execute()

            return {"update database": "success"}, 200

        elif sent_outcome == "rejected":
            # Update application table with rejection
            application_response = supabase.table("application").update(
                {"status": "rejected", "outcome_reason": outcome_reason}
            ).eq("application_id", sent_id).execute()

            return {"update database": "success"}, 200

        else:
            return {"update database": "outcome not recognized"}, 404

    except Exception as e:
        return {"info": repr(e)}, 500



def get_current_manpower(date, test_manager_id):
   date_obj = datetime.strptime(date, "%Y-%m-%d")
   day_of_week = date_obj.strftime("%A").lower()
   try:
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
@application.route("/get_all_requests_staff", methods=['POST'])   
def get_all_requests_staff():
   #test_staff_id = 140003
   json_sent = request.get_json()
   test_staff_id = json_sent['staff_id']
   try:
     
     application_response = supabase.table("application").select("*").eq("staff_id", test_staff_id).execute()
     data = application_response.data
     for item in data:
         created_at_datetime = datetime.fromisoformat(item["created_at"])
         item["created_at"] = created_at_datetime.strftime("%Y-%m-%d")

     for item in data:
        starting_date = item["starting_date"]
        current_date = datetime.now().strftime("%Y-%m-%d")
        condition = validate_date_range(starting_date, current_date)
        item["validity_of_withdrawal"] = condition
     sorted_data = sorted(data, key=lambda x: datetime.fromisoformat(x["created_at"]))
     result_dict = {item["application_id"]: {key: value for key, value in item.items()} for item in data}
     for item in result_dict.values():
       item.pop("application_id", None)
     return result_dict,200
   except Exception as e:
      return {"info": repr(e),"traceback": traceback.format_exc()}, 500


def validate_date_range(date1: str, date2: str) -> str:
    # Convert strings to datetime objects
    date_format = "%Y-%m-%d"
    d1 = datetime.strptime(date1, date_format)
    d2 = datetime.strptime(date2, date_format)
    
   
    lower_bound = d1 - timedelta(weeks=2)
    upper_bound = d1 + timedelta(weeks=2)
    

    if lower_bound <= d2 <= upper_bound:
        return "valid"
    else:
        return "invalid"

