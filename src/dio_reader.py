class DIOReader:
    def __init__(self, dio_pin):
        self.dio_pin = dio_pin
        self.toggle_count = 0
        self.toggle_timestamps = []
        self.last_toggle_time = 0

    def start_reading(self):
        # This method should start monitoring the DIO pin for changes
        # Implementation depends on the specific library used for DIO access
        pass

    def detect_toggle(self, current_time):
        if self.toggle_count < 3:
            if self.toggle_count == 0 or (current_time - self.last_toggle_time) <= 20:
                self.toggle_timestamps.append(current_time)
                self.toggle_count += 1
                self.last_toggle_time = current_time

        if self.toggle_count == 3:
            self.reset_detection()

    def reset_detection(self):
        self.toggle_count = 0
        self.toggle_timestamps.clear()

    def get_toggle_timestamps(self):
        return self.toggle_timestamps.copy()