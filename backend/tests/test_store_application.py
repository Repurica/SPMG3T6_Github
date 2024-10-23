import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from application import application
from datetime import datetime

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(application)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('application.supabase')
def test_store_application_recurring(mock_supabase, client):
    mock_supabase.table.return_value.select.return_value.execute.return_value.count = 5
    mock_supabase.table.return_value.insert.return_value.execute.return_value = MagicMock()

    response = client.post('/store_application', json={
        "request_type": "recurring",
        "starting_date": "2024-10-07",
        "end_date": "2024-10-11",
        "reason": "Test reason",
        "timing": "AM",
        "staff_id": 140002
    })

    assert response.status_code == 200
    assert response.json == {"count": 5, "status": "success"}

@patch('application.supabase')
def test_store_application_ad_hoc(mock_supabase, client):
    mock_supabase.table.return_value.select.return_value.execute.return_value.count = 5
    mock_supabase.table.return_value.insert.return_value.execute.return_value = MagicMock()

    response = client.post('/store_application', json={
        "request_type": "ad_hoc",
        "starting_date": "2024-10-07",
        "end_date": "2024-10-07",
        "reason": "Test reason",
        "timing": "AM",
        "staff_id": 140002
    })

    assert response.status_code == 200
    assert response.json == {"count": 5, "status": "success"}

@patch('application.supabase')
def test_store_application_exception(mock_supabase, client):
    mock_supabase.table.return_value.select.return_value.execute.side_effect = Exception("Database error")

    response = client.post('/store_application', json={
        "request_type": "recurring",
        "starting_date": "2024-10-07",
        "end_date": "2024-10-11",
        "reason": "Test reason",
        "timing": "AM",
        "staff_id": 140002
    })

    assert response.status_code == 500
    assert "info" in response.json
    assert response.json["info"] == "Exception('Database error')"

