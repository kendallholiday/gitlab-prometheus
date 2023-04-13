import json
import os
from gitlab_parse import push_parse, build_parse, pipeline_parse, deployment_parse, tag_push_parse, release_parse
import gitlab_parse
from flask import Flask, json, request
from prometheus_flask_exporter import PrometheusMetrics
from gitlab_parse import update_prometheus_metrics


app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Add this metric for counting webhook events
webhook_event_counter = metrics.counter(
    'webhook_events', 'Number of webhook events received', labels=['event_type']
)

@app.route('/', methods=['GET'])
def hello():
    return 'Yes Running'

@app.post('/gitlab')
@app.post('/gitlab')
def get_post():
    # ... (the existing code)
    
    if 'push' == request.json['object_kind']:
        parsed_data = push_parse.parse_push_data(push_data=request.json)
    elif 'build' == request.json['object_kind']:
        parsed_data = build_parse.parse_build_data(build_data=request.json)
    elif 'pipeline' == request.json['object_kind']:
        parsed_data = pipeline_parse.parse_pipeline_data(pipeline_data=request.json)
    elif 'deployment' == request.json['object_kind']:
        parsed_data = deployment_parse.parse_deployment_data(deployment_data=request.json)
    elif 'tag_push' == request.json['object_kind']:
        parsed_data = tag_push_parse.parse_tag_push_data(tag_push_data=request.json)
    elif 'release' == request.json['object_kind']:
        parsed_data = release_parse.parse_release_data(release_data=request.json)
    else:
        print(request.json)
        return request.json

    # Update Prometheus metrics based on the parsed data
    update_prometheus_metrics(parsed_data)

    return request.json


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True, ssl_context='adhoc')
