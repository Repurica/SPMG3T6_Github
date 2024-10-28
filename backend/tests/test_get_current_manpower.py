import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
import sys
import os
# adding Folder_2 to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from application import application, get_current_manpower_AM, get_current_manpower_PM, get_current_manpower_whole_day
from datetime import datetime

mock_date = "2023-10-01"
mock_manager_id = "test_manager_id"
mock_staff_ids = ["staff1", "staff2", "staff3"]
mock_employee_data = [{"staff_id": "staff1"}, {"staff_id": "staff2"}, {"staff_id": "staff3"}]

# Helper function to mock Supabase select query
def mock_supabase_select(result_data):
    class MockResponse:
        def __init__(self, data):
            self.data = data
    return MockResponse(result_data)

@patch("application.supabase.table")
def test_get_current_manpower_AM_valid(mock_table):
    mock_table.return_value.select.return_value.eq.return_value.execute.side_effect = [
        mock_supabase_select(mock_employee_data),  # Mock employee data
        mock_supabase_select([{}, {}]),           # Mock AM and full_day data
    ]
    
    response, status_code = get_current_manpower_AM(mock_date, mock_manager_id)
    assert status_code == 200
    assert response["status_AM"] == "valid"


@patch('application.supabase')
def test_get_current_manpower_AM_invalid(mock_supabase):
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
        {"staff_id": 1}, {"staff_id": 2}, {"staff_id": 3}
    ]
    mock_supabase.table.return_value.select.return_value.lte.return_value.gte.return_value.eq.return_value.in_.return_value.execute.side_effect = [
        MagicMock(data=[{"schedule_id": 1}, {"schedule_id": 2}, {"schedule_id": 3}]),  # AM schedules
        MagicMock(data=[{"schedule_id": 1}, {"schedule_id": 2}])  # Full day schedules
    ]

    response, status_code = get_current_manpower_AM("2024-10-07", 1)
    assert status_code == 200
    assert response["status_AM"] == "invalid"

@patch("application.supabase.table")
def test_get_current_manpower_PM_valid(mock_table):
    mock_table.return_value.select.return_value.eq.return_value.execute.side_effect = [
        mock_supabase_select(mock_employee_data),
        mock_supabase_select([{}, {}]),           # PM and full_day data within threshold
    ]
    
    response, status_code = get_current_manpower_PM(mock_date, mock_manager_id)
    assert status_code == 200
    assert response["status_PM"] == "valid"

@patch('application.supabase')
def test_get_current_manpower_PM_invalid(mock_supabase):
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
        {"staff_id": 1}, {"staff_id": 2}, {"staff_id": 3}
    ]
    mock_supabase.table.return_value.select.return_value.lte.return_value.gte.return_value.eq.return_value.in_.return_value.execute.side_effect = [
        MagicMock(data=[{"schedule_id": 1}, {"schedule_id": 2}, {"schedule_id": 3}]),  # PM schedules
        MagicMock(data=[{"schedule_id": 1}, {"schedule_id": 2}])  # Full day schedules
    ]

    response, status_code = get_current_manpower_PM("2024-10-07", 1)
    assert status_code == 200
    assert response["status_PM"] == "invalid"

@patch("application.supabase.table")
def test_get_current_manpower_whole_day_valid(mock_table):
    mock_table.return_value.select.return_value.eq.return_value.execute.side_effect = [
        mock_supabase_select(mock_employee_data),
        mock_supabase_select([{}, {}]),           # "Not in office" data within threshold
    ]
    
    response, status_code = get_current_manpower_whole_day(mock_date, mock_manager_id)
    assert status_code == 200
    assert response["status_whole_day"] == "valid"

@patch('application.supabase')
def test_get_current_manpower_whole_day_invalid(mock_supabase):
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
        {"staff_id": 1}, {"staff_id": 2}, {"staff_id": 3}
    ]
    mock_supabase.table.return_value.select.return_value.lte.return_value.gte.return_value.neq.return_value.in_.return_value.execute.return_value.data = [
        {"schedule_id": 1}, {"schedule_id": 2}, {"schedule_id": 3}
    ]

    response, status_code = get_current_manpower_whole_day("2024-10-07", 1)
    assert status_code == 200
    assert response["status_whole_day"] == "invalid"