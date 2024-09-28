"""
:Module Name: **log_helper**

============================

This module contains the functions to setup the logging

"""
import inspect
import logging
import sys
import os
import time
import common.log_formatter as log_instance
from common.platform_helper import get_default_logdirectory
from common.platform_helper import get_login
from extentreport.report import Report

root = logging.root
log = logging.getLogger('ui_api_tests')
log_repo = ''


def _setup_logging():
    """

    This function is for setting up the log

    :return: ``log directory``
    :rtype: ``string``
    """
    global log_repo
    log_repo = _make_log_dir()
    fmt = log_instance.StdFormatter()
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(fmt)
    root.addHandler(stdout_handler)
    root.setLevel(logging.DEBUG)
    root_logger = log_instance.LogHandler(
        log_repo, 'test.log',
    )
    root_logger.setLevel(logging.DEBUG)
    root.addHandler(root_logger)
    return log_repo


def get_logger(name):
    """
    Get the logger handler with name

    :param name:
    :return:
    """
    return logging.getLogger(name)


def _make_log_dir():
    """
    This function to create the log directory
    """
    log_repository = os.path.join(
        get_default_logdirectory(), get_login(),
        time.strftime('%Y%m%d-%H%M%S'),
    )
    return _make_unique_log_dir(log_repository)


def _make_unique_log_dir(desired_logdir, counter_limit=500):
    """

    This function  makes a unique log directory based on the desired_logdir
    path. Append _n(where n<= 500) to the basename as required to
    make sure we don't overwrite an existing directory.
    """
    log_repo = desired_logdir
    canary_logfile = 'test_misc.log'
    for counter in range(0, counter_limit):
        if counter != 0:
            log_repo = '{}_{:d}'.format(desired_logdir, counter)

        if not os.path.exists(log_repo):
            os.makedirs(log_repo)

        logfile = os.path.join(log_repo, canary_logfile)
        if os.path.exists(logfile):
            continue
        try:
            # Create the file mutually exclusively
            fd = os.open(logfile, os.O_CREAT | os.O_EXCL)
        except OSError:
            # Some other process created the file before we could
            continue
        else:
            # We managed to win the race
            os.close(fd)
            break
    else:
        raise Exception('Unique log directory counter limit exceeded')
    return log_repo


def test_result_logger(tc_id: str, status: bool, error=None):
    """
    Log the test result
    :param tc_id:
    :param status:
    :param error:
    :return:
    """
    try:
        parse_tc_id = tc_id.split('.')[-1]
        result = 'Pass' if status else 'Fail'
        logger_str = '[{}] - {}'.format(
           parse_tc_id, result,
        )

        if error:
            log.error('{} - {}'.format(logger_str, error))
            Report.logFail(logger_str)
            raise error
        else:
            log.info(logger_str)
            Report.logPass(logger_str)

    except Exception as e:
        Report.logException(str(e))
        log.error(e)
        raise e
