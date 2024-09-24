from flask import Flask,request
from supabase_init import supabase
from flask_cors import CORS
app = Flask(__name__)
from datetime import datetime, timedelta
CORS(app)

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



@app.route('/application/available_dates',methods=['GET'])
#function that returns all dates at which requests have already been made
def return_available_dates():
    # json_sent = request.get_json()
    # staff id comes in from front-end, so staff_id is hardcoded for now
    staff_id = 140002
    staff_id_2 = 140003
    # extract from supabase the dates where the staff is WFH
    data_recurring = supabase.table("application").select("starting_date","end_date").eq("staff_id",staff_id).eq("request_type","recurring").execute()
    data_ad_hoc= supabase.table("application").select("starting_date").eq("staff_id",staff_id).eq("request_type","ad_hoc").execute() 
    adhoc_results = data_ad_hoc.data   
    recurring_results = data_recurring.data
    results = []
    print(recurring_results)
    for result in recurring_results:
        print(result)
        start_date = result["starting_date"]
        end_date = result["end_date"]
        dates_list = get_dates_on_same_weekday(start_date,end_date)
        print(dates_list)
        for date in dates_list:
            results.append(date.strftime("%Y-%m-%d"))
    # print(results)
    for result2 in adhoc_results:
        start_date = result2["starting_date"]
        results.append(start_date)
    return {"results": results}


@app.route('/application/store_application',methods=['GET'])
def store_application():
    # json_sent = request.get_json()
    json_sent = { 
   "request_type" : "recurring",
   "starting_date" : "2024-09-27",
   "end_date" : "2024-10-11",
   "reason" : "test reason",
   "timing" : "PM",
   "staff_id" : 140002
}   
    
    count_records = supabase.from_("application").select("*", count="exact").execute()
    json_sent["application_id"] = count_records.count + 1
    json_sent["status"] = "pending"
    response = supabase.table("application").insert(json_sent).execute()
    return {"count" : count_records.count}


   







if __name__ == "__main__":
    app.run(debug=True, port=5000)