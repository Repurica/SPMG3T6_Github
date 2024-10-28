import unittest
from flask import Flask
from flask.testing import FlaskClient
from unittest.mock import patch, MagicMock
from schedule import schedule
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app

class ScheduleTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    @patch('schedule.supabase')
    def test_get_staff_schedules_success(self, mock_supabase):
        # Mock the supabase responses
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = [
            MagicMock(data=[{
                'staff_fname': 'John',
                'staff_lname': 'Doe',
                'staff_id': '140003',
                'dept': 'Engineering',
                'position': 'Developer',
                'reporting_manager': '140001'
            }]),
            MagicMock(data=[{
                'staff_fname': 'Jane',
                'staff_lname': 'Smith'
            }]),
            MagicMock(data=[{
                'staff_id': '140003',
                'starting_date': '2023-10-01',
                'monday': 'AM',
                'tuesday': 'PM',
                'wednesday': 'Whole day',
                'thursday': 'in-office',
                'friday': None
            }])
        ]

        response = self.client.get('/schedule/staff_schedules?staff_id=140003')
        self.assertEqual(response.status_code, 200)
        self.assertIn('schedules', response.json)
        self.assertIn('staff_data', response.json)

    @patch('schedule.supabase')
    def test_get_staff_schedules_no_staff(self, mock_supabase):
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = MagicMock(data=[])

        response = self.client.get('/schedule/staff_schedules?staff_id=140003')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json)

    @patch('schedule.supabase')
    def test_get_team_schedules_success(self, mock_supabase):
        # Mock the supabase responses
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = [
            MagicMock(data=[{
                'staff_fname': 'John',
                'staff_lname': 'Doe',
                'staff_id': '140003',
                'dept': 'Engineering',
                'position': 'Developer',
                'reporting_manager': '140001'
            }]),
            MagicMock(data=[{
                'staff_fname': 'Jane',
                'staff_lname': 'Smith'
            }]),
            MagicMock(data=[{
                'staff_fname': 'Alice',
                'staff_lname': 'Johnson',
                'staff_id': '140004',
                'position': 'Developer',
                'role': 2,
                'dept': 'Engineering'
            }]),
            MagicMock(data=[{
                'staff_id': '140004',
                'starting_date': '2023-10-01',
                'monday': 'AM',
                'tuesday': 'PM',
                'wednesday': 'Whole day',
                'thursday': 'in-office',
                'friday': None
            }])
        ]

        response = self.client.get('/schedule/team_schedules?staff_id=140003')
        self.assertEqual(response.status_code, 200)
        self.assertIn('schedules', response.json)
        self.assertIn('staff_data', response.json)

    @patch('schedule.supabase')
    def test_get_team_schedules_no_team_members(self, mock_supabase):
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = [
            MagicMock(data=[{
                'staff_fname': 'John',
                'staff_lname': 'Doe',
                'staff_id': '140003',
                'dept': 'Engineering',
                'position': 'Developer',
                'reporting_manager': '140001'
            }]),
            MagicMock(data=[{
                'staff_fname': 'Jane',
                'staff_lname': 'Smith'
            }]),
            MagicMock(data=[])
        ]

        response = self.client.get('/schedule/team_schedules?staff_id=140003')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json)

if __name__ == '__main__':
    unittest.main()
