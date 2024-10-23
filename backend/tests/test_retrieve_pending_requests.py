import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
def test_retrieve_pending_requests_no_data(mock_supabase, client):
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []
    response = client.post('/retrieve_pending_requests', json={"manager_id": 1})
    assert response.status_code == 200
    assert isinstance(response.json, dict)
    assert response.json == {}

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