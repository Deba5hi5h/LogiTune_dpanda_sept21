"""
:Module Name: **platform_helper**

This module contains all the common test functionality. Different modules will import
this module and use the functions whichever are required.

"""
import logging
import os
import platform
import socket
import subprocess
import sys
import itertools
import random
import re
import cpuinfo
import time as time_time
import string
import requests

from datetime import date, datetime, time, timedelta
from typing import List, Union, Callable, Any

log = logging.getLogger(__name__)
AMD = "AMD"
INTEL = "Intel"
SNAPDRAGON = "Snapdragon"


def get_platform():
    """
    This method gets the name of platform ( operating system)

    :return: ``name of the operating system``
    :rtype: ``string``
    """
    return sys.platform


def get_login():
    """
    Platform independent method for retrieving the login name of the current
    user.

    :return: ``logged in username``
    :rtype: ``string``

    """
    if get_platform().startswith('win'):
        return os.environ.get('USERNAME', 'Unknown')
    else:
        return os.environ.get('USER', 'Unknown')


def get_custom_platform():
    """
    This method gets the custom name of platform ( operating system)

    :return: ``name of the operating system``
    :rtype: ``string``
    """
    _platform = sys.platform
    if _platform.startswith('linux'):
        current_platform = 'linux'
    elif _platform.startswith('darwin'):
        current_platform = 'macos'
    else:
        current_platform = 'windows'

    return current_platform


def get_pc_host_name():
    if get_custom_platform() == 'windows':
        return platform.node().split('.')[0]
    elif get_custom_platform() == 'macos':
        res = subprocess.check_output("scutil --get ComputerName", shell=True, stdin=subprocess.PIPE)
        return res.decode('utf-8').replace('\n', "")
    else:
        return None


def get_current_system_version():
    """
    Method to get platform version e.g. 10 (Windows-10), 11(Windows-11, Mac-11), 12 (Mac-12)
    :return system_version
    """
    if get_custom_platform() == "windows":
        if sys.getwindowsversion().build >= 22000:
            return '11'
        else:
            return '10'
    elif get_custom_platform() == "macos":
        p = subprocess.Popen("sw_vers", stdout=subprocess.PIPE)
        result = p.communicate()[0]
        system_version = 0
        info = result.decode('ascii')
        info_array = info.replace("\n", "_").replace("\t", "").replace(":", "_").split("_")
        for i in range(0, len(info_array)-1):
            if str(info_array[i]).upper() == "PRODUCTVERSION":
                system_version = info_array[i+1].split(".")[0]
                break
        return system_version
    else:
        return None


def get_installer_version():
    from common import config
    settings = config.CommonConfig.get_instance()
    installer_version = settings.get_value_from_section('INSTALLER', 'RUN_CONFIG')
    return installer_version


def get_cpu_vendor():
    """
        Method to get cpu vendor e.g. Intel or AMD
        :return cpu ventor
    """
    vendor = cpuinfo.get_cpu_info()
    brand = vendor.get("brand_raw")
    if get_custom_platform() == "macos":
        return brand
    else:
        brand_lower = brand.lower()
        if "amd" in brand_lower:
            return AMD
        elif "snapdragon" in brand_lower:
            return SNAPDRAGON
        processor_gen = brand.split(" ")[0]
        return f"{INTEL} {processor_gen}"


def get_default_logdirectory():
    """
    This method retrieves the default log directory.

    :return: ``log directory``
    :rtype: ``string``
    """
    try:
        return os.path.join(os.getcwd(), 'testlogs')
    except IOError as io_error:
        raise io_error


def get_pc_name():
    if get_custom_platform() == 'windows':
        return os.environ['COMPUTERNAME']

    elif get_custom_platform() == "macos":
        hostname = socket.gethostname()
        return hostname.split('.')[0]
    else:
        return None


def verify_file_existence(*file_paths: str) -> None:
    """
    Method for checking if file exists in provided directory.

    :return: ``None``
    :rtype: None
    """
    for file_path in file_paths:
        if file_path is not None:
            folder_path, file_name = os.path.split(file_path)
            if not os.path.isfile(file_path):
                raise FileNotFoundError(
                    f'File {file_name} was not found in {folder_path} directory')


def substring_in_iterable(substring: str, *strings: str) -> bool:
    """
    Method for checking whether substring is contained inside iterable.

    :return: ``Info if substring contains inside iterable``
    :rtype: bool
    """
    for current_string in strings:
        if substring in current_string:
            return True
    return False


def change_datetime_to_am_pm_string(timestamp: Union[datetime, time]) -> str:
    """
    Function for changing datetime object to AM PM styled time string without leading zero, eg:
        '9:37 PM', '11:23 AM'
    Args:
        timestamp: datetime/time object
    Returns:
        str - AM PM styled time string
    """
    if get_custom_platform() == "windows":
        time_format = "%#I:%M %p"
    else:
        time_format = "%-I:%M %p"
    return timestamp.strftime(time_format)


