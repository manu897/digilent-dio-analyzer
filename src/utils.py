def format_time(timestamp):
    from datetime import datetime
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def log_event(message):
    with open('event_log.txt', 'a') as log_file:
        log_file.write(f"{format_time(time.time())} - {message}\n")