from flask import request, Blueprint
from supabase_init import supabase
import traceback
from datetime import datetime, timedelta, date
import logging
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
   # json_sent should be in the form of {"staff_id": 140002}
   staff_id = json_sent["staff_id"]
   # extract from supabase the dates where the staff is WFH
   results = []
   # Looping through 
   try:
      data_returned= supabase.table("application").select("timing","applied_dates","request_type").eq("staff_id", staff_id).neq("status","rejected").execute().data
      for record in data_returned:
         applied_dates = record["applied_dates"]["dates"]
         for date in applied_dates:
            results.append({"date": date, "wfh_timing": record["timing"]})

      return {"results": results}, 200
   except Exception as e:
      return {"results": results,
            "info": repr(e)}, 500





@application.route('/store_application', methods=['POST'])
def store_application():
   json_sent = request.get_json()

   try:
      # toSend = { 
      #     "request_type" : selection,
      #     "starting_date" : startDate.toLocaleDateString("en-CA"), // yyyy-mm-dd format
      #     "end_date" : endDate.toLocaleDateString("en-CA"),
      #     "reason" : reason,
      #     "timing" : timing,
      #     "staff_id" : staffId,
      #  } 
      count_records = supabase.table("application").select("*", count="exact").execute()
      json_sent["application_id"] = count_records.count + 1
      json_sent["status"] = "pending"
      if json_sent["request_type"] == "recurring":
         json_sent["applied_dates"] = {"dates": get_matching_weekday_dates(json_sent["starting_date"], json_sent["end_date"])}
      elif json_sent["request_type"] == "ad_hoc":
         json_sent["applied_dates"] = {"dates": [json_sent["starting_date"]]}
      
      response = supabase.table("application").insert(json_sent).execute()
      # if response and response.data:
      return {"count": count_records.count, "status": "success"}, 200
      # else:
      #    return {"status": "error", "message": "could not insert into database"}, 404
   except Exception as e:
      return {"info": repr(e)}, 500





@application.route('/retrieve_pending_requests', methods=['POST'])
def retrieve_pending_requests():
   json_sent = request.get_json()
   # print(json_sent["manager_id"])
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
         timing = record["timing"]
         
         # print(request_type,timing)
         if request_type == "recurring":
            dates_between = get_matching_weekday_dates(starting_date, end_date) # eg. [2024-10-08, 2024-10-15, 2024-10-22]
            if timing == "AM":
               for date in dates_between:
                 response = get_current_manpower_AM(date, json_sent["manager_id"])
                 if response[0]["status_AM"] == "invalid":
                   record["capacity"] = "invalid"
                   break
                 
               record["capacity"] = "valid"
            
            elif timing == "PM":
               for date in dates_between:
                 response= get_current_manpower_PM(date, json_sent["manager_id"])
                 if response[0]["status_PM"] == "invalid":
                   record["capacity"] = "invalid"
                   break
               record["capacity"] = "valid"
            else:
               for date in dates_between:
                 response= get_current_manpower_whole_day(date, json_sent["manager_id"])
                 if response[0]["status_whole_day"] == "invalid":
                   record["capacity"] = "invalid"
                   break
               record["capacity"] = "valid"

         elif request_type == "ad_hoc":
            if timing == "AM":
                 response= get_current_manpower_AM(starting_date, json_sent["manager_id"])
                 print(response)
                 if response[0]["status_AM"] == "invalid":
                   record["capacity"] = "invalid"
                 else:
                   record["capacity"] = "valid"
            
            elif timing == "PM":
                 response= get_current_manpower_PM(starting_date, json_sent["manager_id"])
                 if response[0]["status_PM"] == "invalid":
                   record["capacity"] = "invalid"
                 else:
                   record["capacity"] = "valid"
            else:
                 response = get_current_manpower_whole_day(starting_date, json_sent["manager_id"])
                 if response[0]["status_whole_day"] == "invalid":
                   record["capacity"] = "invalid"
                 else:
                   record["capacity"] = "valid"

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



def get_current_manpower_AM(date, test_manager_id):

   try:
      date_obj = datetime.strptime(date, "%Y-%m-%d")
      day_of_week = date_obj.strftime("%A").lower()
      response_employee = supabase.table("employee").select("staff_id", "staff_fname", "staff_lname").eq("reporting_manager", test_manager_id).execute()
      list_of_staff_ids = []
      for staff_id_dict in response_employee.data:
         list_of_staff_ids.append(staff_id_dict["staff_id"])
      # print(list_of_staff_ids)
      am_counter = len(supabase.table("schedule").select('*').lte('starting_date', date).gte("end_date", date).eq(day_of_week, "AM").in_("staff_id", list_of_staff_ids).execute().data)
      # pm_counter = len(supabase.table("schedule").select('*').lte('starting_date', date).gte("end_date", date).eq(day_of_week, "PM").in_("staff_id", list_of_staff_ids).execute().data)
      full_day_counter = len(supabase.table("schedule").select('*').lte('starting_date', date).gte("end_date", date).eq(day_of_week, "full_day").in_("staff_id", list_of_staff_ids).execute().data)
      max_capacity = len(list_of_staff_ids)
      percentage_capacity = (am_counter + full_day_counter+1)/max_capacity
      print(percentage_capacity)
      if percentage_capacity >= 0.5:
         return {"status_AM": "invalid"}, 200
      return {"status_AM": "valid"}, 200
   
     
   except Exception as e:
        return {"info": repr(e)}, 500
   

