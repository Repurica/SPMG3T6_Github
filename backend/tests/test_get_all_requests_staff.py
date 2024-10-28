import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# adding Folder_2 to the system path
# sys.path.insert(0, 'C:\wamp64\www\SPMG3T6_Github\\backend')
from application import application, validate_date_range
from app import app
from datetime import datetime, timedelta

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(application)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('application.supabase')
@patch('application.validate_date_range')
def test_get_all_requests_staff_success(mock_validate_date_range, mock_supabase, client):
    # Mock application data returned by Supabase
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
        {
            "application_id": 2,
            "staff_id": 140002,
            "created_at": "2024-10-12T00:00:00",
            "starting_date": "2024-10-09",
            "request_type": "ad_hoc",
            "timing": "AM",
            "reason": "test reason 3",
            "status": "pending",
            "applied_dates": {"dates": ["2024-10-09"]}
        },
        # Additional mock entries as needed...
    ]
    mock_validate_date_range.return_value = "invalid"

    # Mock withdrawal dates
    mock_supabase.table.return_value.select.return_value.eq.return_value.eq.return_value.execute.return_value.data = [
        {"withdrawn_dates": {"dates": ["2024-10-09"]}}
    ]

    # Call the route and check response structure
    response = client.post('/get_all_requests_staff', json={"staff_id": 140002})
    
    assert response.status_code == 200
    response_data = response.json
    
    # Check individual application data including `pending_withdrawal_dates`
    assert "2" in response_data
    application = response_data["2"]
    assert application["created_at"] == "2024-10-12"
    assert application["starting_date"] == "2024-10-09"
    assert application["validity_of_withdrawal"] == "invalid"
    assert application["pending_withdrawal_dates"] == ["2024-10-09"]

@patch('application.supabase')
@patch('application.validate_date_range')
def test_get_all_requests_staff_no_data(mock_validate_date_range, mock_supabase, client):
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []
    mock_validate_date_range.return_value = True

    response = client.post('/get_all_requests_staff', json={"staff_id": 140002})

    assert response.status_code == 200
    assert response.json == {}

@patch('application.supabase')
@patch('application.validate_date_range')
def test_get_all_requests_staff_exception(mock_validate_date_range, mock_supabase, client):
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = Exception("Database error")
    mock_validate_date_range.return_value = True

    response = client.post('/get_all_requests_staff', json={"staff_id": 140002})

    assert response.status_code == 500
    assert "info" in response.json
    assert response.json["info"] == "Exception('Database error')"

def test_validate_date_range_within_range():
    date1 = "2023-10-01"
    date2 = (datetime.strptime(date1, "%Y-%m-%d") + timedelta(days=10)).strftime("%Y-%m-%d")
    result = validate_date_range(date1, date2)
    assert result == "valid"

def test_validate_date_range_exact_lower_bound():
    date1 = "2023-10-01"
    date2 = (datetime.strptime(date1, "%Y-%m-%d") - timedelta(weeks=2)).strftime("%Y-%m-%d")
    result = validate_date_range(date1, date2)
    assert result == "valid"

def test_validate_date_range_exact_upper_bound():
    date1 = "2023-10-01"
    date2 = (datetime.strptime(date1, "%Y-%m-%d") + timedelta(weeks=2)).strftime("%Y-%m-%d")
    result = validate_date_range(date1, date2)
    assert result == "valid"

def test_validate_date_range_below_lower_bound():
    date1 = "2023-10-01"
    date2 = (datetime.strptime(date1, "%Y-%m-%d") - timedelta(weeks=2, days=1)).strftime("%Y-%m-%d")
    result = validate_date_range(date1, date2)
    assert result == "invalid"

def test_validate_date_range_above_upper_bound():
    date1 = "2023-10-01"
    date2 = (datetime.strptime(date1, "%Y-%m-%d") + timedelta(weeks=2, days=1)).strftime("%Y-%m-%d")
    result = validate_date_range(date1, date2)
    assert result == "invalid"

def test_validate_date_range_same_day():
    date1 = "2023-10-01"
    date2 = "2023-10-01"
    result = validate_date_range(date1, date2)
    assert result == "valid"