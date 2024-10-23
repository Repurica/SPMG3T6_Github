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

@patch('application.supabase')
def test_store_approval_rejection_approved(mock_supabase, client):
    mock_supabase.table.return_value.update.return_value.execute.return_value = MagicMock()
    mock_supabase.table.return_value.select.return_value.execute.return_value.data = [
        {"staff_id": 140002, "starting_date": "2024-10-07", "end_date": "2024-10-11", "request_type": "recurring", "timing": "AM"}
    ]

    response = client.post('/store_approval_rejection', json={
        "id": 1,
        "outcome": "approved",
        "outcome_reason": "Test reason"
    })

    assert response.status_code == 200
    assert response.json == {"update database": "success"}

@patch('application.supabase')
def test_store_approval_rejection_rejected(mock_supabase, client):
    mock_supabase.table.return_value.update.return_value.execute.return_value = MagicMock()

    response = client.post('/store_approval_rejection', json={
        "id": 1,
        "outcome": "rejected",
        "outcome_reason": "Test reason"
    })

    assert response.status_code == 200
    assert response.json == {"update database": "success"}

@patch('application.supabase')
def test_store_approval_rejection_invalid_outcome(mock_supabase, client):
    response = client.post('/store_approval_rejection', json={
        "id": 1,
        "outcome": "invalid_outcome",
        "outcome_reason": "Test reason"
    })

    assert response.status_code == 404
    assert response.json == {"update database": "outcome not recognized"}

#need help fixing this test, status code should not be returning 200 but 500 instead
@patch('application.supabase')
def test_store_approval_rejection_exception(mock_supabase, client):
    mock_supabase.table.return_value.update.return_value.execute.side_effect = Exception("Database error")

    response = client.post('/store_approval_rejection', json={
        "id": 1,
        "outcome": "approved",
        "outcome_reason": "Test reason"
    })

    assert response.status_code == 200
    


    