def get_current_manpower_PM(date, test_manager_id):
   try:
      date_obj = datetime.strptime(date, "%Y-%m-%d")
      day_of_week = date_obj.strftime("%A").lower()
      response_employee = supabase.table("employee").select("staff_id", "staff_fname", "staff_lname").eq("reporting_manager", test_manager_id).execute()
      list_of_staff_ids = []
      for staff_id_dict in response_employee.data:
         list_of_staff_ids.append(staff_id_dict["staff_id"])
      # print(list_of_staff_ids)
      # am_counter = len(supabase.table("schedule").select('*').lte('starting_date', date).gte("end_date", date).eq(day_of_week, "AM").in_("staff_id", list_of_staff_ids).execute().data)
      pm_counter = len(supabase.table("schedule").select('*').lte('starting_date', date).gte("end_date", date).eq(day_of_week, "PM").in_("staff_id", list_of_staff_ids).execute().data)
      full_day_counter = len(supabase.table("schedule").select('*').lte('starting_date', date).gte("end_date", date).eq(day_of_week, "full_day").in_("staff_id", list_of_staff_ids).execute().data)
      max_capacity = len(list_of_staff_ids)
      percentage_capacity = (pm_counter + full_day_counter+1)/max_capacity
      if percentage_capacity >= 0.5:
         return {"status_PM": "invalid"}, 200
      return {"status_PM": "valid"}, 200
   
     
   except Exception as e:
        return {"info": repr(e)}, 500
   



#create AM counter and PM counter
# for each am add +1 to am, pm also same then full day add +1 to both (how many ppl not in office)

def get_current_manpower_whole_day(date, test_manager_id):
   try:
      
      date_obj = datetime.strptime(date, "%Y-%m-%d")
      day_of_week = date_obj.strftime("%A").lower()
      response_employee = supabase.table("employee").select("staff_id", "staff_fname", "staff_lname").eq("reporting_manager", test_manager_id).execute()
      list_of_staff_ids = []
      for staff_id_dict in response_employee.data:
         list_of_staff_ids.append(staff_id_dict["staff_id"])

      counter = len(supabase.table("schedule").select('*').lte('starting_date', date).gte("end_date", date).neq(day_of_week, "in_office").in_("staff_id", list_of_staff_ids).execute().data)
      max_capacity = len(list_of_staff_ids)
      percentage_capacity = (counter+1)/max_capacity
      if percentage_capacity >= 0.5:
         return {"status_whole_day": "invalid"}, 200
      return {"status_whole_day": "valid"}, 200
   
     
   except Exception as e:
        return {"info": repr(e)}, 500
   



@application.route("/get_all_requests_staff", methods=['POST'])
def get_all_requests_staff():
    # json is in the form of {"staff_id": 140002}
    json_sent = request.get_json()
    staff_id = json_sent['staff_id']
    try:
        application_response = supabase.table("application").select("*").eq("staff_id", staff_id).execute()
        data = application_response.data

        for item in data:
            try:
                try:
                    created_at_datetime = datetime.strptime(item["created_at"], "%Y-%m-%d %H:%M:%S.%f")
                except ValueError:
                    created_at_datetime = datetime.fromisoformat(item["created_at"])
                item["created_at"] = created_at_datetime.strftime("%Y-%m-%d")
            except Exception as e:
                item["created_at"] = "Invalid date"
                logging.error(f"Error parsing created_at for item {item}: {e}")

        for item in data:
            try:
                starting_date = item["starting_date"]
                current_date = datetime.now().strftime("%Y-%m-%d")
                condition = validate_date_range(starting_date, current_date)
                item["validity_of_withdrawal"] = condition
            except Exception as e:
                item["validity_of_withdrawal"] = "Error"
                logging.error(f"Error validating date range for item {item}: {e}")

        sorted_data = sorted(data, key=lambda x: datetime.strptime(x["created_at"], "%Y-%m-%d") if x["created_at"] != "Invalid date" else datetime.min)
        result_dict = {item["application_id"]: {key: value for key, value in item.items()} for item in sorted_data}
        
        # Get pending withdrawal dates
        
        for item in result_dict.values():
            application_id = item["application_id"]
            pending_withdrawal_date_list = []
            withdrawal_response = supabase.table("withdrawals").select("withdrawn_dates").eq("withdrawal_status", "pending").eq("application_id", application_id).execute().data
            for record in withdrawal_response:
               for date in record["withdrawn_dates"]["dates"]:
                 pending_withdrawal_date_list.append(date)
            item["pending_withdrawal_dates"] = pending_withdrawal_date_list
            item.pop("application_id", None)

        return result_dict, 200
    except Exception as e:
        logging.error(f"Error in get_all_requests_staff: {e}")
        return {"info": repr(e), "traceback": traceback.format_exc()}, 500




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
    
@application.route('/test', methods=['GET'])
def test():
   my_list = []
   withdrawal_response = supabase.table("withdrawals").select("withdrawn_dates").eq("withdrawal_status", "pending").eq("application_id", 4).execute().data
   for record in withdrawal_response:
      for date in record["withdrawn_dates"]["dates"]:
         my_list.append(date)
   print(my_list)
      
   return {"results":my_list}, 200


   
