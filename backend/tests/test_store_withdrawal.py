import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, jsonify
import sys
import os
from withdrawals import withdrawals

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(withdrawals)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('withdrawals.supabase')
def test_staff_store_withdrawal_approved(mock_supabase, client):
    mock_supabase.table.return_value.select.return_value.execute.return_value.data = [{"withdrawal_id": 1}]
    mock_supabase.table.return_value.insert.return_value.execute.return_value = MagicMock()

    response = client.post('/staff_store_withdrawal', json={
        "staff_id": 140003,
        "application_id": 2,
        "reason": "withdraw reason",
        "status_of_request": "approved",
        "withdrawn_dates": {"dates": ["2023-01-01", "2023-01-02", "2023-01-03"]}
    })

    assert response.status_code == 200
    assert response.json == {"count": 1, "message": "Withdrawal request submitted successfully"}

@patch('withdrawals.supabase')
def test_staff_store_withdrawal_pending(mock_supabase, client):
    mock_supabase.table.return_value.select.return_value.execute.return_value.data = [{"withdrawal_id": 1}]
    mock_supabase.table.return_value.insert.return_value.execute.return_value = MagicMock()
    mock_supabase.table.return_value.update.return_value.execute.return_value = MagicMock()

    response = client.post('/staff_store_withdrawal', json={
        "staff_id": 140003,
        "application_id": 2,
        "reason": "withdraw reason",
        "status_of_request": "pending",
        "withdrawn_dates": {"dates": ["2023-01-01", "2023-01-02", "2023-01-03"]}
    })

    assert response.status_code == 200
    assert response.json == {"count": 1, "message": "Request has been withdrawn"}

#######################to check#################################

@patch('withdrawals.supabase')
def test_manager_view_withdrawals(mock_supabase, client):
    mock_supabase.table.return_value.select.return_value.execute.return_value.data = [
        {"staff_id": 140003, "staff_fname": "John", "staff_lname": "Doe"}
    ]
    mock_supabase.table.return_value.select.return_value.execute.return_value.data = [
        {"withdrawal_id": 1, "application_id": 2, "reason": "withdraw reason", "withdrawn_dates": {"dates": ["2023-01-01"]}}
    ]
    mock_supabase.table.return_value.select.return_value.execute.return_value.data = [
        {"staff_id": 140003, "timing": "9-5"}
    ]

    response = client.post('/retrieve_withdrawals', json={"manager_id": 140894})

    assert response.status_code == 200
    assert response.json == [
        {"withdrawal_id": 1, "application_id": 2, "reason": "withdraw reason", "withdrawn_dates": {"dates": ["2023-01-01"]}, "staff_name": "John Doe", "staff_id": 140003, "wfh_timing": "9-5"}
    ]

@patch('withdrawals.supabase')
def test_store_outcome_withdrawal_manager_approved(mock_supabase, client):
    mock_supabase.table.return_value.update.return_value.execute.return_value = MagicMock()
    mock_supabase.table.return_value.select.return_value.execute.return_value.data = [
        {"staff_id": 140003, "application_id": 2, "applied_dates": {"dates": ["2023-01-01", "2023-01-02", "2023-01-03"]}}
    ]
    mock_supabase.table.return_value.select.return_value.execute.return_value.data = [
        {"withdrawn_dates": ["2023-01-01", "2023-01-02", "2023-01-03"]}
    ]
    mock_supabase.table.return_value.update.return_value.execute.return_value = MagicMock()

    response = client.post('/manager_approve_reject_withdrawal', json={
        "outcome_status": "approved",
        "outcome_reason": "valid reason",
        "withdrawal_id": 1
    })

    assert response.status_code == 200
    assert response.json == {"status": "success", "message": "Withdrawal approved successfully", "updated_info": MagicMock()}

@patch('withdrawals.supabase')
def test_store_outcome_withdrawal_manager_rejected(mock_supabase, client):
    mock_supabase.table.return_value.update.return_value.execute.return_value = MagicMock()

    response = client.post('/manager_approve_reject_withdrawal', json={
        "outcome_status": "rejected",
        "outcome_reason": "invalid reason",
        "withdrawal_id": 1
    })

    assert response.status_code == 200
    assert response.json == {"status": "success", "message": "Withdrawal rejected successfully"}

@patch('withdrawals.supabase')
def test_test_endpoint(mock_supabase, client):
    mock_supabase.table.return_value.select.return_value.execute.return_value.data = [
        {"staff_id": 140003, "application_id": 2, "withdrawn_dates": {"dates": ["2023-01-01", "2023-01-02", "2023-01-03"]}}
    ]
    mock_supabase.table.return_value.select.return_value.execute.return_value.data = [
        {"applied_dates": {"dates": ["2023-01-01", "2023-01-02", "2023-01-03"]}}
    ]

    response = client.post('/test', json={})

    assert response.status_code == 200
    assert response.json == {
        "withdrawal_dates": ["2023-01-01", "2023-01-02", "2023-01-03"],
        "application_id": 2,
        "staff_id": 140003,
        "applied_dates": ["2023-01-01", "2023-01-02", "2023-01-03"]
    }
