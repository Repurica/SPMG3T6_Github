import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
import sys

# adding Folder_2 to the system path
sys.path.insert(0, 'C:\wamp64\www\SPMG3T6_Github\\backend')
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

@pytest.fixture
def mock_validate_date_range(mocker):
    return mocker.patch('application.validate_date_range')

def test_get_all_requests_staff_valid(client, mock_supabase, mock_validate_date_range):
    test_staff_id = 140002
    request_data = {"staff_id": test_staff_id}

    # Mock Supabase application response
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
        {
            "application_id": 2,
            "created_at": "2024-10-12",
            "end_date": None,
            "outcome_reason": None,
            "reason": "test1",
            "request_type": "ad_hoc",
            "staff_id": 140002,
            "starting_date": "2024-10-09",
            "status": "pending",
            "timing": "PM",
            "validity_of_withdrawal": "valid"
        },
        {    
            "application_id": 2,
            "created_at": "2024-10-12",
            "end_date": None,
            "outcome_reason": None,
            "reason": "test1",
            "request_type": "ad_hoc",
            "staff_id": 140002,
            "starting_date": "2024-10-09",
            "status": "pending",
            "timing": "PM",
            "validity_of_withdrawal": "valid"
        },
    ]
    
    # Mock validate_date_range response
    mock_validate_date_range.return_value = True

    # Make POST request to the route
    response = client.post("/get_all_requests_staff", json=request_data)
    
    # Assert response
    assert response.status_code == 200
    response_json = response.get_json()
    
    # Check that data is correctly formatted and sorted by created_at
    assert "2" in response_json
    assert response_json["1"]["created_at"] == "2024-10-10"
    assert response_json["1"]["validity_of_withdrawal"] is True
    assert "3" in response_json
    assert response_json["2"]["created_at"] == "2024-10-09"

# Negative Path - No applications found for the staff
def test_get_all_requests_staff_no_applications(client, mock_supabase, mock_validate_date_range):
    test_staff_id = 999999
    request_data = {"staff_id": test_staff_id}
    
    # Mock empty response from Supabase
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []
    
    # Make POST request to the route
    response = client.post("/get_all_requests_staff", json=request_data)
    
    # Assert response
    assert response.status_code == 200
    response_json = response.get_json()
    assert response_json == {}  

# Boundary Test - Application date in the past, invalid withdrawal condition
def test_get_all_requests_staff_invalid_withdrawal(client, mock_supabase, mock_validate_date_range):
    test_staff_id = 140002
    request_data = {"staff_id": test_staff_id}
    
   
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
        {
            "application_id": 1,
            "staff_id": test_staff_id,
            "created_at": "2024-10-10T10:00:00",
            "starting_date": "2024-09-15",
        }
    ]
    
    # Mock validate_date_range to return False (invalid withdrawal)
    mock_validate_date_range.return_value = False

   
    response = client.post("/get_all_requests_staff", json=request_data)
    

    assert response.status_code == 200
    response_json = response.get_json()
    
    assert "1" in response_json
    assert response_json["1"]["created_at"] == "2024-10-10"
    assert response_json["1"]["validity_of_withdrawal"] is False


def test_get_all_requests_staff_invalid_json(client, mock_supabase):
    # Sending an invalid JSON (missing staff_id)
    invalid_request_data = {}
    
    # Make POST request to the route
    response = client.post("/get_all_requests_staff", json=invalid_request_data)
    
    # Assert response
    assert response.status_code == 500
    response_json = response.get_json()
    assert "info" in response_json  # Ensure exception is returned


def test_get_all_requests_staff_supabase_exception(client, mock_supabase):
    test_staff_id = 140002
    request_data = {"staff_id": test_staff_id}
    
    # Mock Supabase to throw an exception
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = Exception("Database error")
    
    # Make POST request to the route
    response = client.post("/get_all_requests_staff", json=request_data)
    
    # Assert response
    assert response.status_code == 500
    response_json = response.get_json()
    assert "info" in response_json
    assert "Database error" in response_json["info"]