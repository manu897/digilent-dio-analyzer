import time
import unittest
from unittest.mock import patch, MagicMock
from src.dio_reader import DIOReader

class TestDIOReader(unittest.TestCase):
    def setUp(self):
        self.dio_reader = DIOReader(pin=0)

    @patch('src.dio_reader.time.sleep', return_value=None)  # Mock sleep to speed up tests
    def test_toggle_detection(self, mock_sleep):
        # Simulate toggles
        self.dio_reader.read_pin = MagicMock(side_effect=[0, 1, 0, 1, 0, 1])  # Simulate pin toggling
        self.dio_reader.start_reading()

        # Allow some time for the toggles to be detected
        time.sleep(0.1)

        # Check if we detected 3 toggles
        self.assertEqual(len(self.dio_reader.toggle_times), 3)
        self.assertTrue(all(t1 < t2 for t1, t2 in zip(self.dio_reader.toggle_times, self.dio_reader.toggle_times[1:])))
        
    def test_time_recording(self):
        # Simulate a toggle
        self.dio_reader.toggle_detected()
        time.sleep(0.02)  # Simulate a 20ms gap
        self.dio_reader.toggle_detected()
        time.sleep(0.02)
        self.dio_reader.toggle_detected()

        # Check recorded times
        self.assertEqual(len(self.dio_reader.toggle_times), 3)
        self.assertAlmostEqual(self.dio_reader.toggle_times[1] - self.dio_reader.toggle_times[0], 0.02, delta=0.005)
        self.assertAlmostEqual(self.dio_reader.toggle_times[2] - self.dio_reader.toggle_times[1], 0.02, delta=0.005)

if __name__ == '__main__':
    unittest.main()