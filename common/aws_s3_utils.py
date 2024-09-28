# Copyright (c) 2020 Logitech Inc.
# All rights reserved
"""
:Module Name: **AWSS3Utils**

Aws S3 Utils module will have method implementation for downloading files
from the S3 bucket.
In order to download from S3 bucket we need to use method
:meth:`download_from_S3 <vc.common.aws_s3_utils.AwsS3Utils.download_from_S3>`

.. note::
   It expects AWS credentials to be pre-configured at .aws
   folder location. For more details on how to configure aws credentials
   visit : https://docs.aws.amazon.com/amazonswf/latest/awsrbflowguide/set-up-creds.html

"""
import json
import time
from typing import Optional

import boto3
import os
import logging

import botocore

from common.aws_wrappers import Boto3Wrapper
from common.platform_helper import get_custom_platform

log = logging.getLogger(__name__)


class AwsS3Utils(Boto3Wrapper):
    """
    Class AwsUtil has methods related to downloading files from AWS- S3 bucket
    """
    def __init__(self, aws_config_file=None):
        """
        Init method

        """
        Boto3Wrapper.__init__(self, aws_config_file=aws_config_file)

        self.client = self.init_boto_client('s3')
        self.resource = self.init_boto_session().resource('s3')

    @staticmethod
    def download_from_S3(source, destination, overwriteFlag=True):
        """
        Public method wrapper for download from s3. It can accept source as
        single file or list of files/folders, and destination as single
        folder or list of folders  refer to below example of usage.
        Overwrite can be set to false if user do not want to download each
        time if file exist (default set to True).

        :param source: ``source file/folder list or string``
        :param destination: ``destination folder or folder list``
        :param overwriteFlag: ``Overwrite File flag True/False``

        .. code-block:: python

            # Example 1 - Source is a single file and Destination is folder
            source = 'vc-sw-release/vcautoinfra_helpers/Sync/old_binaries/
            RallyCamera/Windows/FWUpdateRallyCamera_DEV.exe',
            destination = 'binaries/Sync/old_binaries/Win/'
            AwsS3Utils.download_from_S3(source, destination)
            # Example 2 - Source is list of files & destination is single folder
            source = ['vc-sw-release/vcautoinfra_helpers/Sync/old_binaries
            /RallyCamera/Windows/FWUpdateRallyCamera_DEV.exe',
            'vc-sw-release/vcautoinfra_helpers/Sync/ffmpeg_exes/Windows/ffmpeg.exe']
            destination = 'binaries/Sync/old_binaries/Win/'
            AwsS3Utils.download_from_S3(source, destination)
            # Example 3 - Source & Destination both are list of folders
            source = ['vc-sw-release/vcautoinfra_helpers/Sync/old_binaries/RallyCamera/',
            'vc-sw-release/vcautoinfra_helpers/Sync/ffmpeg_exes/Windows/ffmpeg.exe']
            destination = ['binaries/Sync/old_binaries/Win/Rallycamera/',
            'binaries/Sync/old_binaries/Win/ffmpeg_exes/]
            AwsS3Utils.download_from_S3(source, destination)

        """
        s3obj = AwsS3Utils()
        return s3obj._download_s3_wrapper(source, destination, overwriteFlag)

    def find_prefix_with_valid_tune_version(self, app_version: str) -> Optional[str]:
        """
        Method for finding valid S3 bucket path for provided Logi Tune version

        :param app_version: ``[str] Logi Tune version``
        """
        bucket_info = {
            'Bucket': 'vc-sw-release',
            'Prefix': 'vc-apps-tune/',
            'Delimiter': '/',
        }
        objects = self.client.list_objects(**bucket_info)
        paginator = self.client.get_paginator('list_objects')
        for json_object in objects.get('CommonPrefixes'):
            bucket_info['Prefix'] = json_object.get('Prefix')
            page_iterator = paginator.paginate(**bucket_info)
            for tune_versions in page_iterator:
                for versions in tune_versions.get('CommonPrefixes'):
                    current_path = versions.get('Prefix')
                    if app_version in current_path:
                        log.info(f'Found Logi Tune {app_version} in path: {current_path}')
                        return current_path
        log.info(f'Logi Tune {app_version} was not found on S3 bucket!')
        return None

    def find_prefix_with_latest_tune_version(self, app_version: str) -> Optional[str]:
        """
        Method for finding valid S3 bucket path for provided Logi Tune version

        :param app_version: ``[str] Logi Tune version``
        """
        bucket_info = {
            'Bucket': 'vc-sw-release',
            'Prefix': 'vc-apps-tune/',
            'Delimiter': '/',
        }
        objects = self.client.list_objects(**bucket_info)
        paginator = self.client.get_paginator('list_objects')
        data = dict()
        for json_object in objects.get('CommonPrefixes'):
            bucket_info['Prefix'] = json_object.get('Prefix')
            page_iterator = paginator.paginate(**bucket_info)
            for tune_versions in page_iterator:
                for versions in tune_versions.get('CommonPrefixes'):
                    current_path = versions.get('Prefix')
                    data[current_path.split('/')[2]] = current_path
        sorted_data = dict()

        for item_data in data:
            if item_data.startswith(app_version.lower().replace('.x', '')):
                sorted_data[int(item_data.split('.')[2])] = data[item_data]

        bucket_info['Prefix'] = sorted_data.get(max(sorted_data.keys()))
        custom_platform = 'mac' if get_custom_platform() == 'macos' else 'windows'
        for i in range(100):
            page_iterator2 = paginator.paginate(**bucket_info)
            for os_type in page_iterator2:
                if len(os_type.get('CommonPrefixes')) > 1:
                    return bucket_info['Prefix']
                elif custom_platform in os_type.get('CommonPrefixes')[0].get('Prefix').split('/')[3]:
                    return bucket_info['Prefix']
            bucket_info['Prefix'] = sorted_data.get(max(sorted_data.keys())-i-1)
        return None

    def find_prefix_with_tune_version(self, app_version: str) -> Optional[str]:
        if 'x' in app_version:
            return self.find_prefix_with_latest_tune_version(app_version)
        return self.find_prefix_with_valid_tune_version(app_version)

    def get_newest_version_tune_desktop_version_for_project(self, project_version: str):

        bucket_name = 'vc-sw-release'
        prefix = f'vc-apps-tune/{project_version}/'
        delimiter = '/'

        # Create a reusable Paginator
        paginator = self.client.get_paginator("list_objects_v2")

        # Create a PageIterator from the Paginator
        page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

        # Extract versions from the objects
        versions = []
        for page in page_iterator:
            for obj in page.get('Contents', []):
                key = obj['Key']
                key_parts = key.split(delimiter)
                if len(key_parts) > 2:
                    try:
                        versions.append(int(key_parts[2][4:]))
                    except:
                        print(f"Could not parse {key_parts[2]}")

        # Sort the versions
        if versions:
            versions.sort(reverse=True)
            print(f"DEBUG: All available versions: {versions}")

            # get highest version and add prefix '3.6.' back
            parts = project_version.split('.')
            prefix = '.'.join(parts[:2]) + '.'

            for version in versions:
                (platform, file_name) = ('windows', 'LogiTuneInstall.exe') if get_custom_platform() == 'windows' else ('mac', 'LogiTuneInstaller.pkg')

                file_path = f'vc-apps-tune/{project_version}{delimiter}{prefix}{version}/{platform}/{file_name}'

                # Check if the object/file exists
                try:
                    self.client.head_object(Bucket=bucket_name, Key=file_path)
                    return prefix + str(version)
                except botocore.exceptions.ClientError:
                    # The file does not exist.
                    continue

            return None

        else:
            return None

    def find_prefix_with_valid_tune_mobile_version(self, app_version: str) -> Optional[str]:
        """
        Method for finding valid S3 bucket path for provided Tune Mobile App version

        :param app_version: ``[str] Tune Mobile App version``
        """
        bucket_info1 = {
            'Bucket': 'vc-sw-release',
            'Prefix': 'LogiTune/mbg-mulberries-android/',
            'Delimiter': '/',
        }
        bucket_info2 = bucket_info1
        objects = self.client.list_objects(**bucket_info1)
        paginator = self.client.get_paginator('list_objects')
        page_iterator = paginator.paginate(**bucket_info1)
        for versions in page_iterator:
            for versions in versions.get('CommonPrefixes'):
                current_path = versions.get('Prefix')
                objects = self.client.list_objects(**bucket_info1)
                if app_version in current_path:
                    print()
                for json_object in objects.get('CommonPrefixes'):
                    bucket_info1['Prefix'] = json_object.get('Prefix')
                    page_iterator1 = paginator.paginate(**bucket_info1)
                    for folders in page_iterator1:
                        for folders in folders.get('CommonPrefixes'):
                            folder_path = folders.get('Prefix')
                            if app_version in folder_path:
                                bucket_info2['Prefix'] = folder_path
                                page_iterator2 = paginator.paginate(**bucket_info2)
                                for prod in page_iterator2:
                                    for prod in prod.get('CommonPrefixes'):
                                        prod_path = prod.get('Prefix')
                                        if "prod" in prod_path:
                                            return prod_path
        log.info(f'Tune Mobile App {app_version} was not found on S3 bucket!')
        return None

    def _download_files_from_s3(self, source, destination, overwrite):
        """
        Method to download the folders from s3 bucket to local system (
        Folder and sub folder structure in s3 bucket as maintained same in
        local system
        after downloading)

        :param source: ``url including bucket name and prefix pattern to download``
        :param destination: ``local path to folder in which files to place``
        :param overwrite: ``Flag for overwrite file``
        """
        try:
            # Getting the bucket name from source url
            bucket = source.split('/')[0]
            # Getting the prefix pattern to match in s3 bucket
            prefix = source.replace(bucket+"/", "")
            base_kwargs = {
                'Bucket': bucket,
                'Prefix': prefix,
            }
            file_list, dir_list = [], []
            next_token = ''
            while next_token is not None:
                kwargs = base_kwargs.copy()
                if next_token != '':
                    kwargs.update({'ContinuationToken': next_token})
                # list all the folders/files in s3
                results = self.client.list_objects_v2(**kwargs)
                contents = results.get('Contents')
                assert contents is not None,\
                    f'No files available to download in S3 bucket Path : [' \
                    f'{ source }]'
                # contents length is 1 means single file available to download
                if len(contents) == 1:
                    filename = contents[0].get('Key').split('/')[-1]
                    # Create the destination folder if doesn't exist
                    if not os.path.exists(destination):
                        os.makedirs(destination)
                    destination = os.path.join(destination, filename)
                    self._check_overwrite_status_and_download(bucket,
                                                              destination,
                                                              prefix, overwrite)
                    return True
                # Get the files and directories from s3 bucket
                else:
                    for content in contents:
                        file = content.get('Key')
                        if file[-1] != '/':
                            file_list.append(file)
                        else:
                            dir_list.append(file)
                    next_token = results.get('NextContinuationToken')
                    # Stripping the folder which we do not need in local system
                    folder_to_strip = prefix
                    is_file_or_dir = self._is_file_or_dir(source,
                                                          folder_to_strip)
                    if is_file_or_dir[0] is True and is_file_or_dir[1] == \
                            'is_Dir':
                        # Append / if missing from folder to strip
                        if folder_to_strip[-1] != '/':
                            folder_to_strip = folder_to_strip + '/'
                    # creating the folder structure in local system
                    for d in dir_list:
                        if not d == folder_to_strip:
                            replace_strip_path = d.replace(folder_to_strip, '')
                            dest_path = os.path.join(destination,
                                                     replace_strip_path)
                            if not os.path.exists(os.path.dirname(dest_path)):
                                os.makedirs(os.path.dirname(dest_path))
                    # downloading binaries into local system folders
                    for file_key in file_list:
                        replace_strip_path = file_key.replace(folder_to_strip, '')
                        dest_path = os.path.join(destination, replace_strip_path)
                        if not os.path.exists(os.path.dirname(dest_path)):
                            os.makedirs(os.path.dirname(dest_path))
                        # download the file and keept it in destination folder
                        log.debug(f'File download in queue : {file_key}')
                        self._check_overwrite_status_and_download(bucket, dest_path, file_key,
                                                                  overwrite)
                    return True
        except Exception as err:
            raise err

    def _check_overwrite_status_and_download(self, bucket, file_path,
                                             file_key, overwrite):
        """
        Method to handle the overwrite Flag, If True will download the file
        always and if set to false will download file only if it's unavailable

        """
        try:
            is_empty = self._get_size(bucket, file_key)
            if is_empty == 0:
                raise Exception("The Given Path is Empty or Does Not Exists "
                                "in S3")
            # case overwrite false, and destination path not exists
            if not overwrite and not os.path.exists(file_path):
                log.info(f'Downloading file : {file_key}')
                self.client.download_file(bucket, file_key, file_path)
            # case overwrite true, always replace
            elif overwrite:
                log.info(f'Downloading file : {file_key}')
                self.client.download_file(bucket, file_key, file_path)
            # case overwrite flag is marked as false and file exists
            else:
                log.info(f'Overwrite flag is set to False, and file '
                         f'{file_path} exists')
        except Exception as ge:
            log.error(f'Exception found in '
                      f'_check_overwrite_status_and_download method')
            raise ge

    def _download_s3_wrapper(self, source, destination, overwrite):
        """
        This is wrapper method to download from s3 from given source file or
        folder and place it in destination folder.
        It accepts argument as mentioned below
        source can be single file or folder or a list of files or folder
        destination can be a single folder or list of folder corresponding
        each of entries in source list.

        :param source: ``list source file or folder``
        :param destination: ``list of destination folder``
        :param overwrite: ``Flag for overwrite file``
        """
        # Check of single file/folder is provided or a list
        try:
            # check if source and destination is not empty or None
            assert source and destination, 'Source or Destination can not be ' \
                                           'empty or None'
            # case source and destination is a string file/folder
            if not isinstance(source, list) and not isinstance(destination,
                                                               list):
                log.debug(f'Source: {source} Destination : {destination}')
                _status = self._download_files_from_s3(source, destination,
                                                       overwrite=overwrite)
                return _status
            # case source and destination is list
            if isinstance(destination, list) and len(source) == len(
                    destination):
                for src, dest in zip(source, destination):
                    log.debug(f'Source: {source} Destination : {destination}')
                    self._download_files_from_s3(src, dest, overwrite=overwrite)
            # case source and destination is list but lenght is un - equal
            elif isinstance(destination, list) and len(source) != len(
                    destination) and len(destination) != 1:
                err_str = 'Mis-match in source and destination list length'
                raise Exception(err_str)
            # case where all src files to be copied to same destination folder
            else:
                # convert to string if destination is passed as a list input
                destination = ''.join(destination)
                for each in source:
                    log.debug(f'Source: {source} Destination : {destination}')
                    self._download_files_from_s3(each, destination,
                                                 overwrite=overwrite)
        except Exception as exp:
            log.error(exp)

    def _is_file_or_dir(self, source, key):
        """
        Checks whether a downloading element is a file or directory

        :source: ``path of the file or dir``
        :key: ``path to filter out required source contents``
        """
        # get bucket name
        bucket_name = source.split('/')[0]
        # connect with the bucket
        bucket = self.resource.Bucket(bucket_name)
        objs = list(bucket.objects.filter(Prefix=key))
        # check if path is directory or file
        if len(objs) == 1 and objs[0].key == key:
            return True, "is_File"
        elif len(objs) > 1:
            return True, "is_Dir"
        else:
            return False

    def _get_size(self, bucket, source):
        """
        Calculates the total size of a file or folder in S3
        :param bucket: bicket name
        :param source: source path
        :return: total size of a file or folder
        """
        try:

            # Connects to the bucket
            my_bucket = self.resource.Bucket(bucket)
            total_size = 0
            for obj in my_bucket.objects.filter(Prefix=source):
                total_size = total_size + obj.size
            return total_size
        except Exception as ge:
            log.error(f'Exception found in _get_size_of_file method')
            raise ge


if __name__ == '__main__':
    aws = AwsS3Utils()
    print(aws.find_prefix_with_latest_tune_version('99.15.x'))
