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

    gl_event = {
        "project_id": push_data["project"]["id"],
        "project_name": push_data["project"]["name"],
        "ref": push_data["ref"],
        "before_sha": push_data["before"],
        "after_sha": push_data["after"],
        "total_commits_count": push_data["total_commits_count"]
    }

    gl_commit_array = []

    for commit in push_data["commits"]:
        gl_commit = {
            "commit_id": commit["id"],
            "message": commit["message"],
            "author_name": commit["author"]["name"],
            "author_email": commit["author"]["email"],
            "timestamp": commit["timestamp"],
            "url": commit["url"],
            "added": commit["added"],
            "modified": commit["modified"],
            "removed": commit["removed"],
            "git_project_id": push_data["project"]["id"]
        }
        gl_commit_array.append(gl_commit)

    return {
        "gl_event": gl_event,
        "gl_commit_array": gl_commit_array,
        "result": "success"
    }

