from prometheus_client import Counter, start_http_server
import time

# Define metrics
gitlab_events_total = Counter('gitlab_events_total', 'Total number of GitLab events', ['event_type'])

def increment_event_counter(event_type):
    gitlab_events_total.labels(event_type=event_type).inc()

if __name__ == '__main__':
    # Start the HTTP server to expose metrics
    start_http_server(8000)
    while True:
        time.sleep(1)
