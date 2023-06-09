from prometheus_client import Counter, start_http_server
import time

# Define metrics
gitlab_events_total = Counter('gitlab_events_total', 'Total number of GitLab events', ['event_type'])



def increment_event_counter(event_type):
    print("Incrementing event counter for", event_type)
    gitlab_events_total.labels(event_type=event_type).inc()

def write_data(data):
    if isinstance(data, list):
        for item in data:
            increment_event_counter(item['eventType'])
    elif isinstance(data, dict):
        increment_event_counter(data['eventType'])
    else:
        raise ValueError("Unsupported data type. Expected list or dict.")
    
if __name__ == '__main__':
    # Start the HTTP server to expose metrics
    start_http_server(8001)
    while True:
        time.sleep(1)
