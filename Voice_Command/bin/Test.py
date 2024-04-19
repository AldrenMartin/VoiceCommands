import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from Voice_Commands import EventScheduler, main


class TestEventScheduler(unittest.TestCase):
    def setUp(self):
        with patch('Voice_Commands.sched.scheduler') as mock_scheduler:
            self.mock_scheduler = mock_scheduler
            self.scheduler = EventScheduler()
            self.mock_scheduler_instance = MagicMock()
            self.mock_scheduler.return_value = self.mock_scheduler_instance

    @patch('Voice_Commands.notification.notify')
    def test_add_event(self, mock_notify):
        event_name = "Meeting"
        event_date = "2024-04-20"
        event_time = "15:30"
        self.scheduler.add_event(event_name, event_date, event_time)
        self.assertEqual(len(self.scheduler.events), 1)
        self.assertIn(event_name, self.scheduler.events[0]['name'])

    @patch('Voice_Commands.notification.notify')
    def test_edit_event(self, mock_notify):
        self.scheduler.add_event("Meeting", "2024-04-20", "15:30")
        self.scheduler.edit_event(0, "Updated Meeting", "2024-04-21", "16:30")
        self.assertEqual(self.scheduler.events[0]['name'], "Updated Meeting")
        self.assertEqual(self.scheduler.events[0]['date'], "2024-04-21")
        self.assertEqual(self.scheduler.events[0]['time'], "16:30")

    def test_view_events(self):
        self.scheduler.add_event("Meeting", "2024-04-20", "15:30")
        with patch('builtins.print') as mocked_print:
            self.scheduler.view_events()
            mocked_print.assert_called_with("0: Meeting on 2024-04-20 at 15:30")

    @patch('Voice_Commands.notification.notify')
    def test_delete_event(self, mock_notify):
        self.scheduler.add_event("Meeting", "2024-04-20", "15:30")
        self.scheduler.delete_event(0)
        self.assertEqual(len(self.scheduler.events), 0)


class TestApplicationFlow(unittest.TestCase):
    def setUp(self):
        self.scheduler = EventScheduler()

    @patch('builtins.input', side_effect=['6'])
    def test_application_exit(self, mock_input):
        with self.assertRaises(SystemExit):
            main()

    @patch('builtins.input', side_effect=['1', 'Meeting', '2024-01-01', '12:00', '6'])
    @patch('Voice_Commands.EventScheduler.add_event')
    def test_add_event_through_manual_input(self, mock_add_event, mock_input):
        with self.assertRaises(SystemExit):
            main()
        mock_add_event.assert_called_once_with('Meeting', '2024-01-01', '12:00')

    @patch('builtins.input', side_effect=['5', '6'])  # activates voice command, then stops
    @patch('Voice_Commands.get_audio', side_effect=['add event', 'Meeting', '2024-01-01', '12:00'])
    @patch('Voice_Commands.speak')
    @patch('Voice_Commands.EventScheduler.add_event')
    def test_add_event_through_voice_command(self, mock_add_event, mock_speak, mock_get_audio, mock_input):
        with self.assertRaises(SystemExit):
            main()
        mock_add_event.assert_called_once_with('Meeting', '2024-01-01', '12:00')


if __name__ == '__main__':
    unittest.main()