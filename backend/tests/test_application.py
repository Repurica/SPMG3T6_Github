import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
import sys

# adding Folder_2 to the system path
sys.path.insert(0, 'C:\wamp64\www\SPMG3T6_Github\\backend')
from application import application, get_dates_on_same_weekday, get_matching_weekday_dates
from datetime import datetime

# Setup test client
@pytest.fixture
def client():
   app = Flask(__name__)
   app.register_blueprint(application)
   app.config['TESTING'] = True
   with app.test_client() as client:
      yield client

def test_get_dates_on_same_weekday():
   start_date = "2023-01-01"
   end_date = "2023-01-31"
   expected_dates = [
      datetime(2023, 1, 1),
      datetime(2023, 1, 8),
      datetime(2023, 1, 15),
      datetime(2023, 1, 22),
      datetime(2023, 1, 29)
   ]
   assert get_dates_on_same_weekday(start_date, end_date) == expected_dates

def test_get_matching_weekday_dates():
    start_date = "2023-01-01"
    end_date = "2023-01-31"
    expected_dates = [
        "2023-01-01",
        "2023-01-08",
        "2023-01-15",
        "2023-01-22",
        "2023-01-29"
    ]
    assert get_matching_weekday_dates(start_date, end_date) == expected_dates

@patch('backend.application.supabase')
def test_return_available_dates(mock_supabase, client):
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
        {"starting_date": "2023-01-01", "end_date": "2023-01-31", "timing": "AM"}
    ]
    response = client.post('/available_dates', json={"staff_id": 1})
    assert response.status_code == 200
    assert isinstance(response.json, dict)
    assert "results" in response.json



@patch('backend.application.supabase')   
def test_retrieve_pending_requests(mock_supabase, client):
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
        {"staff_id": 1400, "staff_fname": "John", "staff_lname": "Doe"}
    ]
    mock_supabase.table.return_value.select.return_value.in_.return_value.eq.return_value.execute.return_value.data = [
        {"application_id": 1, "staff_id": 1, "created_at": "2023-01-01T00:00:00", "starting_date": "2023-01-01", "end_date": "2023-01-31", "timing": "morning", "request_type": "recurring", "reason": "test"}
    ]
    response = client.post('/retrieve_pending_requests', json={"manager_id": 1})
    assert response.status_code == 200
    assert isinstance(response.json, dict)

@patch('backend.application.supabase')
def test_store_approval_rejection(mock_supabase, client):
    mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = MagicMock()
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
        {"staff_id": 1, "starting_date": "2023-01-01", "end_date": "2023-01-31", "request_type": "recurring", "timing": "morning"}
    ]
    response = client.get('/store_approval_rejection')
    assert response.status_code == 200
    assert response.json["update database"] == "success"

@patch('backend.application.supabase')
def test_return_available_dates_no_data(mock_supabase, client):
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []
    response = client.post('/available_dates', json={"staff_id": 1})
    assert response.status_code == 200
    assert isinstance(response.json, dict)
    assert response.json["results"] == []

@patch('backend.application.supabase')
def test_store_application_failure(mock_supabase, client):
    mock_supabase.from_.return_value.select.return_value.execute.return_value.count = 1
    mock_supabase.table.return_value.insert.return_value.execute.return_value.data = None
    response = client.post('/store_application', json={"staff_id": 1, "starting_date": "2023-01-01", "end_date": "2023-01-31", "timing": "morning"})
    assert response.status_code == 500

@patch('backend.application.supabase')
def test_retrieve_pending_requests_no_data(mock_supabase, client):
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []
    response = client.post('/retrieve_pending_requests', json={"manager_id": 1})
    assert response.status_code == 200
    assert isinstance(response.json, dict)
    assert response.json == {}

@patch('backend.application.supabase')
def test_store_approval_rejection(mock_supabase, client):
    mock_supabase.table.return_value.update.return_value.eq.return_value.execute.side_effect = Exception("Database error")
    response = client.get('/store_approval_rejection')
    assert response.status_code == 200
    assert "info" in response.json

@patch('backend.application.supabase')
def test_get_current_manpower_no_data(mock_supabase, client):
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []
    response = client.get('/current_manpower')
    assert response.status_code == 404


def test_get_matching_weekday_dates():
   start_date = "2023-01-01"
   end_date = "2023-01-31"
   expected_dates = [
      "2023-01-01",
      "2023-01-08",
      "2023-01-15",
      "2023-01-22",
      "2023-01-29"
   ]
   assert get_matching_weekday_dates(start_date, end_date) == expected_dates

@patch('backend.application.supabase')
def test_return_available_dates(mock_supabase, client):
   mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
      {"starting_date": "2023-01-01", "end_date": "2023-01-31", "timing": "morning"}
   ]
   response = client.post('/available_dates', json={"staff_id": 1})
   assert response.status_code == 200
   assert isinstance(response.json, dict)
   assert "results" in response.json

# @patch('backend.application.supabase')
# def test_store_application(mock_supabase, client):
#    mock_supabase.from_.return_value.select.return_value.execute.return_value.count = 1
#    mock_supabase.table.return_value.insert.return_value.execute.return_value.data = True
#    response = client.post('/store_application', json={"staff_id": 1, "starting_date": "2023-01-01", "end_date": "2023-01-31", "timing": "morning"})
#    assert response.status_code == 200
#    assert response.json["status"] == "success"

@patch('backend.application.supabase')
def test_retrieve_pending_requests(mock_supabase, client):
   mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
      {"staff_id": 1, "staff_fname": "John", "staff_lname": "Doe"}
   ]
   mock_supabase.table.return_value.select.return_value.in_.return_value.eq.return_value.execute.return_value.data = [
      {"application_id": 1, "staff_id": 1, "created_at": "2023-01-01T00:00:00", "starting_date": "2023-01-01", "end_date": "2023-01-31", "timing": "morning", "request_type": "recurring", "reason": "test"}
   ]
   response = client.post('/retrieve_pending_requests', json={"manager_id": 1})
   assert response.status_code == 200
   assert isinstance(response.json, dict)

@patch('backend.application.supabase')
def test_store_approval_rejection(mock_supabase, client):
   mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = MagicMock()
   mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
      {"staff_id": 1, "starting_date": "2023-01-01", "end_date": "2023-01-31", "request_type": "recurring", "timing": "AM"}
   ]
   response = client.get('/store_approval_rejection')
   assert response.status_code == 200
   assert response.json["update database"] == "success"