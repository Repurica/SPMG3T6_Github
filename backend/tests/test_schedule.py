

import unittest
from flask import Flask
from flask.testing import FlaskClient
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app
from schedule import schedule

class ScheduleTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    @patch('schedule.supabase')
    def test_get_staff_schedules_success(self, mock_supabase):
        # Mock supabase responses for staff_schedules
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
                'staff_id': '140003',
                'starting_date': '2023-10-01',
                'monday': 'AM',
                'tuesday': 'PM',
                'wednesday': 'full_day',
                'thursday': 'in_office',
                'friday': None
            }])
        ]

        response = self.client.get('/schedule/staff_schedules?staff_id=140003')
        self.assertEqual(response.status_code, 200)
        
        # Ensure response JSON structure
        self.assertIn('schedules', response.json)
        self.assertIn('staff_data', response.json)
        
        # Test staff_data contents
        staff_data = response.json['staff_data'][0]
        self.assertEqual(staff_data['staff_name'], 'John Doe')
        self.assertEqual(staff_data['staff_id'], '140003')
        
        # Test schedules contents
        schedules = response.json['schedules']
        self.assertEqual(len(schedules), 3)  # Three days with WFH status

        # Check specific day entries
        am_schedule = next((s for s in schedules if s['wfh'] == 'AM WFH'), None)
        # Further checks for PM and full_day can be added here

    @patch('schedule.supabase')
    def test_get_all_schedules_success(self, mock_supabase):
        # Mock supabase responses for all_schedules
        mock_supabase.table.return_value.select.return_value.execute.side_effect = [
            MagicMock(data=[
                {
                    'staff_fname': 'Alice',
                    'staff_lname': 'Smith',
                    'staff_id': '140001',
                    'position': 'Manager',
                    'role': 3,
                    'dept': 'Engineering',
                    'reporting_manager': None
                },
                {
                    'staff_fname': 'Bob',
                    'staff_lname': 'Brown',
                    'staff_id': '140002',
                    'position': 'Developer',
                    'role': 2,
                    'dept': 'Engineering',
                    'reporting_manager': '140001'
                }
            ]),
            MagicMock(data=[
                {
                    'staff_id': '140001',
                    'starting_date': '2023-10-01',
                    'monday': 'AM',
                    'tuesday': 'PM',
                    'wednesday': 'full_day',
                    'thursday': 'in_office',
                    'friday': None
                },
                {
                    'staff_id': '140002',
                    'starting_date': '2023-10-01',
                    'monday': 'PM',
                    'tuesday': 'full_day',
                    'wednesday': None,
                    'thursday': 'in_office',
                    'friday': 'AM'
                }
            ])
        ]

        response = self.client.get('/schedule/all_schedules')
        self.assertEqual(response.status_code, 200)

        # Check response structure
        self.assertIn('schedules', response.json)
        self.assertIn('staff_data', response.json)

        # Test staff_data contents
        staff_data = response.json['staff_data']
        self.assertEqual(len(staff_data), 2)
        self.assertEqual(staff_data[0]['staff_name'], 'Alice Smith')
        self.assertEqual(staff_data[1]['staff_name'], 'Bob Brown')

        # Test schedules contents
        schedules = response.json['schedules']
        self.assertGreater(len(schedules), 0)

        # Verify individual schedule entries for AM, PM, and full_day
        am_schedule = next((s for s in schedules if s['wfh'] == 'AM WFH' and s['staff_id'] == '140001'), None)
        self.assertIsNotNone(am_schedule)
        self.assertEqual(am_schedule['dept'], 'Engineering')
        self.assertEqual(am_schedule['position'], 'Manager')

        pm_schedule = next((s for s in schedules if s['wfh'] == 'PM WFH' and s['staff_id'] == '140002'), None)
        self.assertIsNotNone(pm_schedule)

        # Additional checks for other statuses or days can be included here

if __name__ == '__main__':
    unittest.main()
