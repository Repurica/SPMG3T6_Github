import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# adding Folder_2 to the system path
# sys.path.insert(0, 'C:\wamp64\www\SPMG3T6_Github\\backend')
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

@pytest.fixture
def mock_supabase(mocker):
    mock_client = mocker.patch('app.supabase')  # Mock the supabase client in your app
    return mock_client

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
    response = client.post('/available_dates', json={"staff_id": 140003})
    assert response.status_code == 200
    assert isinstance(response.json, dict)
    assert "results" in response.json


@patch('backend.application.supabase')
def test_return_available_dates_no_data(mock_supabase, client):
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []
    response = client.post('/available_dates', json={"staff_id": 1})
    assert response.status_code == 200
    assert isinstance(response.json, dict)
    assert response.json["results"] == []