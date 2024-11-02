from flask import request, Blueprint, jsonify
from supabase_init import supabase
import traceback
from datetime import datetime, timedelta, date

withdrawals = Blueprint('withdrawals', __name__)

@withdrawals.route("/staff_store_withdrawal", methods=['POST']) #tested and is working (using postman)
def staff_store_withdrawal():
   """
    This function is used to store the withdrawal request of a staff member.
    This is the example json sent to the function (for frontend's ease of use):
    json_sent = {
        "staff_id": 140003,
        "application_id": 2,
        "reason": "withdraw reason",
        "status_of_request": "pending",  # this is the status of the wfh request, whether it is pending or approved
        "withdrawn_dates": {"dates": ["2023-01-01", "2023-01-02", "2023-01-03"]}
    }
    """

   json_sent = request.get_json()
   
   try:
      #retrieve the number of withdrawal requests in the table
      count = len(supabase.table("withdrawals").select("withdrawal_id").execute().data)
      #retrieve the staff id, application id, reason, and withdrawn dates from the json sent
      staff_id = json_sent["staff_id"]
      application_id = json_sent["application_id"]
      reason = json_sent["reason"]
      withdrawal_id = count + 1
      # case where the outcome of the wfh request is approved
      if json_sent["status_of_request"] == "approved":
         #store the withdrawal request in the table
         json_stored = {"withdrawal_id": withdrawal_id, "application_id": application_id,"staff_id": staff_id, "reason": reason, "withdrawal_status": "pending","withdrawn_dates": json_sent["withdrawn_dates"]}
         response = supabase.table("withdrawals").insert(json_stored).execute()
         return {"count": count, "message": "Withdrawal request submitted successfully"}, 200
      else:
      # if the outcome of the wfh request is pending, the withdrawal request is not stored, and the withdrawn dates will be removed from the dates 
         applied_dates = supabase.table("application").select("applied_dates").eq("application_id", application_id).execute().data
         withdrawn_dates = json_sent["withdrawn_dates"]["dates"]
         for date in withdrawn_dates:
            if date in applied_dates[0]["applied_dates"]["dates"]:
               applied_dates[0]["applied_dates"]["dates"].remove(date)
         if len(applied_dates[0]["applied_dates"]["dates"]) == 0:
             #if the staff has no more applied dates, the status of the application will be set to withdrawn
            application_response = supabase.table("application").update({"status": "withdrawn","applied_dates":applied_dates[0]["applied_dates"]}).eq("application_id", application_id).execute()
            json_stored = {"withdrawal_id": withdrawal_id, "application_id": application_id,"staff_id": staff_id, "reason": reason, "withdrawal_status": "approved","withdrawn_dates": json_sent["withdrawn_dates"]}
            withdrawal_response = supabase.table("withdrawals").insert(json_stored).execute()

         else:
            #if the staff still has applied dates, the status of the WFH application itself will still be pending, but the withdrawal request will be stored as approved
            application_response = supabase.table("application").update({"applied_dates":applied_dates[0]["applied_dates"]}).eq("application_id", application_id).execute()
            json_stored = {"withdrawal_id": withdrawal_id, "application_id": application_id,"staff_id": staff_id, "reason": reason, "withdrawal_status": "approved","withdrawn_dates": json_sent["withdrawn_dates"]}
            withdrawal_response = supabase.table("withdrawals").insert(json_stored).execute()
         
         return {"count": count, "message": "Request has been withdrawn"}, 200
   except Exception as e:
      traceback.print_exc()
      return {"status": "error", "message": str(e)}, 500


