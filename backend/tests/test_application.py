import pytest
from application import app
from unittest.mock import patch, MagicMock
from flask import Flask

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('application.supabase') 
def test_return_available_dates(mock_supabase, client):
    mock_recurring_data = {
        "data": [
            {"starting_date": "2024-09-01", "end_date": "2024-09-23", "timing": "AM"},
        ]
    }
    

    mock_ad_hoc_data = {
        "data": [
            {"starting_date": "2024-09-11", "timing": "PM"},
        ]
    }

 
    mock_supabase.table.return_value.select.return_value.eq.return_value.eq.return_value.execute.side_effect = [
        MagicMock(data=mock_recurring_data["data"]),
        MagicMock(data=mock_ad_hoc_data["data"])
    ]


    response = client.get('/application/available_dates')


    assert response.status_code == 200

    # Parse the JSON response
    response_json = response.get_json()


    assert "results" in response_json
    assert len(response_json["results"]) == 5

    
    assert response_json["results"][0]["date"] == "2024-09-01"  # Recurring date


    assert response_json["results"][0]["wfh_timing"] == "AM"
    assert response_json["results"][1]["wfh_timing"] == "AM"
