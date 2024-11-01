import pytest
from unittest.mock import patch, MagicMock, Mock
from flask import Flask, jsonify
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from withdrawals import withdrawals, manager_view_withdrawals, store_outcome_withdrawal_manager
app = Flask(__name__)
@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(withdrawals)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
@pytest.fixture
def mock_supabase():
    with patch("withdrawals.supabase") as mock_supabase:
        mock_withdrawals_table = Mock()
        mock_application_table = Mock()
        mock_employee_table = Mock()
        mock_schedule_table = Mock()

        # Set up mock responses based on table name
        mock_supabase.table.side_effect = lambda table_name: {
            "withdrawals": mock_withdrawals_table,
            "application": mock_application_table,
            "employee": mock_employee_table,
            "schedule": mock_schedule_table,
        }[table_name]

        yield {
            "supabase": mock_supabase,
            "withdrawals": mock_withdrawals_table,
            "application": mock_application_table,
            "employee": mock_employee_table,
            "schedule": mock_schedule_table
        }

@patch('withdrawals.supabase')
def test_staff_store_withdrawal_approved(mock_supabase, client):
    mock_supabase.table.return_value.select.return_value.execute.return_value.data = [{"withdrawal_id": 1}]
    mock_supabase.table.return_value.insert.return_value.execute.return_value.data = []

    response = client.post('/staff_store_withdrawal', json={
        "staff_id": 140003,
        "application_id": 2,
        "reason": "withdraw reason",
        "status_of_request": "approved",
        "withdrawn_dates": {"dates": ["2023-01-01", "2023-01-02", "2023-01-03"]}
    })
    assert response.status_code == 200
    assert response.json["message"] == "Withdrawal request submitted successfully"

@patch('withdrawals.supabase')
def test_staff_store_withdrawal_pending(mock_supabase, client):
    mock_supabase.table.return_value.select.return_value.execute.return_value.data = [{"withdrawal_id": 1}]
    mock_supabase.table.return_value.update.return_value.execute.return_value.data = []
    mock_supabase.table.return_value.insert.return_value.execute.return_value.data = []

    response = client.post('/staff_store_withdrawal', json={
        "staff_id": 140003,
        "application_id": 2,
        "reason": "withdraw reason",
        "status_of_request": "pending",
        "withdrawn_dates": {"dates": ["2023-01-01", "2023-01-02", "2023-01-03"]}
    })
    assert response.status_code == 200
    assert response.json["message"] == "Request has been withdrawn"

def test_manager_view_withdrawals(mock_supabase):
    json_input = {"manager_id": 1}
    # Mock employee table response
    mock_supabase["employee"].select.return_value.eq.return_value.execute.return_value = Mock(
        data=[{"staff_id": 140003, "staff_fname": "John", "staff_lname": "Doe"}]
    )
    # Mock withdrawals table response
    mock_supabase["withdrawals"].select.return_value.in_.return_value.eq.return_value.execute.return_value = Mock(
        data=[{"withdrawal_id": 1, "application_id": 2, "reason": "test reason", "withdrawn_dates": {"dates": ["2023-01-01"]}}]
    )
    # Mock application table response
    mock_supabase["application"].select.return_value.eq.return_value.execute.return_value = Mock(
        data=[{"staff_id": 140003, "timing": "9:00 AM - 5:00 PM"}]
    )

    with app.test_request_context(json=json_input):
        with patch("flask.request.get_json", return_value=json_input):
            response, status_code = manager_view_withdrawals()

    assert status_code == 200
    assert response.json[0]["staff_name"] == "John Doe"

def test_store_outcome_withdrawal_manager(mock_supabase):
    json_input = {
        "outcome_status": "rejected",
        "outcome_reason": "test reason",
        "withdrawal_id": 1
    }
    # Mock withdrawal update response
    mock_supabase["withdrawals"].update.return_value.eq.return_value.execute.return_value = {"status": "success"}
    
    with app.test_request_context(json=json_input):
        with patch("flask.request.get_json", return_value=json_input):
            response = store_outcome_withdrawal_manager()

    assert response["status"] == "success"
    assert "Withdrawal rejected successfully" in response["message"]


def test_store_outcome_withdrawal_manager_rejection(mock_supabase):
    json_input = {
        "outcome_status": "rejected",
        "outcome_reason": "test reason",
        "withdrawal_id": 1
    }
    mock_supabase["withdrawals"].update.return_value.eq.return_value.execute.return_value = Mock(
        data={"status": "success"}
    )

    with app.test_request_context(json=json_input):
        with patch("flask.request.get_json", return_value=json_input):
            response = store_outcome_withdrawal_manager()

    assert response["status"] == "success"
    assert "Withdrawal rejected successfully" in response["message"]

def test_store_outcome_withdrawal_manager_approval_no_remaining_dates(mock_supabase):
    json_input = {
        "outcome_status": "approved",
        "outcome_reason": "approved reason",
        "withdrawal_id": 1
    }
    mock_supabase["withdrawals"].update.return_value.eq.return_value.execute.return_value = Mock(data={"status": "success"})
    mock_supabase["withdrawals"].select.return_value.eq.return_value.execute.return_value = Mock(
        data=[{"staff_id": 140003, "application_id": 2, "withdrawn_dates": {"dates": ["2023-01-01"]}}]
    )
    mock_supabase["application"].select.return_value.eq.return_value.execute.return_value = Mock(
        data=[{"applied_dates": {"dates": ["2023-01-01"]}, "status": "pending"}]
    )
    mock_supabase["schedule"].update.return_value.lte.return_value.gte.return_value.eq.return_value.execute.return_value = Mock(data={})
    mock_supabase["application"].update.return_value.eq.return_value.execute.return_value = Mock(data={"status": "withdrawn"})

    with app.test_request_context(json=json_input):
        with patch("flask.request.get_json", return_value=json_input):
            response = store_outcome_withdrawal_manager()

    assert response["status"] == "success"
    assert "Withdrawal approved successfully" in response["message"]

def test_store_outcome_withdrawal_manager_approval_with_remaining_dates(mock_supabase):
    json_input = {
        "outcome_status": "approved",
        "outcome_reason": "approved reason",
        "withdrawal_id": 1
    }
    mock_supabase["withdrawals"].update.return_value.eq.return_value.execute.return_value = Mock(data={"status": "success"})
    mock_supabase["withdrawals"].select.return_value.eq.return_value.execute.return_value = Mock(
        data=[{"staff_id": 140003, "application_id": 2, "withdrawn_dates": {"dates": ["2023-01-01"]}}]
    )
    mock_supabase["application"].select.return_value.eq.return_value.execute.return_value = Mock(
        data=[{"applied_dates": {"dates": ["2023-01-01", "2023-01-02"]}}]
    )
    mock_supabase["schedule"].update.return_value.lte.return_value.gte.return_value.eq.return_value.execute.return_value = Mock(data={})
    mock_supabase["application"].update.return_value.eq.return_value.execute.return_value = Mock(data={"status": "pending"})

    with app.test_request_context(json=json_input):
        with patch("flask.request.get_json", return_value=json_input):
            response = store_outcome_withdrawal_manager()

    assert response["status"] == "success"
    assert "Withdrawal approved successfully" in response["message"]