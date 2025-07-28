import unittest
from src.utils import format_time, log_event

class TestUtils(unittest.TestCase):

    def test_format_time(self):
        # Test formatting of time
        timestamp = 1633072800  # Example timestamp
        formatted_time = format_time(timestamp)
        self.assertEqual(formatted_time, "2021-10-01 00:00:00")  # Expected format

    def test_log_event(self):
        # Test logging of events
        log_message = "Test event"
        log_event(log_message)  # Assuming this function prints or logs the message
        # Here you would check the output of the log, depending on how log_event is implemented
        # This is a placeholder as actual checking would depend on the logging mechanism used

if __name__ == '__main__':
    unittest.main()