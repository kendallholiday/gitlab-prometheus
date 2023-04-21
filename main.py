import threading
from prom_gldb import prom_write
import json
import os
from gitlab_parse import push_parse, build_parse, pipeline_parse, deployment_parse, tag_push_parse, release_parse
import gitlab_parse
from flask import Flask, json, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello():
    return 'Yes Running'

@app.post('/gitlab')
def get_post():
    #print(request.json)
    print("Received event:", request.json)
    print(request.json['object_kind'])

    if 'push' == request.json['object_kind']:
        push_parse.parse_push_data(push_data=request.json)
    elif 'build' == request.json['object_kind']:
        build_parse.parse_build_data(build_data=request.json)
    elif 'pipeline' == request.json['object_kind']:
        pipeline_parse.parse_pipeline_data(pipeline_data=request.json)
    elif 'deployment' == request.json['object_kind']:
        deployment_parse.parse_deployment_data(deployment_data=request.json)
    elif 'tag_push' == request.json['object_kind']:
        tag_push_parse.parse_tag_push_data(tag_push_data=request.json)
    elif 'release' == request.json['object_kind']:
        release_parse.parse_release_data(release_data=request.json)
    else:
        print(request.json)



    return request.json

t = threading.Thread(target=start_prom_server)
t.start()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True, ssl_context='adhoc', threaded=True)
