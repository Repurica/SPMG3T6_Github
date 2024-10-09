from flask import Flask,request
from supabase_init import supabase
from flask_cors import CORS
app = Flask(__name__)
from datetime import datetime, timedelta,date
CORS(app)
#helper function to get_dates_between_2_dates
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



@app.route('/application/available_dates',methods=['POST'])
#function that returns all dates at which requests have already been made
def return_available_dates():
    json_sent = request.get_json()
    # staff id comes in from front-end, so staff_id is hardcoded for now
    staff_id = json_sent["staff_id"]
    # extract from supabase the dates where the staff is WFH
    results = []
    #looping through 
    try:
      data_recurring = supabase.table("application").select("starting_date","end_date","timing").eq("staff_id",staff_id).eq("request_type","recurring").execute()
      data_ad_hoc= supabase.table("application").select("starting_date","timing").eq("staff_id",staff_id).eq("request_type","ad_hoc").execute() 
      adhoc_results = data_ad_hoc.data   
      recurring_results = data_recurring.data
      results = []
      for result in recurring_results:
        start_date = result["starting_date"]
        end_date = result["end_date"]
        wfh_timing = result["timing"]
        dates_list = get_dates_on_same_weekday(start_date,end_date)
        print(dates_list)
        for date in dates_list:
            results.append({"date" : date.strftime("%Y-%m-%d"),
                            "wfh_timing" : wfh_timing})
    # print(results)
      for result2 in adhoc_results:
        start_date = result2["starting_date"]
        wfh_timing_adhoc = result2["timing"]
        results.append({"date" : start_date, "wfh_timing": wfh_timing_adhoc})
      return {"results": results}, 200
    except Exception as e:
       return {"results":results,
               "info" : repr(e)}, 500


@app.route('/application/store_application',methods=['POST'])
def store_application():
    json_sent = request.get_json()

    try:
         count_records = supabase.from_("application").select("*", count="exact").execute()
         json_sent["application_id"] = count_records.count + 1
         json_sent["status"] = "pending"
         response = supabase.table("application").insert(json_sent).execute()
         if response and response.data:
           return {"count" : count_records.count,"status": "success"},200
         else:
           return {"status" : "error", "message" : "could not insert into database"},404
    except Exception as e:
        return {"info" : repr(e)}, 500



@app.route('/application/retrieve_pending_requests')
def retrieve_pending_requests():
   test_manager_id = 140894

   try:
     response_employee = supabase.table("employee").select("staff_id","staff_fname","staff_lname").eq("reporting_manager",test_manager_id).execute()
     list_of_staff_ids = []
     dict_staff_ids_names = {}
    
     for staff_id_dict in response_employee.data:
        list_of_staff_ids.append(staff_id_dict["staff_id"])
     for staff_id_dict in response_employee.data:
        dict_staff_ids_names[staff_id_dict["staff_id"]] = staff_id_dict["staff_fname"] + " " + staff_id_dict["staff_lname"]
        
     response_application = supabase.table("application").select("application_id","staff_id","created_at","starting_date","end_date","timing","request_type","reason").in_("staff_id",list_of_staff_ids).eq("status","pending").execute()
     returned_result = response_application.data
    #  print(dict_staff_ids_names)
     for record in returned_result:
        record_staff_id = record["staff_id"]
        record["staff_fullname"] = dict_staff_ids_names[record_staff_id]

     sorted_data = sorted(returned_result, key=lambda x: datetime.fromisoformat(x["created_at"]))
     for item in sorted_data:
      created_at_datetime = datetime.fromisoformat(item["created_at"])
      item["created_at"] = created_at_datetime.strftime("%Y-%m-%d")

     result_dict = {item["application_id"]: {key: value for key, value in item.items()} for item in sorted_data}
     return result_dict,200


   except Exception as e:
        return {"info" : repr(e)}, 500



@app.route("/application/specific_request")
def request_details():
   test_request_id = 1
   try:
     

     
     response_application = supabase.table("application").select("reason","staff_id","created_at","starting_date","end_date","timing","request_type").eq("application_id",test_request_id).execute()
     application_data = response_application.data
     staff_id = response_application.data[0]["staff_id"]
     employee_response = supabase.table("employee").select("staff_fname","staff_lname").eq("staff_id",staff_id).execute()
     employee_data = employee_response.data
     returned_data = response_application.data
     returned_data[0]["employee_fullname"] = employee_data[0]["staff_fname"] + " " + employee_data[0]["staff_lname"]

     return returned_data,200
   except Exception as e:
      return {"info" : repr(e)}, 500
   
  
@app.route("/application/store_approval_rejection")
def store_approval_rejection():
   sent_info = {
      "id" : 1,
      "outcome":"approved"
   }
   try:
    sent_id = sent_info["id"]
    sent_outcome = sent_info["outcome"]
    if sent_outcome == "approved":
       application_response = supabase.table("application").update({"status": "approved"}).eq("application_id", sent_id).execute()
       return {"update database":"success"},200
    elif sent_outcome == "rejected":
       application_response = supabase.table("application").update({"status": "rejected"}).eq("application_id", sent_id).execute()
       return {"update database":"success"},200
    else:
       return {"update database":"succeeded but outcome is neither rejected or approved"},404
   except Exception as e:
      return {"info" : repr(e)}, 500
   
@app.route("/application/current_manpower_team")
def get_current_manpower():
   today = date.today()
   print(today)
   current_day_of_week = datetime.now().strftime('%A').lower()
   current_day_of_week = current_day_of_week.lower()
   print(current_day_of_week)
   test_manager_id = 140894
   try:
     
     response_employee = supabase.table("employee").select("staff_id","staff_fname","staff_lname").eq("reporting_manager",test_manager_id).execute()
     list_of_staff_ids = []
    
     for staff_id_dict in response_employee.data:
        list_of_staff_ids.append(staff_id_dict["staff_id"])
     print(list_of_staff_ids)
     schedule_response = supabase.table("schedule").select('*').lte('starting_date', today).gte("end_date", today).eq(current_day_of_week,"in_office").in_("staff_id",list_of_staff_ids).execute()
     count_in_office = len(schedule_response.data) - 1
     max_capacity_response = supabase.table("schedule").select('*').lte('starting_date', today).gte("end_date", today).in_("staff_id",list_of_staff_ids).execute()
     max_capacity = len(max_capacity_response.data)
     percentage_capacity = count_in_office/max_capacity*100
     formatted_capacity = round(percentage_capacity, 2)  
     return {"percentage_capacity": formatted_capacity},200
   
   except Exception as e:
      return {"info" : repr(e)}, 500

      
  
      

   







if __name__ == "__main__":
    app.run(debug=True, port=5000)