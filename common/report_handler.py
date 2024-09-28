import collections
import datetime
import os
import threading
import time

import requests

from common.framework_params import JENKINS_SVC_RUNNER


MAIN_SERVER_ADDRESS = 'http://swqa-dashboard:8000/'


class ReportFilesUpload:
    def __init__(self, main_upload_folder: str, file_name: str, report_folder_name: str):
        self._main_upload_folder = main_upload_folder
        self._file_name = file_name
        self._report_folder_name = report_folder_name
        self.response = None

    def _upload_file(self, retry: int = 5) -> requests.Response:
        try:
            with open(self._file_name, 'rb') as file:
                return requests.put(
                    _create_endpoint(f'upload_file/{self._main_upload_folder}/{self._report_folder_name}'),
                    files={'file': file},
                    timeout=60
                )
        except requests.exceptions.RequestException as e:
            if retry <= 0:
                raise e
            time.sleep(1)
            print(f'[{datetime.datetime.now()}] File "{self._file_name}" - {repr(e)} - '
                  f'retrying {retry - 1} more times')
            return self._upload_file(retry=retry - 1)

    def upload_file(self) -> requests.Response:
        self.response = self._upload_file()
        return self.response

    def valid_upload(self) -> bool:
        if self.response.status_code == 200 and self.response.json().get('status') == 'OK':
            return True
        else:
            return False


def _create_endpoint(endpoint: str) -> str:
    return f'{MAIN_SERVER_ADDRESS}{endpoint}'


def verify_server_is_up() -> bool:
    try:
        response = requests.get(MAIN_SERVER_ADDRESS)
        if response.ok:
            return True
        else:
            print(f'Invalid response from "{MAIN_SERVER_ADDRESS}" - '
                  f'[{response.status_code}] {response.text}')
            return False
    except requests.exceptions.ConnectionError as e:
        if 'Errno 8' in str(e):
            print(f'Probably host address "{MAIN_SERVER_ADDRESS}" is not visible in current network. '
                  f'Please check if /etc/hosts have valid domain created - {e}')
        else:
            print(f'Unable to get response from "{MAIN_SERVER_ADDRESS}" - {e}')
        return False
    except Exception as e:
        print(f'Unable to get response from "{MAIN_SERVER_ADDRESS}" - {e}')
        return False


def create_report_folder(main_folder: str, folder_name: str) -> requests.Response:
    return requests.post(_create_endpoint(f'create_dir/{main_folder}'), json={'name': folder_name})


def upload_files_from_directory(source_folder: str, main_upload_folder: str, report_folder_name: str) -> None:
    if JENKINS_SVC_RUNNER:
        upload_files_from_directory_one_by_one(source_folder, main_upload_folder, report_folder_name)
    else:
        upload_files_from_directory_in_batches(source_folder, main_upload_folder, report_folder_name)


def upload_files_from_directory_one_by_one(source_folder: str, main_upload_folder: str,
                                           report_folder_name: str) -> None:
    not_uploaded = list()
    for idx, data in enumerate(os.listdir(source_folder)):
        full_data = os.path.join(source_folder, data)
        response = ReportFilesUpload(main_upload_folder, full_data, report_folder_name).upload_file()
        if response.status_code != 200:
            print(f'[{datetime.datetime.now()}] {idx:>3d}|{len(os.listdir(source_folder)):<3d} '
                  f'Problem with uploading file "{data}": {response.status_code} - {response.text}')
            not_uploaded.append(data)
        if idx % 100 == 0:
            print(f'[{datetime.datetime.now()}] {idx:>3d}|{len(os.listdir(source_folder)):<3d} '
                  f'Files uploaded')
    if not_uploaded:
        print(f'[{datetime.datetime.now()}] Not all files uploaded correctly '
              f'({len(not_uploaded)}): {not_uploaded}')
    else:
        print(f'[{datetime.datetime.now()}] All files uploaded!')


def upload_files_from_directory_in_batches(source_folder: str, main_upload_folder: str, report_folder_name: str,
                                           batch_size: int = 25) -> None:
    files = os.listdir(source_folder)
    queue = collections.deque([(os.path.join(source_folder, data), data) for data in files])
    print(f'[{datetime.datetime.now()}] Trying to upload {len(queue)} files to report server')
    uploaders = list()
    start_time = time.time()
    while queue:
        active_threads = list()
        for _ in range(min(batch_size, len(queue))):
            full_data, data = queue.popleft()
            uploader = ReportFilesUpload(main_upload_folder, full_data, report_folder_name)
            uploaders.append(uploader)
            t = threading.Thread(target=uploader.upload_file, name=data)
            t.daemon = True
            active_threads.append(t)
            t.start()

        while [t for t in active_threads if t.is_alive()]:
            time.sleep(0.1)
        if time.time() - start_time > 5:
            start_time = time.time()
            print(f'[{datetime.datetime.now()}] {len(queue) + batch_size} files left to upload')

    if all([uploader.valid_upload() for uploader in uploaders]):
        print(f'[{datetime.datetime.now()}] All files uploaded successfully!')
    else:
        failed_uploads = [uploader for uploader in uploaders if not uploader.valid_upload()]
        print(f'[{datetime.datetime.now()}] Some files failed to upload ({len(failed_uploads)}):'
              f'{failed_uploads}')
