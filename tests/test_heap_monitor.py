import time
import unittest
from unittest.mock import patch
from src.heap_monitor import HeapMonitor
from src.dio_reader import DIOReader

class TestHeapMonitor(unittest.TestCase):
    def setUp(self):
        self.heap_monitor = HeapMonitor()
        self.dio_reader = DIOReader()

    @patch('src.dio_reader.DIOReader.read_pin')
    def test_toggle_detection_and_heap_monitoring(self, mock_read_pin):
        # Simulate DIO pin toggling
        mock_read_pin.side_effect = [0, 1, 0, 1, 0, 1]  # Simulate toggles
        toggle_times = []
        
        # Start monitoring
        self.dio_reader.start_reading()
        
        # Record the time of each toggle
        for _ in range(6):
            time.sleep(0.02)  # 20 ms gap
            if self.dio_reader.check_toggle():
                toggle_times.append(time.time())
        
        # Stop monitoring
        self.dio_reader.stop_reading()

        # Check if we detected exactly three toggles
        self.assertEqual(len(toggle_times), 3)

        # Check heap memory size at the time of toggles
        heap_sizes = [self.heap_monitor.get_current_heap_size() for _ in toggle_times]

        # Log the toggle times and heap sizes for analysis
        for toggle_time, heap_size in zip(toggle_times, heap_sizes):
            print(f'Toggle at {toggle_time}, Heap size: {heap_size}')

if __name__ == '__main__':
    unittest.main()