import logging
import os
import sys
import time
from zipfile import ZipFile

import boto3
from botocore.exceptions import ClientError

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BUCKET_NAME = 'vc-sw-release'

audio_bucket = "Kong/Kong-Audio-Zynq/master"
audio_name_prefix = "FITImage-"
audio_name_suffix = ".itb"
pt_bucket = "Kong/Video/STM32_PT_firmware/master"
pt_file_name = "KongPanTilt.bin"
hk_bucket = "Kong/HouseKeeping/master"
hk_file_name = "stmHkFW.bin"
zf_bucket = "Kong/Video/STM32_ZF_firmware/master"
zf_file_name = "KongZoomFocus.bin"
KONG_BUILD_PREFIXES = ["kong-collabos-1.2.x", "kong-collabos1.1", "kong-launch", "kong-day0", "kdl-07600", "kong-mtr", "kong-collabos1.2-factory"]

log = logging.getLogger(__name__)


class AwsUtils(object):

    def __init__(self):
        self.adb_devices = []
        self.__s3_resource = boto3.resource('s3')
        self.__s3_client = boto3.client('s3')

    def get_kong_bucket_by_build_version(self, version, is_user_debug, is_signed):
        if is_signed:
            build_ver = (version + '/secure-signed-build/' + "0UWW.zip") if is_user_debug else (version + '/secure-signed-build/' + "00WW.zip")
        else:
            build_ver = (version + '/' + "0UWW.zip") if is_user_debug else (version + '/' + "00WW.zip")

        paginator = self.__s3_client.get_paginator("list_objects_v2")

        for prefix in KONG_BUILD_PREFIXES:
            page_iterator = paginator.paginate(Bucket=BUCKET_NAME, Prefix='Kong/SystemImage/'+prefix)

            for page in page_iterator:
                if "Contents" in page:
                    for key in page["Contents"]:
                        keyString = key["Key"]
                        if build_ver in keyString:
                            return keyString
        log.debug("Bucket: " + version + " not found")
        return False

    def get_apks_entries_from_bucket(self, bucket_name, prefix):
        s3 = self.__s3_resource
        bucket = s3.Bucket(name=bucket_name)
        filtered_objects = bucket.objects.filter(Prefix=prefix)
        if sum(1 for _ in filtered_objects) == 0:
            log.debug("No apps found in this S3 bucket")
            return False
        return filtered_objects

    def find_apk_by_detailed_version(self, bucket_name, prefix, version):
        res = self.get_apks_entries_from_bucket(bucket_name, prefix)

        if res:
            for obj in res:
                if version in obj.key:
                    return obj.key
        return False

    def download_apk_from_s3(self, bucket, key, apk, retry_on_failure):
        s3 = self.__s3_resource

        max_attempts = 10 if retry_on_failure else 1
        wait_period = 180   # number of seconds
        for attempt in range(max_attempts):
            try:
                s3.Bucket(bucket).download_file(key, apk)
                return True
            except ClientError as e:
                if e.response['Error']['Code'] == "404":
                    log.debug('Attempt ' + str(attempt) + ': File not found in S3. ' + key + ' Destination: ' + apk)
                    if attempt < max_attempts - 1:  # zero-indexed
                        time.sleep(wait_period)
                        continue
                    else:
                        sys.exit('File not found in S3. ' + key)
                else:
                    raise


class DownloadImages:

    @staticmethod
    def get_component_file_properties(component, version):
        full_folder = None
        file_name = None
        destination_file_name = None

        if "hk" in component.lower():
            file_name = hk_file_name
            full_folder = f'{hk_bucket}/{version}/'
            destination_file_name = f"HK_{version}.bin"
        elif "zf" in component.lower():
            file_name = zf_file_name
            full_folder = f'{zf_bucket}/{version}/'
            destination_file_name = f"ZF_{version}.bin"
        elif "pt" in component.lower():
            file_name = pt_file_name
            full_folder = f'{pt_bucket}/{version}/'
            destination_file_name = f"PT_{version}.bin"
        elif "audio" in component.lower():
            file_name = audio_name_prefix + version + audio_name_suffix
            full_folder = f'{audio_bucket}/{version}/'
            destination_file_name = f"Audio_{version}.itb"

        return full_folder, file_name, destination_file_name

    def download_component_by_version(self, component, version):
        file_suffix = "itb" if component == 'Audio' else 'bin'

        file_path = f"{BASE_DIR}/files/{component}_{version}.{file_suffix}"

        log.debug(f"is file: {os.path.isfile(file_path)}")
        if not os.path.isfile(file_path):
            full_folder, file_name, destination_file_name = self.get_component_file_properties(component, version)

            if full_folder:
                utils = AwsUtils()
                file = utils.find_apk_by_detailed_version(BUCKET_NAME, full_folder, file_name)
                if file:
                    utils.download_apk_from_s3(BUCKET_NAME, file, BASE_DIR + "/files/" + destination_file_name,
                                               False)
                    log.debug(f"Downloaded as: {BASE_DIR}/files/{destination_file_name}")
                    return True
                log.debug(f"File: {file_name} not found on S3")
                return False
            return False
        return True

    def __download_android_build(self, version, is_debug_build, is_signed):
        utils = AwsUtils()
        full_s3_folder_path = utils.get_kong_bucket_by_build_version(version, is_debug_build, is_signed)
        if full_s3_folder_path:
            folder_path_splitted = full_s3_folder_path.split("/")
            if is_signed:
                destination_file_name = f'SSB_{folder_path_splitted[-1].split(".")[0]}_{folder_path_splitted[-3]}.zip'
            else:
                destination_file_name = f'{folder_path_splitted[-1].split(".")[0]}_{folder_path_splitted[-2]}.zip'
            utils.download_apk_from_s3(BUCKET_NAME, full_s3_folder_path, BASE_DIR + "/files/" + destination_file_name,
                                       False)
            log.debug(f"Downloaded as: {BASE_DIR}/files/{destination_file_name}")
            return True
        return False

    def download_and_unzip_android_image(self, version, is_debug_build=True, is_signed=False):
        if is_debug_build:
            zip_prefix = "0UWW"
        else:
            zip_prefix = "00WW"

        if is_signed:
            file_name = f"SSB_{zip_prefix}_{version}"
        else:
            file_name = f"{zip_prefix}_{version}"

        if is_debug_build:
            zip_path = f"{BASE_DIR}/files/{file_name}.zip"
            dir_path = f"{BASE_DIR}/files/{file_name}"
        else:
            zip_path = f"{BASE_DIR}/files/{file_name}.zip"
            dir_path = f"{BASE_DIR}/files/{file_name}"

        if not os.path.isdir(dir_path):
            if not os.path.isfile(zip_path):
                log.debug(f"Download Android file")
                if not self.__download_android_build(version, is_debug_build, is_signed):
                    return False
                log.debug(f"Android file downloaded")
            with ZipFile(zip_path, 'r') as zip_ref:
                log.debug(f"Extract Android file")
                zip_ref.extractall(dir_path)
                log.debug(f"Android file extracted")
                return True
        return True

if __name__ == "__main__":
    d = DownloadImages()
    d.download_and_unzip_android_image("0.904.267", is_signed=True)