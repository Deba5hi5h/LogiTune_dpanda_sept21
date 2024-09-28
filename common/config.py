import json
import os
import datetime
import configparser
import logging

LOGISYNC_DEVICES = ['rallycamera', 'rally', 'meetup', 'rallybar']
LOGISYNC_WINDOWSx86_PATH = r'C:\Program Files (' \
        r'x86)\Logitech\LogiSync\frontend\Sync.exe'
LOGISYNC_WINDOWS_PATH = r'C:\Program Files\Logitech\LogiSync\frontend\Sync.exe'
MAC_LOGISYNC_VERSION = r'OneAppVersion= mdls -name kMDItemVersion ' \
                           r"/Applications/Sync.app | tr -d \"\";"
MAC_LOGISYNC_PATH = r'../../../binaries/LogiSync/mac'
LOGISYNC_PROCESS_LIST = ['LogiSyncHandler', 'LogiSyncMiddleware', 'LogiSyncProxy']
URL = 'wss://localhost:9506'

log = logging.getLogger(__name__)


class CommonConfig:
    """
    Class contains configs.

    """
    _instance = None

    def __init__(self):
        if CommonConfig._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.config = self._read_config()
            self.config_template = self._read_config_template()
            self.execution_date = datetime.datetime.now().strftime("%Y-%m-%d")
            CommonConfig._instance = self

    @staticmethod
    def get_instance():
        """Returns instance of Config Parser, creates one if doesn't exist."""
        if CommonConfig._instance is None:
            CommonConfig()
        return CommonConfig._instance

    @staticmethod
    def _read_config():
        """Reads file depending on ENV variable and returns correct config."""
        config = configparser.RawConfigParser()
        config_file = "properties.LOCAL"
        directory = os.path.dirname(__file__)
        config.read(os.path.join(directory, config_file))
        return config

    @staticmethod
    def _read_config_template():
        """Reads file depending on ENV variable and returns correct config."""
        config = configparser.RawConfigParser()
        config_file = "properties.TEMPLATE"
        directory = os.path.dirname(__file__)
        config.read(os.path.join(directory, config_file))
        return config

    def get_value_from_section(self, key, section):
        """Returns value from properties file. If value
        depends on ENV variable, correct value returned."""
        try:
            value = self.config.get(section, key)
            return value

        except configparser.NoOptionError as e:
            log.error(f'Please configure properties.LOCAL file: {format(e)}')
            log.error(f'Value for {key} is taken from properties.TEMPLATE file.')
            value = self.config_template.get(section, key)
            return value

    def set_value_in_section(self, section, key, value):
        """Sets value in properties file."""
        try:
            self.config.set(section, key, value)
            config_file = "properties.LOCAL"
            directory = os.path.dirname(__file__)
            with open(os.path.join(directory, config_file), "w+") as configfile:
                self.config.write(configfile)
        except configparser.NoOptionError as e:
            log.error('Please configure properties.LOCAL file: {}'.format(e))
            raise e

    def get_bt_address_from_section(self, key, section):
        """Returns value from properties file. If value
        depends on ENV variable, correct value returned."""
        try:
            tmp_str = self.config.get(section, key)
            tmp_array = tmp_str.split(':')
            value = [int(x, 16) for x in tmp_array]

            return value

        except configparser.NoOptionError as e:
            log.error('Please configure properties.LOCAL file: {}'.format(e))
            raise e



class AntiFlickerConfig:
    """
    Class containing enumeration for anti flicker settings.
    """
    ANTIFLICKER_NTSC_ENUMERATION = 0
    ANTIFLICKER_PAL_ENUMERATION = 1


class DeviceModelConfig:
    """
    Class containing enumeration for device model
    """
    model_unknown = 0
    model_meetup = 1
    model_rally = 20
    model_rally_camera = 21
    model_tap = 22
    model_swytch = 23
    model_rally_bar = 24
    model_generic = 100
    model_rally_bar_mini = 25
    model_scribe = 26
