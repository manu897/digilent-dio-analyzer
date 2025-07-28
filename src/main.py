import time
import signal
import sys
from dio_reader import DIOReader
from heap_monitor import HeapMonitor
from utils import log_event, analyze_toggle_pattern, clear_log_file

class DIOAnalyzer:
    def __init__(self, pin=0, rapid_toggle_count=6, rapid_window_ms=60):
        self.dio_reader = DIOReader(pin=pin)
        self.heap_monitor = HeapMonitor()
        
        # Configuration
        self.rapid_toggle_count = rapid_toggle_count
        self.rapid_window_ms = rapid_window_ms / 1000.0  # Convert to seconds
        
        # State tracking
        self.toggle_count = 0
        self.toggle_times = []
        self.last_toggle_time = 0
        self.running = False
        self.total_toggles = 0
        
        # Statistics
        self.rapid_sequences_detected = 0
        self.start_time = None
        
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        log_event("Interrupt signal received. Shutting down...")
        self.stop()
        
    def start(self):
        """Start the monitoring process"""
        self.running = True
        self.start_time = time.time()
        
        # Set up signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        
        log_event("Starting DIO analysis...")
        log_event(f"Configuration: {self.rapid_toggle_count} toggles within {self.rapid_window_ms*1000}ms")
        
        try:
            self.dio_reader.start_reading()
            self._monitoring_loop()
        except Exception as e:
            log_event(f"Error during monitoring: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """Stop the monitoring process"""
        if not self.running:
            return
            
        self.running = False
        self.dio_reader.stop_reading()
        
        # Print final statistics
        self._print_final_stats()
        
        log_event("DIO analysis stopped.")
        sys.exit(0)
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.running:
            current_time = time.time()
            
            # Check for DIO toggle
            if self.dio_reader.check_toggle():
                self._handle_toggle(current_time)
            
            # Monitor memory (with built-in rate limiting)
            self.heap_monitor.log_heap_size()
            
            # Check for memory spikes
            if self.heap_monitor.check_memory_spike(threshold_mb=50):
                log_event("Memory spike detected during DIO monitoring")
            
            # Small sleep to prevent excessive CPU usage
            time.sleep(0.001)  # 1ms sleep
    
    def _handle_toggle(self, current_time):
        """Handle a detected toggle"""
        self.toggle_count += 1
        self.total_toggles += 1
        self.toggle_times.append(current_time)
        
        log_event(f"Toggle #{self.total_toggles} detected at {current_time:.6f}")
        
        # Set the first toggle time for sequence detection
        if self.toggle_count == 1:
            self.last_toggle_time = current_time
        
        # Check for rapid toggle sequence
        if self.toggle_count >= self.rapid_toggle_count:
            self._check_rapid_sequence(current_time)
    
    def _check_rapid_sequence(self, current_time):
        """Check if we have a rapid toggle sequence"""
        time_diff = current_time - self.last_toggle_time
        
        if time_diff <= self.rapid_window_ms:
            self.rapid_sequences_detected += 1
            
            # Analyze the toggle pattern
            recent_toggles = self.toggle_times[-self.rapid_toggle_count:]
            pattern_analysis = analyze_toggle_pattern(recent_toggles, self.rapid_window_ms * 1000)
            
            log_event(f"🚨 RAPID SEQUENCE #{self.rapid_sequences_detected} DETECTED!")
            log_event(f"   {self.rapid_toggle_count} toggles in {time_diff*1000:.1f}ms")
            log_event(f"   Frequency: {pattern_analysis['frequency']:.1f} Hz")
            log_event(f"   Avg interval: {pattern_analysis['avg_interval']:.1f}ms")
            log_event(f"   Toggle times: {[f'{t:.6f}' for t in recent_toggles]}")
            
            # Log memory state during rapid sequence
            memory_info = self.heap_monitor.get_memory_info()
            if memory_info:
                log_event(f"   Memory at event: {memory_info['rss']//1024//1024}MB RSS, "
                         f"{memory_info['percent']:.1f}% usage")
        
        # Reset counter for next sequence detection
        self.toggle_count = 0
        self.toggle_times = self.toggle_times[-self.rapid_toggle_count:]  # Keep last N toggles
    
    def _print_final_stats(self):
        """Print final statistics"""
        if self.start_time:
            runtime = time.time() - self.start_time
            log_event("="*50)
            log_event("FINAL STATISTICS")
            log_event("="*50)
            log_event(f"Runtime: {runtime:.1f} seconds")
            log_event(f"Total toggles detected: {self.total_toggles}")
            log_event(f"Rapid sequences detected: {self.rapid_sequences_detected}")
            
            if runtime > 0:
                log_event(f"Average toggle rate: {self.total_toggles/runtime:.2f} toggles/sec")
            
            # Memory summary
            memory_summary = self.heap_monitor.get_memory_summary()
            if memory_summary != "No memory data available":
                log_event(f"Memory usage - Min: {memory_summary['min_mb']:.1f}MB, "
                         f"Max: {memory_summary['max_mb']:.1f}MB, "
                         f"Avg: {memory_summary['avg_mb']:.1f}MB")

def main():
    """Main entry point"""
    # Clear previous log
    clear_log_file()
    
    # Create and start analyzer
    analyzer = DIOAnalyzer(pin=0, rapid_toggle_count=6, rapid_window_ms=60)
    
    try:
        analyzer.start()
    except KeyboardInterrupt:
        analyzer.stop()

if __name__ == "__main__":
    main()