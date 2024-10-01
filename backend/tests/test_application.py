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


@patch("application.supabase")
def test_store_application_success(mock_supabase, client):
    
    mock_count_response = MagicMock()
    mock_count_response.count = 5
    mock_supabase.from_.return_value.select.return_value.execute.return_value = mock_count_response

   
    mock_insert_response = MagicMock()
    mock_insert_response.data = {"id": 5}
    mock_supabase.table.return_value.insert.return_value.execute.return_value = mock_insert_response


    response = client.get('/application/store_application')

    # Verify the response
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["count"] == 5
    assert json_data["status"] == "success"

@patch("application.supabase")
def test_store_application_insert_failure(mock_supabase, client):
   
    mock_count_response = MagicMock()
    mock_count_response.count = 5
    mock_supabase.from_.return_value.select.return_value.execute.return_value = mock_count_response

    
    mock_insert_response = MagicMock()
    mock_insert_response.data = None
    mock_supabase.table.return_value.insert.return_value.execute.return_value = mock_insert_response

    # Simulate a GET request to the route
    response = client.get('/application/store_application')

    # Verify the response
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data["status"] == "error"
    assert json_data["message"] == "could not insert into database"



@patch("application.supabase")
def test_store_application_exception(mock_supabase, client):
    # Mock an exception during the process
    mock_supabase.from_.return_value.select.side_effect = Exception("DB Error")

    # Simulate a GET request to the route
    response = client.get('/application/store_application')

    # Verify the response
    assert response.status_code == 500
    json_data = response.get_json()
    assert "DB Error" in json_data["info"]