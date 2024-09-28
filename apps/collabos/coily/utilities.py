import os
import subprocess
import time
from datetime import datetime, timedelta
from typing import Tuple

import psutil
from webdriver_manager.chrome import ChromeDriverManager
import shutil

from apps.collabos.coily.tune_coily_config import FORMAT_24H, FORMAT_AMPM
from common.framework_params import COILY_USER_CONFIG, TUNE_CALENDAR_CONFIG
from common.platform_helper import get_custom_platform, get_correct_time_format_based_on_system
from config.aws_helper import AWSHelper
from extentreport.report import Report


def prepare_work_account_credentials(account_type):
    try:
        force_download = COILY_USER_CONFIG != 'local'
        credentials = AWSHelper.get_json_config('coily_end_users_v2', force_download=force_download)

        platform = get_custom_platform()
        users = 'COILY_END_USERS'
        return credentials.get(users).get(COILY_USER_CONFIG).get(platform).get(account_type)
    except (KeyError, AttributeError):
        error_message = f"Key '{account_type}' not found in COILY_END_USERS"
        Report.logException(error_message)
    except Exception as e:
        error_message = f"Error retrieving '{account_type}' credentials: {str(e)}"
        Report.logException(error_message)

    return None

def prepare_tune_calendar_account_credentials(account_type):
    try:
        force_download = COILY_USER_CONFIG != 'local'
        credentials = AWSHelper.get_json_config('tune_calendar_end_users', force_download=force_download)
        platform = get_custom_platform()
        return credentials.get('TUNE_CALENDAR_END_USERS').get(TUNE_CALENDAR_CONFIG).get(platform).get(account_type)
    except KeyError:
        error_message = f"Key '{account_type}' not found in TUNE_CALENDAR_END_USERS"
        Report.logException(error_message)
    except Exception as e:
        error_message = f"Error retrieving '{account_type}' credentials: {str(e)}"
        Report.logException(error_message)

    return None

def prepare_ms_api_credentials():
    try:
        credentials = AWSHelper.get_config('tune_calendar_end_users')
        return credentials.MICROSOFT_API_CONFIG
    except Exception as e:
        error_message = f"Error retrieving MICROSOFT_API_CONFIG credentials: {str(e)}"
        Report.logException(error_message)

    return None

def get_time_with_offset(time, hours_offset):
    target_time = time + timedelta(hours=hours_offset)
    if get_custom_platform() == "windows":
        time_format = "%#I:%M %p"
    else:
        time_format = "%-I:%M %p"
    target_time_str = target_time.strftime(time_format)
    return target_time_str


def get_times_with_offset(reservation_start_time: datetime, hours_offset: int, time_format: str
                          ) -> Tuple[str, ...]:
    target_base_time = reservation_start_time + timedelta(hours=hours_offset)

    target_time_0 = target_base_time - timedelta(minutes=1)
    target_time_1 = target_base_time
    target_time_2 = target_base_time + timedelta(minutes=1)

    if target_time_0.day == reservation_start_time.day:
        if time_format == FORMAT_24H:
            t_format = "%H:%M"
        else:
            t_format = get_correct_time_format_based_on_system("%_I:%M %p")
        target_time_1_str = target_time_0.strftime(t_format)
        target_time_2_str = target_time_1.strftime(t_format)
        target_time_3_str = target_time_2.strftime(t_format)
        return target_time_1_str, target_time_2_str, target_time_3_str

    else:
        if time_format == FORMAT_24H:
            return tuple(['00:00'] * 3)
        elif time_format == FORMAT_AMPM:
            return tuple(['12:00 AM'] * 3)


def get_curent_time():
    current_time = datetime.now()
    return current_time

def get_current_time_ampm():
    time_now = datetime.now()
    time_now_minus_1 = time_now + timedelta(minutes=-1)
    time_now_plus_1 = time_now + timedelta(minutes=1)
    if get_custom_platform() == "windows":
        time_str_now = time_now.strftime("%#I:%M %p")
        time_str_minus_1 = time_now_minus_1.strftime("%#I:%M %p")
        time_str_plus_1 = time_now_plus_1.strftime("%#I:%M %p")
    else:
        time_str_now = time_now.strftime("%-I:%M %p")
        time_str_minus_1 = time_now_minus_1.strftime("%-I:%M %p")
        time_str_plus_1 = time_now_plus_1.strftime("%-I:%M %p")
    return time_str_now, time_str_minus_1, time_str_plus_1