def create_dates_list(start_from_date: Union[datetime, date], date_format: str, dates_number: int
                      ) -> List[str]:
    """
    Function for creating list of dates string, formatted by date_format eg:
        'Fri, Feb 02' from '%a, %b %d' formatting
    Args:
        start_from_date: datetime/date from which dates should start counting
        date_format: str format for datetime.strftime to create valid string from datetime object
        dates_number: int of how many dates should be created from starting date

    Returns:
        List[str] - list of dates strings from provided date
    """
    return [(start_from_date + timedelta(days=i)).strftime(date_format)
            for i in range(dates_number)]


def create_am_pm_times_list_until_eod(start_from_time: Union[datetime, time]) -> List[str]:
    """
    Function for creating list of times string, in AM/PM format with 15 minutes interval until
        end of day
    Args:
        start_from_time: datetime/time object from which times should start counting

    Returns:
        List[str] - list of times strings from provided time
    """
    output = list()
    current_time = start_from_time - timedelta(minutes=start_from_time.minute % 15 - 15)
    while current_time.hour > 0:
        output.append(change_datetime_to_am_pm_string(current_time))
        current_time += timedelta(minutes=15)
    return output


def get_all_combinations_from_dict_of_lists(input_dict: dict) -> List[dict]:
    keys = input_dict.keys()
    values = input_dict.values()
    combinations = itertools.product(*values)
    result = [dict(zip(keys, el)) for el in combinations]
    return result


def get_all_values_to_cover_from_dict_of_lists(input_dict: dict) -> List[dict]:
    keys = input_dict.keys()
    values = input_dict.values()

    zipped_values = itertools.zip_longest(*values)
    result_list = []
    for combination in zipped_values:
        result_dict = dict(zip(keys, combination))
        for key, value in result_dict.items():
            if value is None:
                result_dict[key] = random.choice(input_dict[key])
        result_list.append(result_dict)
    return result_list


def change_camel_case_to_snake_case(value: str) -> str:

    pattern = "[aA-zZ][a-z|0-9]*"
    sub_values = re.findall(pattern, value)
    return '_'.join([el.lower() for el in sub_values])


def get_correct_time_format_based_on_system(time_format: str) -> str:
    """
    Function Replaces '_' with either - or # based on current system
    Args:
        time_format: str with wanted time format to strftime
    Returns:
        str - formatted time based on system
    """
    if get_custom_platform() == "windows":
        return time_format.replace('_', '#')
    else:
        return time_format.replace('_', '-')


def tune_time_format_from_datetime_obj(input_time: datetime) -> str:

    return input_time.strftime(get_correct_time_format_based_on_system("%_I:%M %p"))


def set_dark_mode(dark_mode: bool = True) -> None:
    dark_mode_int = int(dark_mode)
    if get_custom_platform() == "windows":
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize", 0,
                            winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, "AppsUseLightTheme", 0, winreg.REG_DWORD, not dark_mode_int)
    else:
        dark_mode_script = (f"osascript -e 'tell app \"System Events\" "
                            f"to tell appearance preferences to set dark mode to {dark_mode_int}'")
        os.system(dark_mode_script)
    time_time.sleep(2)


def get_dark_mode_value() -> bool:
    if get_custom_platform() == "windows":
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize") as key:
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return value == 0
    else:
        result = subprocess.run(["defaults", "read", "-g", "AppleInterfaceStyle"], capture_output=True, text=True)
        output = result.stdout.strip()
        return output == "Dark"


def find_path_in_dict(input_key: str, input_dict: dict, path=None):
    if path is None:
        path = []

    for key, value in input_dict.items():
        new_path = path + [key]
        if key == input_key:
            return new_path
        if isinstance(value, dict):
            result = find_path_in_dict(input_key, value, new_path)
            if result:
                return result


def set_value_in_dict_for_path(input_dict: dict, path: list, value: any) -> None:
    for key in path[:-1]:
        input_dict = input_dict[key]
    input_dict[path[-1]] = value


def get_value_in_dict_for_path(input_dict: dict, path: list) -> any:
    for key in path[:-1]:
        input_dict = input_dict[key]
    return input_dict[path[-1]]


def generate_random_string(length: int) -> str:
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    random_msg = ''.join([random.choice(chars) for _ in range(length)])
    return random_msg


def generate_random_string_with_special_chars(length: int) -> str:
    chars = string.punctuation
    random_msg = ''.join([random.choice(chars) for _ in range(length)])
    return random_msg


def retry_handler(function) -> Callable:
    def wrapper(*args, retry: int = 5, **kwargs) -> Any:
        if retry == 0:
            raise Exception('Retries number exceeded')
        try:
            return function(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            print(f"Retrying request - retry reason: {repr(e)}")
            return wrapper(retry=retry - 1, *args, **kwargs)
    return wrapper


def get_instance(cls):
    return cls()


@get_instance
class retry_request:
    def __getattribute__(self, method: str, *args, **kwargs) -> requests.request:
        if method in ['get', 'post', 'put', 'patch', 'delete']:
            return retry_handler(getattr(requests.api, method))
        else:
            return super().__getattribute__(method, *args, **kwargs)


def check_for_app_installed_macos(app_name: str) -> bool:
    res = subprocess.check_output("system_profiler SPApplicationsDataType", shell=True)
    apps = res.decode("utf-8")
    return f"Location: /Applications/{app_name}.app" in apps


def is_windows_service_running(service_name: str) -> bool:
    command = f'sc query {service_name}'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return b"RUNNING" in output