@withdrawals.route("/retrieve_withdrawals", methods=['POST']) #tested and is working (using postman)
def manager_view_withdrawals():
   # a manager id is sent in the json
   json_sent = request.get_json()
   # print(json_sent["manager_id"])
   try:
      #retrieve the staff ids of the staff members who have the manager id as their reporting manager
      response_employee = supabase.table("employee").select("staff_id", "staff_fname", "staff_lname").eq("reporting_manager", json_sent["manager_id"]).execute()
      list_of_staff_ids = []
      dict_staff_ids_names = {}
      #store the staff ids and names in a dictionary
      for staff_id_dict in response_employee.data:
         list_of_staff_ids.append(staff_id_dict["staff_id"])
      for staff_id_dict in response_employee.data:
         dict_staff_ids_names[staff_id_dict["staff_id"]] = staff_id_dict["staff_fname"] + " " + staff_id_dict["staff_lname"]

      #retrieve the withdrawal requests of the staff members who have the manager id as their reporting manager, and the status of the withdrawal request is pending
      returned_result = supabase.table("withdrawals").select("withdrawal_id","application_id", "reason","withdrawn_dates").in_("staff_id", list_of_staff_ids).eq("withdrawal_status", "pending").execute().data
      
      #add the staff name, staff id, and wfh timing to the returned result
      for result in returned_result:
         result["staff_name"] = dict_staff_ids_names[supabase.table("application").select("staff_id").eq("application_id", result["application_id"]).execute().data[0]["staff_id"]]
         result["staff_id"] = supabase.table("application").select("staff_id").eq("application_id", result["application_id"]).execute().data[0]["staff_id"]
         result["wfh_timing"] = supabase.table("application").select("timing").eq("application_id", result["application_id"]).execute().data[0]["timing"]
      return jsonify(returned_result), 200

   except Exception as e:
        traceback.print_exc()
        return {"status": "error", "message": str(e)},500
   
@withdrawals.route("/manager_approve_reject_withdrawal", methods=['POST'])
def store_outcome_withdrawal_manager():
   """
    This function is used to store the outcome of the withdrawal request by the manager.
      This is the example json sent to the function (for frontend's ease of use):
      json_sent = {
            "outcome_status": "rejected",
            "outcome_reason": "gg",
            "withdrawal_id": 1
         }
    """
   json_sent = request.get_json()
   #send withdrawal id in json {"outcome_status":"rejected","outcome_reason":"gg","withdrawal_id":1}
   #test change
   try:
      #update the status of the withdrawal request to rejected (This is the case where the manager rejects the withdrawal request)
      if json_sent["outcome_status"] == "rejected":
         response = supabase.table("withdrawals").update({"withdrawal_status": "rejected","outcome_reason":json_sent["outcome_reason"]}).eq("withdrawal_id", json_sent["withdrawal_id"]).execute()
         return {"status": "success", "message": "Withdrawal rejected successfully"}
      
      #update the status of the withdrawal request to approved (This is the case where the manager approves the withdrawal request)
      response = supabase.table("withdrawals").update({"withdrawal_status": "approved","outcome_reason":json_sent["outcome_reason"]}).eq("withdrawal_id", json_sent["withdrawal_id"]).execute()
      #get the application id, staff_id, and applied_dates of the withdrawal request

      withdrawal_details = supabase.table("withdrawals").select("staff_id","application_id","withdrawn_dates").eq("withdrawal_id", json_sent["withdrawal_id"]).execute().data
      
      application_id = withdrawal_details[0]["application_id"]
      applied_dates = supabase.table("application").select("applied_dates").eq("application_id", application_id).execute().data
      applied_dates = applied_dates[0]["applied_dates"]["dates"]
      print(applied_dates)
      staff_id = withdrawal_details[0]["staff_id"]


      #select withdrawn dates of the withdrawal request
      withdrawn_dates = supabase.table("withdrawals").select("withdrawn_dates").eq("withdrawal_id", json_sent["withdrawal_id"]).execute().data[0]["withdrawn_dates"]["dates"]
      print(withdrawn_dates)

      # return {"withdrawn_dates":withdrawn_dates,"applied_dates":applied_dates["applied_dates"]["dates"]}

      #update application dates in application table
      for date in withdrawn_dates:
         
         date_obj = datetime.strptime(date, "%Y-%m-%d")
         day_of_week = date_obj.strftime("%A").lower()
         update_schedule = supabase.table("schedule").update({day_of_week: "in_office"}).lte("starting_date",date).gte("end_date",date).eq("staff_id", staff_id).execute()
         if date in applied_dates:
            applied_dates.remove(date)

      # update the applied dates of the staff member in the application table(this is the case where the staff member has no more applied dates)
      if len(applied_dates) == 0:
         application_response = supabase.table("application").update({"status": "withdrawn","applied_dates":{"dates":applied_dates}}).eq("application_id", application_id).execute()
         return {"status": "success", "message": "Withdrawal approved successfully","updated_info":application_response.data}
      
      # update the applied dates of the staff member in the application table(this is the case where the staff member still has applied dates)
      application_response = supabase.table("application").update({"applied_dates":{"dates":applied_dates}}).eq("application_id", application_id).execute()
      
      return {"status": "success", "message": "Withdrawal approved successfully","updated_info":application_response.data}
   
   
   except Exception as e:
      traceback.print_exc()
      return {"status": "error", "message": str(e)},500
   
