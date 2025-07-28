import time
from dio_reader import DIOReader
from heap_monitor import HeapMonitor
from utils import log_event

def main():
    dio_reader = DIOReader(pin=0)
    heap_monitor = HeapMonitor()
    
    toggle_count = 0
    toggle_times = []
    last_toggle_time = 0

    dio_reader.start_reading()

    try:
        while True:
            current_time = time.time()
            if dio_reader.check_toggle():
                toggle_count += 1
                toggle_times.append(current_time)
                log_event(f"Toggle detected at {current_time}")

                if toggle_count == 1:
                    last_toggle_time = current_time

                if toggle_count >= 6:
                    time_diff = current_time - last_toggle_time
                    if time_diff <= 0.06:  # 20 ms * 3 = 60 ms
                        log_event(f"Six toggles detected within 20 ms intervals: {toggle_times[-6:]}")
                    toggle_count = 0  # Reset after six toggles

            heap_monitor.log_heap_size()
            time.sleep(0.01)  # Sleep to prevent busy waiting

    except KeyboardInterrupt:
        log_event("Monitoring stopped by user.")
    finally:
        dio_reader.stop_reading()

if __name__ == "__main__":
    main()