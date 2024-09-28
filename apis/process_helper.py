"""

:Module Name: **Process helper**

===============================

Module process utils contains all common helper methods related to
system process

"""
import logging
import subprocess
import sys
import common.config as config
import psutil
import time


log = logging.getLogger(__name__)


def execute_command(cmd, timeout=None):
    """
    This method to execute a command in Terminal

    :param cmd: ``Command to Execute``
    :param timeout: optional timeout of the command in seconds
    :return: popen instance, command stdout, command stderr
    """
    try:
        p_out = subprocess.Popen(
            cmd, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, shell=True,
        )
        (command_output, command_error) = p_out.communicate(timeout=timeout)
        return p_out, command_output, command_error

    except Exception as e:
        log.error('Error found: {}'.format(e))
        raise e


def check_service_running_win(app_name):
    """
    Check a Windows Service App is Running
    :param app_name:
    :return:
    """
    try:
        log.info('app name: %s', app_name)
        logiSync_taklist_cmd = r'C:\\WINDOWS\\system32\\tasklist /FI "Imagename eq {}.exe '.format(
            app_name,
        )
        cmd_output = execute_command(logiSync_taklist_cmd)
        cmd_output = str(cmd_output[1])
        # if no running task are found -1 will be returned
        if 'No tasks are running' in cmd_output:
            return False, -1
        return True, cmd_output.split(r'\r\n')[3].split()[1]

    except Exception as e:
        raise AssertionError('Error in  check_service_running_win : {0}'.format(e))


def kill_app_win(app_name):
    """
    Kill the running service on Windows
    :param app_name:
    :return: True/False
    """
    _status = False
    try:
        process_pid = check_service_running_win(app_name)[1]
        print('PROCESS ID ', process_pid)
        if process_pid == -1:
            _status = False
            raise AssertionError(
                'No process running with name : {}'.format(app_name),
            )
        str_cmd = r'C:\\WINDOWS\\system32\\taskkill /PID /F {}'.format(
            process_pid,
        )
        cmd_output = execute_command(str_cmd)
        match_string = 'PID {} has been terminated'.format(process_pid)
        if not match_string in str(cmd_output[1]):
            raise AssertionError('Error : {}'.format(str(cmd_output[1])))
        _status = True
    except AssertionError as exp:
        log.error(exp)
        raise exp
    finally:
        return _status


def kill_app(app_name):
    """
    Kill a app in Mac
    :param app_name:
    :return:
    """
    try:
        log.info('Killing {}'.format(app_name))
        if sys.platform.startswith('win'):
            return kill_app_win(app_name)
        for proc in psutil.process_iter():
            # check whether the process name matches
            if app_name == proc.name():
                log.info('Killing App {}'.format(proc.name()))
                proc.kill()
                time.sleep(2)
    except Exception as e:
        log.error('Error in  check_service_running_win : {}'.format(e))
        raise e


def check_service_running(sync_service_list):
    """
    Check a Mac Service App is Running
    :param sync_service_list:
    :return:
    """
    # Iterate through the entire Mac Process List
    for proc in psutil.process_iter():
        # check whether the process name matches with sync_service_list
        if proc.name() in sync_service_list:
            # If matches remove that process from List
            sync_service_list.remove(proc.name())

    log.info('Sync Process Status - {}'.format(sync_service_list))

    # If Sync Service List is not empty, return True
    return False if sync_service_list else True


def open_mac_service(app_name):
    """
    This Method is for opening std Mac Services
    open "/Library/Application Support/Logitech/LogiSync/Helpers/LogiSyncProxy.app"
    open "/Library/Application Support/Logitech/LogiSync/Helpers/LogiSyncMiddleware.app"
    open "/Library/Application Support/Logitech/LogiSync/Helpers/LogiSyncHandler.app"
    open "/Applications/Sync.app"
    :param app_name:
    :return:
    """
    try:
        service_names = ['LogiSyncProxy',
                         'LogiSyncMiddleware', 'LogiSyncHandler']
        for service in service_names:
            log.info('Starting the Sync {}'.format(service))
            app_name = '/usr/bin/open -W -n -a "/Library/Application Support/Logitech/LogiSync/Helpers/{}.app"'.format(
                service)
            p_out = subprocess.Popen(
                app_name, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, shell=True,
            )
            log.info('Opening {} Logs {}'.format(service, p_out))
            time.sleep(3)

        log.info('Starting the Logisync App....')
        app_name = '/usr/bin/open -W -n -a /Applications/Sync.app'
        p_out = subprocess.Popen(
            app_name, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, shell=True,
        )

        return p_out
    except Exception as e:
        raise e


def setup_sync_mac():
    try:
        process_list = ['Sync', 'LogiSyncMiddleware', 'LogiSyncProxy']

        status = check_service_running(process_list)
        log.info('LogiSync Running Status {}'.format(status))
        if not status:
            log.info('Restarting LogiSync Service.....')
            time.sleep(10)
            kill_app(process_list)
            check_service_running(process_list)
            time.sleep(10)
            open_mac_service('Sync')
            time.sleep(30)
    except Exception as e:
        raise e


def check_process_status(process_list):
    """
    Method to check status of process running for windows and mac

    :param process_list: ``list of process``
    :return: ``process status dict ``
    """
    try:
        process_status_dict = {i: False for i in process_list}
        # Add .exe at the end in case of windows as per process name
        if sys.platform.startswith('win'):
            process_list = list(map(lambda x: x + '.exe', process_list))

        # Need to start Sync App on Darwin OS
        if sys.platform.startswith('dar'):
            setup_sync_mac()

        # check whether the process name matches with sync_service_list
        for proc in psutil.process_iter():
            # check whether the process name matches with sync_service_list
            if proc.name() in process_list:
                if proc.name().endswith('.exe'):
                    process = proc.name().replace('.exe', '')
                    process_status_dict.update({process: proc.is_running()})
                else:
                    process_status_dict.update(
                        {proc.name(): proc.is_running()})

        return process_status_dict
    except Exception as exp:
        raise exp


def check_sync_service_status():
    """
    Method to call check process status , log service status and return
    False if any one one of the service not running or True if all services
    are running
    :return:  True/False
    """
    try:
        _status_dict = check_process_status(
            config.LOGISYNC_PROCESS_LIST)
        log.info(f'Logi Sync Process Status {_status_dict}')
        if not all(value for value in _status_dict.values()):
            log.error(f'Service running status : {_status_dict}')
            return False
        return True
    except Exception as exp:
        log.error(exp)
        raise exp

