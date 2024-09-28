import logging
import os
from typing import List

from common.aws_s3_utils import AwsS3Utils

TUNE_FIRMWARE_BUCKET = "qa-auto-repo/LogiTune"
log = logging.getLogger(__name__)


class FirmwareDownloader:
    """Class containing methods to download files from different s3 buckets."""

    def get_firmware_file_for_logitune(self, device: str, file_path: str) -> None:
        """Method to download LogiTune firmware file from specified S3 bucket.

        @param device: device name folder from S3
        @param file_path: destination file path
        @return:
        """
        try:
            assert self.download_file_from_s3(
                f"{TUNE_FIRMWARE_BUCKET}/{device}", file_path
            )
            log.info("File successfully downloaded.")
        except Exception as ex:
            log.error("Not possible to download file from S3.")
            raise ex

    def prepare_firmware_files_for_test(self, s3_bucket_name: str, *paths: str) -> None:
        """Method to download LogiTune list of firmware files from specified S3 bucket.

        @param s3_bucket_name: S3 bucket path
        @param paths: paths to firmware files
        @return:
        """
        for file_path in paths:
            try:
                if not os.path.isfile(file_path):
                    self.get_firmware_file_for_logitune(s3_bucket_name, file_path)
            except Exception as ex:
                log.error(str(ex))
                raise ex

    def download_file_from_s3(self, bucket: str, file_path: str) -> bool:
        """Method to download specific file from S3 bucket and save it specified location.

        @param bucket: S3 bucket path
        @param file_name: file name to download
        @return: True is files exists after download, False otherwise
        """
        try:
            dir_path = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)

            log.info(
                f"Start downloading Logi Tune app {file_name} from S3 to {dir_path}."
            )

            prefix = f"{bucket}/{file_name}"
            awsutils = AwsS3Utils()
            awsutils.download_from_S3(f"{prefix}", destination=dir_path)
            return os.path.isfile(file_path)
        except Exception as ex:
            log.error("Not possible to download file from S3.")
            raise ex
