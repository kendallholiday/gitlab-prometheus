import json
import os
import gitlab_parse
from gitlab_parse import build_parse, push_parse
from flask import Flask, json, request
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

def event_type(request_obj):
    return request_obj.json.get("object_kind")

webhook_event_counter = metrics.counter(
    'webhook_events', 'Number of webhook events received', labels={'event_type': lambda: event_type(request)}
)

commit_counter = metrics.counter(
    "commit_counter", "Number of commits", labels=["git_project_id"]
)

@app.route('/', methods=['GET'])
def hello():
    return 'Yes Running'

@app.post('/gitlab')
def get_post():
    webhook_event_counter.labels().inc()
    
    if "push" == request.json["object_kind"]:
        parsed_data = push_parse.parse_push_data(push_data=request.json)
        for commit_event in parsed_data["gl_commit_array"]:
            git_project_id = commit_event["git_project_id"]
            commit_counter.labels(git_project_id=git_project_id).inc()
    elif 'build' == request.json['object_kind']:
        parsed_data = build_parse.parse_build_data(build_data=request.json)
    else:
        print(request.json)
        return request.json

    return request.json

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True, ssl_context='adhoc')
