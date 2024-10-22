import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
import sys
import os
# adding Folder_2 to the system path
# sys.path.insert(0, 'C:\wamp64\www\SPMG3T6_Github\\backend')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from application import application, get_current_manpower
from datetime import datetime

# Setup test client
# @pytest.fixture
# def client():
#    app = Flask(__name__)
#    app.register_blueprint(application)
#    app.config['TESTING'] = True
#    with app.test_client() as client:
#       yield client

# @pytest.fixture
# def mock_supabase(mocker):
#     mock_client = mocker.patch('app.supabase')  # Mock the supabase client in your app
#     return mock_client


# def test_get_current_manpower_valid(mock_supabase):
#     # Test input
#     test_date = "2024-10-18"
#     test_manager_id = 140894
    
#     # Mock employee response
#     mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
#         {"staff_id": 101}, {"staff_id": 102}
#     ]
    
#     # Mock schedule responses
#     mock_supabase.table.return_value.select.return_value.lte.return_value.gte.return_value.eq.return_value.in_.return_value.execute.side_effect = [
#         MagicMock(data=[{"staff_id": 101}, {"staff_id": 102}, {"staff_id": 103}]),  
#         MagicMock(data=[{"staff_id": 101}, {"staff_id": 102}]) 
#     ]
    
#     # Expected valid status
#     response, status_code = get_current_manpower(test_date, test_manager_id)
#     assert response["status"] == "valid"
#     assert status_code == 200

# # Negative Path - No staff under the manager
# def test_get_current_manpower_no_staff(mock_supabase):
#     test_date = "2024-10-18"
#     test_manager_id = 140894
    
#     # Mock employee response - no staff
#     mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []
    
#     # Mock schedule response
#     mock_supabase.table.return_value.select.return_value.lte.return_value.gte.return_value.eq.return_value.in_.return_value.execute.return_value.data = []
    
#     # Expected invalid status due to lack of staff
#     response, status_code = get_current_manpower(test_date, test_manager_id)
#     assert response["status"] == "valid"
#     assert status_code == 200

# # Boundary Test - Less than 50% capacity
# def test_get_current_manpower_boundary_low(mock_supabase):
#     test_date = "2024-10-08"
#     test_manager_id = 140894
    
#     # Mock employee response
#     mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
#         {"staff_id": 101}, {"staff_id": 102}
#     ]
    
#     # Mock schedule responses - In office < 50% of capacity
#     mock_supabase.table.return_value.select.return_value.lte.return_value.gte.return_value.eq.return_value.in_.return_value.execute.side_effect = [
#         MagicMock(data=[{"staff_id": 101}]),  # count_in_office
#         MagicMock(data=[{"staff_id": 101}, {"staff_id": 102},{"staff_id":103}])  # max_capacity
#     ]
    
#     # Expected invalid status due to less than 50% in-office capacity
#     response, status_code = get_current_manpower(test_date, test_manager_id)
#     assert response["status"] == "invalid"
#     assert status_code == 200

# # Boundary Test - Exactly 50% capacity
# def test_get_current_manpower_boundary_exact(mock_supabase):
#     test_date = "2024-10-18"
#     test_manager_id = 140894
    
#     # Mock employee response
#     mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
#         {"staff_id": 101}, {"staff_id": 102}
#     ]
    
#     # Mock schedule responses - 50% in office
#     mock_supabase.table.return_value.select.return_value.lte.return_value.gte.return_value.eq.return_value.in_.return_value.execute.side_effect = [
#         MagicMock(data=[{"staff_id": 101}]),  
#         MagicMock(data=[{"staff_id": 101}, {"staff_id": 102}])  
#     ]
    
#     # Expected valid status since 50% capacity is exactly at the boundary
#     response, status_code = get_current_manpower(test_date, test_manager_id)
#     assert response["status"] == "valid"
#     assert status_code == 200

# # Error Path - Invalid date format
# def test_get_current_manpower_invalid_date_format(mock_supabase):
#     invalid_date = "18-10-2024"
#     test_manager_id = 140894
    
#     # Expected exception due to wrong date format
#     response, status_code = get_current_manpower(invalid_date, test_manager_id)
#     assert "info" in response
#     assert status_code == 500