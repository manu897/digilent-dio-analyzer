class HeapMonitor:
    def __init__(self):
        self.heap_sizes = []

    def check_heap_size(self):
        # This method should return the current heap size.
        # For demonstration purposes, we'll return a mock value.
        import random
        return random.randint(1000, 10000)

    def log_heap_size(self):
        current_size = self.check_heap_size()
        self.heap_sizes.append(current_size)
        print(f"Current heap size: {current_size} bytes")

    def get_heap_sizes(self):
        return self.heap_sizes

    def clear_heap_sizes(self):
        self.heap_sizes.clear()