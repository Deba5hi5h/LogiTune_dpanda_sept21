import json
import os
from time import sleep

directory = os.path.dirname(__file__)


def read_manifest_file():
    filename = directory + '/' + 'manifests.json'
    with open(filename) as f:
        data = json.load(f)
    return data


def get_components_versions_by_manifest(manifest_ver):
    json = read_manifest_file()
    for entry in json:
        if entry == manifest_ver:
            return json[entry]['ANDROID'], json[entry]['AUDIO'], json[entry]['PT'], json[entry]['ZF'], json[entry]['HK'], json[entry]['COLLAB_OS']


def wait_for_result_or_timeout(callback, predicate, timeout=60):
    retry_time_s = 1
    max_tries = timeout / retry_time_s
    tries = 0
    while True:
        result = callback()
        if predicate(result):
            return True
        else:
            sleep(retry_time_s)
            if tries < max_tries:
                tries += 1
            else:
                return False


def isTrue(param):
    return True == param