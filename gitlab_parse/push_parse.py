import json



class PushData:
    def __init__(self, push_data):
        self.project_detail_ci_config_path = push_data.get("project_detail_ci_config_path", None)
        self.project_detail_ci_config_path = push_data.get("project_detail_ci_config_path", None)
        self.project_detail_default_branch = push_data.get("project_detail_default_branch", None)
        self.project_detail_description = push_data.get("project_detail_description", None)
        self.project_detail_visibility_level = push_data.get("project_detail_visibility_level", None)
        self.repository_detail_description = push_data.get("repository_detail_description", None)
        self.repository_detail_visibility_level = push_data.get("repository_detail_visibility_level", None)

def parse_push_data(push_data):
    push_data_obj = PushData(push_data)


    return {
        "gl_event": gl_event,
        "gl_commit_array": gl_commit_array,
        "result": "success"
    }
