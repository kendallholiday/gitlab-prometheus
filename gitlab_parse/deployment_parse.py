import json
from prom_gldb.prom_write import increment_event_counter
from prom_gldb import prom_write


def parse_deployment_data(deployment_data, license_key, account_id):
    # print(deployment_data)

    nr_event = {}
    nr_event['eventType'] = 'gitlabdeploymentEvent'
    increment_event_counter(nr_event['eventType'])
    global_project_id = deployment_data['project']['id']
    nr_event['git_project_id'] = global_project_id
    nr_deployment_array = []

    for item in deployment_data:

        if 'project' == item:

            for p_item in deployment_data['project']:
                fix_project = 'project_detail_' + p_item
                nr_event[fix_project] = deployment_data['project'][p_item]


        else:
            nr_event[item] = deployment_data[item]

    #print(nr_event)
    prom_write.write_data(nr_event, license_key, account_id=account_id)