"""
:Module Name: **log_formatter**

This module contains the classes for log handling

"""
import os
import logging
import time


class LogHandler(logging.FileHandler):
    """
    LogHandler class is for handling logs generation and log file path
    generation

    """
    def __init__(self, logdirectory, filename, level=logging.DEBUG):
        """
        This is method to initialize the the LogHandler

        """
        logdirectory = os.path.abspath(logdirectory)
        if not os.path.exists(logdirectory):
            os.makedirs(logdirectory)
        filename = self.generate_filepath(logdirectory, filename)
        logging.FileHandler.__init__(self, filename, encoding='utf-8')
        self.setLevel(level)
        self.setFormatter(FileFormat())

    @classmethod
    def generate_filepath(cls, logdirectory, filename='lcioutput.log'):
        """
        This method is for log file path generation

        """
        return os.path.join(logdirectory, filename)


class StdFormatter(logging.Formatter):
    """
    StringFormatter class to set the format of the logs captured
    """
    std_format = '%(asctime)s: [%(name)s] {%(levelname)s} %(message)s'

    def __init__(self):
        """
         This is method to initialize the the StdFormatter class
        """
        logging.Formatter.__init__(self, self.std_format)


class FileFormat(StdFormatter):
    """
    FileFormat class to set the format of the log file
    """
    std_format = '%(asctime)s: [%(name)s] {%(levelname)s} %(message)s'

    def formatTime(self, record, datefmt=None):
        """
       This method is to set the format of the date and time
       """
        if datefmt:
            format_time = StdFormatter.formatTime(self, record, datefmt)
        else:
            time_struct = self.converter(record.created)
            format_time = time.strftime("%Y-%m-%d %H:%M:%S.{:03.0f}  "
                                        "%Z".format(record.msecs), time_struct)
        return format_time
