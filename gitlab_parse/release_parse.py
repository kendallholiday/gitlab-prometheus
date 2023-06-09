import json
from prom_gldb.prom_write import increment_event_counter
from prom_gldb import prom_write

def parse_release_data(release_data):
    # print(release_data)
    nr_event={}
    nr_event['eventType'] = 'gitlabreleaseEvent'
    increment_event_counter(nr_event['eventType'])
    global_project_id = release_data['project']['id']
    nr_event['git_project_id'] = global_project_id

    nr_commit_array = []

    for item in release_data:

        #Flatten the Project Detail

        if 'project' == item:

            for p_item in release_data['project']:
                fix_project = 'project_detail_' + p_item
                nr_event[fix_project] = release_data['project'][p_item]
        elif 'commit' == item:

            for p_item in release_data['commit']:
                fix_project = 'commit_detail_' + p_item
                nr_event[fix_project] = release_data['commit'][p_item]

        elif 'assets' == item:

            for p_item in release_data['assets']:
                if p_item == 'sources':

                    print(p_item)
                    source_array = []
                    for source_list in release_data['assets']['sources']:
                        print(source_list)
                        nr_event_sources = {}
                        nr_event_sources['git_project_id'] = global_project_id
                        nr_event_sources['eventType'] = 'gitlabReleaseSourcesEvent'
                        global_project_id = release_data['project']['id']
                        for source_detail in source_list:
                            nr_event_sources[source_detail] = source_list[source_detail]
                        source_array.append(nr_event_sources)





                else:
                    fix_project = 'asset_detail_' + p_item
                    nr_event[fix_project] = release_data['assets'][p_item]
                    print(nr_event[fix_project])
        else:
            nr_event[item] = release_data[item]


    #print(nr_event)
    prom_write.increment_event_counter(nr_event['eventType'])
    for source_event in source_array:
        prom_write.increment_event_counter(source_event['eventType'])