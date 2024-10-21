import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
import sys

# adding Folder_2 to the system path
# sys.path.insert(0, 'C:\wamp64\www\SPMG3T6_Github\\backend')
from application import application
from datetime import datetime

# Setup test client
@pytest.fixture
def client():
   app = Flask(__name__)
   app.register_blueprint(application)
   app.config['TESTING'] = True
   with app.test_client() as client:
      yield client

@pytest.fixture
def mock_supabase(mocker):
    mock_client = mocker.patch('app.supabase')  # Mock the supabase client in your app
    return mock_client


@patch('backend.application.supabase')
def test_store_approval_rejection_rejected(mock_supabase, client):
    mock_supabase.table.return_value.update.return_value.eq.return_value.execute.side_effect = Exception("error")
    response = client.post('/store_approval_rejection', json={"id": None, "outcome": "rejected", "outcome_reason": "testr"})
    assert response.status_code == 500
    assert "info" in response.json



def test_store_approval_rejection(mock_supabase, client):
    # Mocking the database calls
    mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = MagicMock()
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
        {"staff_id": 140002, "starting_date": "2024-10-07", "end_date": "2023-10-18", "request_type": "recurring", "timing": "AM", "status": "rejected", "outcome_reason": "testr"}
    ]

    # Sending the request with the correct field names
    response = client.post('/store_approval_rejection', json={"id": 1, "outcome": "rejected", "outcome_reason": "testr"})

    # Check if the response status is 200
    assert response.status_code == 200
    assert response.json["update database"] == "success"



    