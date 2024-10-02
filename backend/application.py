from flask import Flask,request
from supabase_init import supabase
from flask_cors import CORS
app = Flask(__name__)
from datetime import datetime, timedelta
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


   







if __name__ == "__main__":
    app.run(debug=True, port=5000)