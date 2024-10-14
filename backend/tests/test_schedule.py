import unittest
from flask import Flask
from flask.testing import FlaskClient
from unittest.mock import patch, MagicMock
from schedule import schedule

class TestSchedule(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(schedule, url_prefix='/schedule')
        self.client = self.app.test_client()

    @patch('schedule.supabase')
    def test_get_staff_schedules_valid_staff_id(self, mock_supabase):
        mock_staff_data = MagicMock(data=[{'staff_fname': 'John', 'staff_lname': 'Doe', 'staff_id': 140003}])
        mock_schedule_data = MagicMock(data=[
            {'starting_date': '2024-09-01', 'monday': 'AM', 'tuesday': 'PM', 'wednesday': 'Whole day', 'thursday': 'in-office', 'friday': 'AM'}
        ])
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = [mock_staff_data, mock_schedule_data]
        
        response = self.client.get('/schedule/staff_schedules?staff_id=140003')
        self.assertEqual(response.status_code, 200)
        self.assertIn('schedules', response.json)
        self.assertIn('staff_data', response.json)

    @patch('schedule.supabase')
    def test_get_team_schedules_valid_staff_id(self, mock_supabase):
        mock_staff_data = MagicMock(data=[{'staff_fname': 'John', 'staff_lname': 'Doe', 'staff_id': 140003, 'position': 'Manager', 'role': 3}])
        mock_team_members = MagicMock(data=[
            {'staff_fname': 'John', 'staff_lname': 'Doe', 'staff_id': 140003, 'position': 'Manager', 'role': 3},
            {'staff_fname': 'Jane', 'staff_lname': 'Smith', 'staff_id': 140004, 'position': 'Manager', 'role': 2}
        ])
        mock_schedule_data = MagicMock(data=[
            {'starting_date': '2024-09-01', 'monday': 'AM', 'tuesday': 'PM', 'wednesday': 'Whole day', 'thursday': 'in-office', 'friday': 'AM'}
        ])
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = [mock_staff_data, mock_team_members, mock_schedule_data, mock_schedule_data]
        
        response = self.client.get('/schedule/team_schedules?staff_id=140003')
        self.assertEqual(response.status_code, 200)
        self.assertIn('schedules', response.json)
        self.assertIn('staff_data', response.json)



    @patch('schedule.supabase')
    def test_get_staff_schedules_no_schedule(self, mock_supabase):
        mock_staff_data = MagicMock(data=[{'staff_fname': 'John', 'staff_lname': 'Doe', 'staff_id': 140003}])
        mock_schedule_data = MagicMock(data=[])
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = [mock_staff_data, mock_schedule_data]
        
        response = self.client.get('/schedule/staff_schedules?staff_id=140003')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json)

    @patch('schedule.supabase')
    def test_get_team_schedules_no_team_members(self, mock_supabase):
        mock_staff_data = MagicMock(data=[{'staff_fname': 'John', 'staff_lname': 'Doe', 'staff_id': 140003, 'position': 'Manager', 'role': 3}])
        mock_team_members = MagicMock(data=[])
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = [mock_staff_data, mock_team_members]
        
        response = self.client.get('/schedule/team_schedules?staff_id=140003')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json)

if __name__ == '__main__':
    unittest.main()