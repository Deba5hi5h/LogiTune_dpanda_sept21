from common import framework_params

import requests
import uuid
import os


LOGS_SERVER_LOCAL_IP = "http://172.17.54.176"


dashboard_publish = framework_params.DASHBOARD_PUBLISH


def store_failed_testcase_logs_on_server(logs_path: str) -> str:
    server_running = requests.get(LOGS_SERVER_LOCAL_IP).ok
    if dashboard_publish and server_running:
        with open(logs_path, "rb") as file:
            uuid_file_name = str(uuid.uuid1()) + "_" + os.path.basename(logs_path)
            files = {'file': (uuid_file_name, file)}
            response = requests.post(LOGS_SERVER_LOCAL_IP + "/logs", files=files)
        if response.ok:
            return LOGS_SERVER_LOCAL_IP + "/logs/" + uuid_file_name
