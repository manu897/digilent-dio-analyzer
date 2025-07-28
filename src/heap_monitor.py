import psutil
import time
from utils import log_event

class HeapMonitor:
    def __init__(self):
        self.heap_sizes = []
        self.process = psutil.Process()
        self.last_log_time = 0
        self.log_interval = 1.0  # Log every 1 second to avoid spam

    def get_memory_info(self):
        """Get detailed memory information"""
        try:
            memory_info = self.process.memory_info()
            return {
                'rss': memory_info.rss,  # Resident Set Size (physical memory)
                'vms': memory_info.vms,  # Virtual Memory Size
                'percent': self.process.memory_percent(),
                'available': psutil.virtual_memory().available,
                'total': psutil.virtual_memory().total
            }
        except Exception as e:
            print(f"Error getting memory info: {e}")
            return None

    def check_heap_size(self):
        """Get current memory usage in bytes"""
        memory_info = self.get_memory_info()
        if memory_info:
            return memory_info['rss']  # Return RSS (physical memory usage)
        return 0

    def log_heap_size(self):
        """Log heap size with rate limiting"""
        current_time = time.time()
        
        # Rate limit logging to avoid spam
        if current_time - self.last_log_time < self.log_interval:
            return
            
        current_size = self.check_heap_size()
        memory_info = self.get_memory_info()
        
        if memory_info:
            self.heap_sizes.append({
                'timestamp': current_time,
                'rss': memory_info['rss'],
                'vms': memory_info['vms'],
                'percent': memory_info['percent']
            })
            
            # Log to console (less verbose)
            print(f"Memory: RSS={memory_info['rss']//1024//1024}MB, "
                  f"VMS={memory_info['vms']//1024//1024}MB, "
                  f"Usage={memory_info['percent']:.1f}%")
            
            self.last_log_time = current_time

    def check_memory_spike(self, threshold_mb=100):
        """Check if there's been a significant memory increase"""
        if len(self.heap_sizes) < 2:
            return False
            
        current = self.heap_sizes[-1]['rss']
        previous = self.heap_sizes[-2]['rss']
        
        increase_mb = (current - previous) / (1024 * 1024)
        
        if increase_mb > threshold_mb:
            log_event(f"Memory spike detected: +{increase_mb:.1f}MB")
            return True
        return False

    def get_heap_sizes(self):
        """Get all recorded heap sizes"""
        return self.heap_sizes.copy()

    def clear_heap_sizes(self):
        """Clear recorded heap sizes"""
        self.heap_sizes.clear()

    def get_memory_summary(self):
        """Get a summary of memory usage"""
        if not self.heap_sizes:
            return "No memory data available"
            
        rss_values = [entry['rss'] for entry in self.heap_sizes]
        
        return {
            'min_mb': min(rss_values) / (1024 * 1024),
            'max_mb': max(rss_values) / (1024 * 1024),
            'avg_mb': sum(rss_values) / len(rss_values) / (1024 * 1024),
            'samples': len(rss_values)
        }