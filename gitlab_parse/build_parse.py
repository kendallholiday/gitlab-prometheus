import json
from prometheus_client import Counter

class BuildData:
    def __init__(self, build_data):
        self.build_queued_duration = build_data.get("build_queued_duration", None)
        self.build_failure_reason = build_data.get("build_failure_reason", None)
        self.commit_detail_author_url = build_data.get("commit_detail_author_url", None)
        self.commit_detail_duration = build_data.get("commit_detail_duration", None)

def parse_build_data(build_data):
    build_data_obj = BuildData(build_data)


    gl_event={}
    gl_event['eventType'] = 'gitlabBuildEvent'
    # ... (the existing code)
    return gl_event

build_events = Counter('gitlab_build_events', 'Number of GitLab build events', ['event_type'])

def update_prometheus_metrics(parsed_data):
    event_type = parsed_data['eventType']
    build_events.labels(event_type=event_type).inc()

