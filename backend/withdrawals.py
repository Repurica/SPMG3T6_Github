from flask import request, Blueprint, jsonify
from supabase_init import supabase
import traceback
from datetime import datetime, timedelta, date

withdrawals = Blueprint('withdrawals', __name__)

@withdrawals.route("/store_withdrawal", methods=['POST']) #tested and is working (using postman)
def staff_store_withdrawal():
   json_sent = request.get_json()
   # json_sent = {
   #    "staff_id": 140003,
   #    "application_id": 2,
   #    "reason": "withdraw reason",
   #    "status_of_request": "pending", this is the status of the wfh request, whether it is pending or approved
   #    "withdrawn_dates":{"dates":["2023-01-01","2023-01-02","2023-01-03"]}
   try:
      if json_sent["status_of_request"] == "approved":
         count = len(supabase.table("withdrawals").select("withdrawal_id").execute().data)
         staff_id = json_sent["staff_id"]
         application_id = json_sent["application_id"]
         reason = json_sent["reason"]
         withdrawal_id = count + 1
         json_stored = {"withdrawal_id": withdrawal_id, "application_id": application_id,"staff_id": staff_id, "reason": reason, "withdrawal_status": "pending","withdrawn_dates": json_sent["withdrawn_dates"]}
         response = supabase.table("withdrawals").insert(json_stored).execute()
         return {"count": count, "message": "Withdrawal request submitted successfully"}
      else:
         application_record_dates = supabase.table("application").select("applied_dates").eq("application_id", application_id).execute().data
         application_withdrawal_response = supabase.table("application").update({"status": "withdrawn"}).eq("application_id", application_id).execute()
            
         
         return {"count": count, "message": "Request has been withdrawn"}
   except Exception as e:
      traceback.print_exc()
      return {"status": "error", "message": str(e)},500


@withdrawals.route("/retrieve_withdrawals", methods=['POST']) #tested and is working (using postman)
def manager_view_withdrawals():
   # a manager id is sent in the json
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
         
      returned_result = supabase.table("withdrawals").select("withdrawal_id","application_id", "reason","withdrawn_dates").in_("staff_id", list_of_staff_ids).eq("withdrawal_status", "pending").execute().data
    
      return jsonify(returned_result), 200

   except Exception as e:
        traceback.print_exc()
        return {"status": "error", "message": str(e)},500
   
@withdrawals.route("/manager_approve_reject_withdrawal", methods=['POST'])
def store_outcome_withdrawal_manager():
   json_sent = request.get_json()
   #send withdrawal id in json {"outcome_status":"rejected","outcome_reason":"gg","withdrawal_id":1}
   #test change
   try:
      if json_sent["outcome_status"] == "rejected":
         response = supabase.table("withdrawals").update({"status": "rejected"}).eq("withdrawal_id", json_sent["withdrawal_id"]).execute()
         return {"status": "success", "message": "Withdrawal rejected successfully"}
      
      #update the status of the withdrawal request to approved
      response = supabase.table("withdrawals").update({"status": "approved","outcome_reason":json_sent["outcome_reason"]}).eq("withdrawal_id", json_sent["withdrawal_id"]).execute()
      #get the application id of the withdrawal request

      withdrawal_details = supabase.table("withdrawals").select("staff_id","application_id","applied_dates").eq("withdrawal_id", json_sent["withdrawal_id"]).execute().data

      application_id = withdrawal_details[0]["application_id"]

      applied_dates = withdrawal_details[0]["applied_dates"]["dates"]
      staff_id = withdrawal_details[0]["staff_id"]

      #select withdrawn dates of the withdrawal request
      withdrawn_dates = supabase.table("withdrawals").select("withdrawn_dates").eq("withdrawal_id", json_sent["withdrawal_id"]).execute().data[0]["withdrawn_dates"]


      #update application dates in application table
      for date in withdrawn_dates:
         if date in applied_dates:
            applied_dates.remove(date)
         date_obj = datetime.strptime(date, "%Y-%m-%d")
         day_of_week = date_obj.strftime("%A").lower()
         update_schedule = supabase.table("schedule").update({day_of_week: "in_office"}).lte("starting_date",date).gte("end_date",date).eq("staff_id", staff_id).execute()
         
      application_response = supabase.table("application").update("applied_dates",{"dates":applied_dates}).eq("application_id", application_id).execute()
      
      return {"status": "success", "message": "Withdrawal approved successfully","updated_info":application_response}
   except Exception as e:
      traceback.print_exc()
      return {"status": "error", "message": str(e)},500
   