def get_current_time_24h():
    time_now = datetime.now()
    time_str_now = time_now.strftime("%H:%M")
    now_plus_1 = time_now + timedelta(minutes=1)
    time_str_plus_1 = now_plus_1.strftime("%H:%M")
    now_minus_1 = time_now + timedelta(minutes=-1)
    time_str_minus_1 = now_minus_1.strftime("%H:%M")
    return time_str_now, time_str_minus_1, time_str_plus_1


def get_current_time(time_format: str):
    if time_format == FORMAT_24H:
        return get_current_time_24h()
    elif time_format == FORMAT_AMPM:
        return get_current_time_ampm()


def get_current_date():
    # Get the current date
    current_date = datetime.now()

    # Format the date without leading zeros for the day
    if get_custom_platform() == "windows":
        formatted_date = current_date.strftime("%A, %B %#d")
    else:
        formatted_date = current_date.strftime("%A, %B %-d")

    return formatted_date

def is_device_connected_over_adb_ip(device_ip):
    try:
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
        output = result.stdout.strip()
        return f'{device_ip}:5555' in output
    except FileNotFoundError:
        return False


def connect_device_over_ip(device_ip, disconnect_existing_adb: bool = True):
    try:
        if disconnect_existing_adb:
            subprocess.run(["adb", "disconnect"], capture_output=True,
                           text=True)  # Disconnect any existing ADB connection
        Report.logInfo(f'Connect device over IP: {device_ip}')
        subprocess.run(["adb", "connect", device_ip], capture_output=True, text=True)  # Connect to the device over IP
        return True
    except Exception:
        return False


def restart_adb_server():
    try:
        Report.logInfo(f'Kill adb server')
        subprocess.run(["adb", "kill-server"], capture_output=True, text=True)
        Report.logInfo(f'Start adb server')
        subprocess.run(["adb", "start-server"], capture_output=True, text=True)
        return True
    except Exception:
        return False


def check_and_connect_device(device_ip, disconnect_existing_adb: bool = True):
    if is_device_connected_over_adb_ip(device_ip):
        Report.logInfo(f"Device is already connected over ADB: {device_ip}")
    else:
        Report.logInfo("Device is not connected over ADB. Connecting over IP...")
        if connect_device_over_ip(device_ip, disconnect_existing_adb=disconnect_existing_adb):
            Report.logInfo(f"Device connected over IP successfully: {device_ip}")
        else:
            Report.logInfo("Failed to connect the device over IP.")


def check_if_device_booted(device_ip: str) -> bool:
    command = f"adb -s {device_ip} shell getprop sys.boot_completed".split(" ")
    res = subprocess.run(command)
    return res.returncode == 0


def restart_adb_device_and_wait_for_boot(device_ip: str, timeout: int = 120):
    time_interval = 10
    retries = int(timeout/time_interval)
    check_and_connect_device(device_ip)
    subprocess.run(f"adb -s {device_ip} reboot".split(" "))

    while not check_if_device_booted(device_ip) and retries > 0:
        time.sleep(time_interval)
        retries -= 1

    if check_if_device_booted(device_ip):
        Report.logInfo("Coily successfully restarted")
    else:
        if retries == 0:
            connect_device_over_ip(device_ip)
            if not check_if_device_booted(device_ip):
                Report.logException("Could not restart the Coily due to timeout")

def restart_scheduler_app_via_adb():
    subprocess.call(f"adb root && adb shell kill -9 $(adb shell pidof -s com.logitech.vc.scheduler)", shell=True)

def remove_chromedriver_folder():
    try:
        folder_path = os.path.dirname(ChromeDriverManager().install())
        shutil.rmtree(folder_path)
        Report.logInfo(f"Folder '{folder_path}' and its contents have been successfully removed.")
    except OSError as e:
        Report.logException(f"Error: Failed to remove folder '{folder_path}'. {e}")

def collect_logcat_logs_over_wifi(device_ip, file_path):
    Report.logInfo(f"Save logcat logs to {file_path}")
    subprocess.call(f"adb -s {device_ip}:5555 logcat -b all -d > {file_path}", shell=True)

def get_system_battery_charging_state():
    Report.logInfo(f"Get power_plugged state")
    battery = psutil.sensors_battery()
    return battery.power_plugged

def is_external_monitor_connected():
    from screeninfo import get_monitors
    if len(get_monitors()) > 1:
        return True
    return False
