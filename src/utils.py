import time
import os
from datetime import datetime

def format_time(timestamp):
    """Format timestamp to readable string"""
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

def log_event(message, log_file='event_log.txt'):
    """Log event with timestamp to file and console"""
    timestamp = time.time()
    formatted_time = format_time(timestamp)
    log_message = f"[{formatted_time}] {message}"
    
    # Print to console
    print(log_message)
    
    # Write to log file
    try:
        # Ensure logs directory exists
        log_dir = os.path.dirname(log_file) if os.path.dirname(log_file) else '.'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')
    except Exception as e:
        print(f"Error writing to log file: {e}")

def calculate_frequency(toggle_times):
    """Calculate frequency from toggle times"""
    if len(toggle_times) < 2:
        return 0
    
    time_span = toggle_times[-1] - toggle_times[0]
    if time_span == 0:
        return 0
    
    # Frequency = number of transitions / time span
    return (len(toggle_times) - 1) / time_span

def analyze_toggle_pattern(toggle_times, window_ms=60):
    """Analyze toggle pattern within a time window"""
    if len(toggle_times) < 2:
        return {
            'frequency': 0,
            'intervals': [],
            'avg_interval': 0,
            'rapid_toggles': False
        }
    
    # Calculate intervals between toggles
    intervals = []
    for i in range(1, len(toggle_times)):
        interval_ms = (toggle_times[i] - toggle_times[i-1]) * 1000
        intervals.append(interval_ms)
    
    avg_interval = sum(intervals) / len(intervals) if intervals else 0
    frequency = calculate_frequency(toggle_times)
    
    # Check if toggles are within the rapid window
    time_span = (toggle_times[-1] - toggle_times[0]) * 1000  # Convert to ms
    rapid_toggles = time_span <= window_ms and len(toggle_times) >= 6
    
    return {
        'frequency': frequency,
        'intervals': intervals,
        'avg_interval': avg_interval,
        'rapid_toggles': rapid_toggles,
        'time_span_ms': time_span
    }

def clear_log_file(log_file='event_log.txt'):
    """Clear the log file"""
    try:
        if os.path.exists(log_file):
            os.remove(log_file)
            print(f"Log file {log_file} cleared")
    except Exception as e:
        print(f"Error clearing log file: {e}")

def get_log_stats(log_file='event_log.txt'):
    """Get statistics about the log file"""
    try:
        if not os.path.exists(log_file):
            return {'lines': 0, 'size_bytes': 0}
        
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = sum(1 for _ in f)
        
        size_bytes = os.path.getsize(log_file)
        
        return {
            'lines': lines,
            'size_bytes': size_bytes,
            'size_kb': size_bytes / 1024
        }
    except Exception as e:
        print(f"Error getting log stats: {e}")
        return {'lines': 0, 'size_bytes': 0}