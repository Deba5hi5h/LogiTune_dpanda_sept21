import os
import re
import subprocess
import sys

import inspect
from typing import Any, Optional

from base.base_settings import TUNES_APP_PATH_WIN, TUNES_APP_PATH_WIN_NEW
from common.platform_helper import get_custom_platform
from extentreport.report import Report


def exception_handler(function) -> Any:
    """Decorator which handles unexpected exception
        Args:
            function: Function to check
        Returns:
            Any
    """

    def wrapper(*args, **kwargs) -> Any:
        try:
            return function(*args, **kwargs)
        except Exception as ex:
            sig = inspect.signature(function)
            bound_arguments = sig.bind(*args, **kwargs)
            if kwargs.get('skip_exception') is not True:
                Report.logException(f'Exception in {function.__name__}: {repr(ex)} - {ex}'
                                    f'called with {"<br>".join([f"{argument}: {value}" for argument, value in bound_arguments.arguments.items()])}')
    return wrapper


def get_python_version() -> int:
    """
    Returns the version of the Python interpreter as an integer.

    Returns:
        int: The version of the Python interpreter. For example, if the Python version is 3.9.x,
             the return value would be 309.
    """
    return int(f'{sys.version_info[0]}{sys.version_info[1]:02d}')


def return_valid_windows_logi_tune_path() -> str:
    old_path = os.path.join('C:', os.sep, 'Program Files (x86)', 'Logitech', 'LogiTune')
    new_path = os.path.join('C:', os.sep, 'Program Files', 'Logitech', 'LogiTune')
    return old_path if os.path.isdir(old_path) else new_path


def get_logitune_version_macos() -> Optional[str]:
    tunes = (r'Logi\ Tune', r'LogiTune')
    for tune in tunes:
        try:
            response = subprocess.check_output(
                f"mdls -name kMDItemVersion /Applications/{tune}.app",
                shell=True
            )
        except subprocess.CalledProcessError:
            continue
        version = response.decode("utf-8")
        return re.search('\"(.*)\"', version)[1]


def get_logitune_version_windows() -> Optional[str]:
    if os.path.exists(TUNES_APP_PATH_WIN_NEW):
        valid_path = TUNES_APP_PATH_WIN_NEW
    elif os.path.exists(TUNES_APP_PATH_WIN):
        valid_path = TUNES_APP_PATH_WIN
    else:
        print('Logi Tune not found, it might not be installed')
        return None
    valid_path = valid_path.replace('\\', '\\\\')
    response = subprocess.check_output(
        f'wmic datafile where name="{valid_path}" get Version /value',
        shell=True
    )
    version = response.decode("utf-8").strip().split('=')[1]
    return version


def get_logitune_version() -> Optional[str]:
    if get_custom_platform() == 'macos':
        return get_logitune_version_macos()
    else:
        return get_logitune_version_windows()
