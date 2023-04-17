import json
import os
import gitlab_parse
from gitlab_parse import build_parse, push_parse
from flask import Flask, json, request
from prometheus_flask_exporter import PrometheusMetrics
# Removed the import for update_prometheus_metrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Add this metric for counting webhook events
webhook_event_counter = metrics.counter(
    'webhook_events', 'Number of webhook events received', labels=['event_type']
)

# Moved the commit_counter to main.py and updated the label
commit_counter = metrics.counter(
    "commit_counter", "Number of commits", labels=["git_project_id"]
)

@app.route('/', methods=['GET'])
def hello():
    return 'Yes Running'

@app.post('/gitlab')
@app.post('/gitlab')
def get_post():
    # ... (the existing code)
    
    if "push" == request.json["object_kind"]:
        parsed_data = push_parse.parse_push_data(push_data=request.json)
        # Update Prometheus metrics based on the parsed data
        for commit_event in parsed_data["nr_commit_array"]:
            git_project_id = commit_event["git_project_id"]
            commit_counter.labels(git_project_id=git_project_id).inc()
    elif 'build' == request.json['object_kind']:
        parsed_data = build_parse.parse_build_data(build_data=request.json)
        # Update Prometheus metrics based on the parsed data
        build_parse.update_prometheus_metrics(parsed_data)
    else:
        print(request.json)
        return request.json

    return request.json

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True, ssl_context='adhoc')
