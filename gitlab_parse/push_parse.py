import json
from prom_gldb.prom_write import increment_event_counter
from prom_gldb import prom_write

def parse_push_data(push_data):
    # print(push_data)
    nr_event={}
    nr_event['eventType'] = 'gitlabPushEvent'
    increment_event_counter(nr_event['eventType'])
    global_project_id = push_data['project_id']
    nr_event['git_project_id'] = global_project_id

    nr_commit_array = []

    for item in push_data:

        #Flatten the Project Detail

        if 'project' == item:

            for p_item in push_data['project']:
                fix_project = 'project_detail_' + p_item
                nr_event[fix_project] = push_data['project'][p_item]

        elif 'commits' == item:

            nr_commit_event = {}
            for c_item in push_data['commits']:
                nr_commit_event = {}
                nr_commit_event['eventType'] = 'gitlabPushCommitEvent'
                nr_commit_event['git_project_id'] = global_project_id
                for c_detail in c_item:
                    nr_commit_event[c_detail] = c_item[c_detail]
            nr_commit_array.append(nr_commit_event)


        elif 'repository' == item:

            for r_item in push_data['repository']:
                fix_project = 'repository_detail_' + r_item
                nr_event[fix_project] = push_data['project'][r_item]

        else:
            nr_event[item] = push_data[item]


    #print(nr_event)
    prom_write.increment_event_counter(nr_event['eventType'])
    for commit_event in nr_commit_array:
        prom_write.increment_event_counter(commit_event['eventType'])