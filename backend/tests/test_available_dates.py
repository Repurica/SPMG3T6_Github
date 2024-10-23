import pytest
from unittest.mock import patch
from flask import Flask, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from application import application

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(application)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(application)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('application.supabase')
def test_return_available_dates_success(mock_supabase, client):
    mock_supabase.table.return_value.select.return_value.eq.return_value.neq.return_value.execute.return_value.data = [
        {"timing": "AM", "applied_dates": {"dates": ["2023-01-01", "2023-01-02"]}, "request_type": "recurring"},
        {"timing": "PM", "applied_dates": {"dates": ["2023-01-03"]}, "request_type": "ad_hoc"}
    ]

    response = client.post('/available_dates', json={"staff_id": 140002})

    assert response.status_code == 200
    assert response.json == {
        "results": [
            {"date": "2023-01-01", "wfh_timing": "AM"},
            {"date": "2023-01-02", "wfh_timing": "AM"},
            {"date": "2023-01-03", "wfh_timing": "PM"}
        ]
    }

@patch('application.supabase')
def test_return_available_dates_no_data(mock_supabase, client):
    mock_supabase.table.return_value.select.return_value.eq.return_value.neq.return_value.execute.return_value.data = []

    response = client.post('/available_dates', json={"staff_id": 140002})

    assert response.status_code == 200
    assert response.json == {"results": []}

@patch('application.supabase')
def test_return_available_dates_exception(mock_supabase, client):
    mock_supabase.table.return_value.select.return_value.eq.return_value.neq.return_value.execute.side_effect = Exception("Database error")

    response = client.post('/available_dates', json={"staff_id": 140002})

    assert response.status_code == 500
    assert "info" in response.json
    assert response.json["info"] == "Exception('Database error')"

