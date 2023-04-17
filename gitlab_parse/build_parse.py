import json
from prometheus_client import Counter


def parse_build_data(build_data):

    nr_event={}
    nr_event['eventType'] = 'gitlabBuildEvent'
    # ... (the existing code)

    return nr_event

build_events = Counter('gitlab_build_events', 'Number of GitLab build events', ['event_type'])

def update_prometheus_metrics(parsed_data):
    event_type = parsed_data['eventType']
    build_events.labels(event_type=event_type).inc()
