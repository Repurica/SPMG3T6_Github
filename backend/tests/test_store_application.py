import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
import sys

# adding Folder_2 to the system path
# sys.path.insert(0, 'C:\wamp64\www\SPMG3T6_Github\\backend')
# from application import application, get_dates_on_same_weekday, get_matching_weekday_dates
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
def test_store_application_failure(mock_supabase, client):
    mock_supabase.from_.return_value.select.return_value.execute.return_value.count = 1
    mock_supabase.table.return_value.insert.return_value.execute.return_value.data = None
    response = client.post('/store_application', json={"staff_id": 1, "starting_date": "2023-01-01", "end_date": "2023-01-31", "timing": "AM"})
    assert response.status_code == 500

@patch('backend.application.supabase')
def test_store_application(mock_supabase, client):
    # Mocking select query response (indicating no existing application)
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.count = 0

    # Mocking insert response
    mock_supabase.table.return_value.insert.return_value.execute.return_value.data = True

    # Sending POST request to the endpoint with the required JSON data
    response = client.post('/store_application', json={
        "request_type":"ad_hoc",
        "staff_id": 140003,
        "starting_date": "2023-01-01",
        "end_date": "2023-01-31",
        "reason":"test12345",
        "timing": "AM",
        "status": "pending"
    })

    # Asserting that the response status code is 200
    assert response.status_code == 200

    # Asserting that the returned JSON status is 'success'
    assert response.json["status"] == "success"