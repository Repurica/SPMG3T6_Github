import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, request
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from withdrawals import withdrawals

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config.update({
        "TESTING": True,
    })

    # Register the withdrawals Blueprint with the app
    app.register_blueprint(withdrawals, url_prefix="/")

    return app

@pytest.fixture
def client(app):
    return app.test_client()

# Test staff_store_withdrawal function for 'approved' case
@patch('withdrawals.supabase')  # Mock the supabase object
def test_staff_store_withdrawal_approved(mock_supabase, client):
    # Mock supabase responses
    mock_supabase.table().select().execute().data = [{'withdrawal_id': 1}]
    mock_supabase.table().insert().execute.return_value = MagicMock()

    # Call the function using the test client and send the request data
    response = client.post('/store_withdrawal', json={
        "staff_id": 140003,
        "application_id": 2,
        "reason": "withdraw reason",
        "status_of_request": "approved",
        "withdrawn_dates": {"dates": ["2023-01-01", "2023-01-02", "2023-01-03"]}
    })

    # Assertions
    assert response.status_code == 200
    assert response.json['message'] == 'Withdrawal request submitted successfully'

# Test staff_store_withdrawal function for non-approved case
@patch('withdrawals.supabase')  # Mock the supabase object
def test_staff_store_withdrawal_non_approved(mock_supabase, client):
    # Mock supabase responses for the non-approved case
    mock_supabase.table().select().eq().execute().data = [{"applied_dates": ["2023-01-01", "2023-01-02"]}]
    mock_supabase.table().update().eq().execute.return_value = MagicMock()

    # Call the function using the test client and send the request data
    response = client.post('/store_withdrawal', json={
        "staff_id": 140003,
        "application_id": 2,
        "reason": "withdraw reason",
        "status_of_request": "pending",
        "withdrawn_dates": {"dates": ["2023-01-01", "2023-01-02", "2023-01-03"]}
    })

    # Assertions
    assert response.status_code == 200
    assert response.json['message'] == 'Request has been withdrawn'

# Test manager_view_withdrawals function
@patch('withdrawals.supabase')
def test_manager_view_withdrawals(mock_supabase, client):
    # Mock supabase response
    mock_supabase.table().select().execute().data = [
        {"withdrawal_id": 1, "staff_id": 140003, "reason": "Sample reason"}
    ]

    # Call the function using the test client and send the request data
    response = client.post('/retrieve_withdrawals', json={
        "manager_id": 1001
    })

    # Assertions
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['reason'] == 'Sample reason'