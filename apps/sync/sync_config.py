import time

SYNC_TIMEOUT = 90
base_driver = None
SYNC_APP_PATH_WIN = "C:\\Program Files (x86)\\Logitech\\LogiSync\\frontend\\Sync.exe"
SYNC_APP_PATH_MAC = '/Applications/Sync.app/Contents/MacOS/Sync'

RIGHT_SIGHT_URL = "https://www.logitech.com/en-us/video-collaboration/resources/rightsense-technology.html"
RALLY_WHERE_SHOULD_I_PLACE_COMPUTER_URL = "https://www.logitech.com/content/dam/logitech/vc/en/pdf/helpful-guidelines-for-setting-up-a-video-meeting-space.pdf"

RALLY_SYSTEM_DOESNT_SEE_DEVICE_URL = "https://support.logi.com/hc/en-us/articles/360024325453"
RALLY_CAMERA_SYSTEM_DOESNT_SEE_DEVICE_URL = "https://support.logi.com/hc/en-us/articles/360024151434"
MEETUP_DOESNT_SEE_DEVICE_URL = "https://support.logi.com/hc/en-us/articles/360024152594"

MEETUP_SETUP_VIDEO = "youtube.com/watch?v=CqeUIzYth_w"
MEETUP_QUICK_START_GUIDE = "https://prosupport.logi.com/hc/en-us/articles/360040084193"
MEETUP_PRODUCT_SUPPORT = "https://support.logi.com/hc/en-us/articles/360024152594"
MEETUP_ORDER_SPARE_PARTS = "https://prosupport.logi.com/hc/en-us/articles/360040084173-Spare-Part-MeetUp-ConferenceCam"
MEETUP_REFER_TO_FAQ = "https://support.logi.com/hc/en-us/articles/360024152594"
RALLY_REFER_TO_FAQ = "https://support.logi.com/hc/en-us/articles/360024325453"

RALLYCAMERA_SETUP_VIDEO = "youtube.com/watch?v=wcTCET74z2U"
RALLYCAMERA_QUICK_START_GUIDE = "https://prosupport.logi.com/hc/en-us/articles/360039589534"
RALLYCAMERA_PRODUCT_SUPPORT = "https://support.logi.com/hc/en-us/articles/360024151434"
RALLYCAMERA_ORDER_SPARE_PARTS = "https://prosupport.logi.com/hc/en-us/articles/360040083673-Spare-Part-Rally-Camera"
RALLYCAMERA_REFER_TO_FAQ = "https://support.logi.com/hc/en-us/articles/360024151434"

RALLYBAR_REFER_TO_FAQ = "https://prosupport.logi.com/hc/en-us/articles/360056237674"
RALLYBARMINI_REFER_TO_FAQ = "https://prosupport.logi.com/hc/en-us/articles/360058919854-Getting-Started-Rally-Bar-Mini"


class SyncConfig:

    @staticmethod
    def is_selected(element, timeout: int = None, selected: bool = True):
        """
        Private Method to verify whether the element status is selected

        :param element:
        :param timeout:
        :param selected:
        :return bool:
        """
        i = SYNC_TIMEOUT if timeout is None else timeout
        while i > 0:
            if selected and element.is_selected():
                return True
            elif not selected and not element.is_selected():
                return True
            i = i - 1
            time.sleep(1)
        return False

    @staticmethod
    def is_attribute_present(element, attribute: str, value: str, timeout: int = None, present: bool = True):
        """
        Private Method to verify whether the attribute value present in element attribute

        :param value:
        :param element:
        :param attribute:
        :param timeout:
        :param present:
        :return bool:
        """
        i = SYNC_TIMEOUT if timeout is None else timeout
        value_list = value.split(",")
        while i > 0:
            for val in value_list:
                if present and str(element.get_attribute(attribute)).__contains__(val):
                    return True
                elif not present and not str(element.get_attribute(attribute)).__contains__(val):
                    return True
            i = i - 1
            time.sleep(1)
        return False