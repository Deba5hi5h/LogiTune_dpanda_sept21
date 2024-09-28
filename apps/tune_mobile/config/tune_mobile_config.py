import time

SYNC_TIMEOUT = 90
implicit_wait = 20
new_command_timeout = 3000
base_driver = None
app_package = "com.logitech.logue"
app_activity = "com.logitech.logue.ui.activity.SplashActivity"
coily_app_package = "com.logitech.vc.scheduler"
coily_app_activity = "com.logitech.coily.ui.main.MainActivity"
coily_platform_version = "10"
coily_platform_name = "Android"
lanngauge = "English"
headset = "Zone Wireless Plus"
locale = "EN"
phone = "S22"
android_automationName = "UiAutomator2"
teammate_phone = "iPhone15"
building = 'Logi-SJ'
port = 4723
device = {
    "iPhone12": {"platform_name": "iOS",
                 "platform_version": "16.7.2",
                 "udid": "00008101-000C351A11A3003A",
                 "model": "",
                 "passcode": "123456"},
    "iPhone13": {"platform_name": "iOS",
                 "platform_version": "15.6.1",
                 "udid": "00008110-000475690C81401E",
                 "model": "",
                 "passcode": "123456"},
    "iPhone14": {"platform_name": "iOS",
                 "platform_version": "17.5",
                 "udid": "00008110-000A45D60C9A201E",
                 "model": "",
                 "passcode": "123456"},
    "iPhone15": {"platform_name": "iOS",
                 "platform_version": "17.2.1",
                 "udid": "00008130-000605691A50001C",
                 "model": "",
                 "passcode": "123456"},
    "S22": {"platform_name": "Android",
            "platform_version": "14",
            "udid": "2C161FDH200ES4",
            "model": "Pixel7",
            "passcode": "123456"},
    "S10": {"platform_name": "Android",
            "platform_version": "12",
            "udid": "",
            "model": "SM_G973F",
            "passcode": "123456"},
    "OnePlus": {"platform_name": "Android",
                "platform_version": "13",
                "udid": "",
                "model": "LE2115",
                "passcode": "123456"},
    "Pixel2": {"platform_name": "Android",
               "platform_version": "11",
               "udid": "",
               "model": "Pixel_2",
               "passcode": "123456"},
    "Pixel6": {"platform_name": "Android",
               "platform_version": "13",
               "udid": "",
               "model": "sdk_gphone64_arm64",
               "passcode": "123456"},
    "Pixel5": {"platform_name": "Android",
               "platform_version": "11",
               "udid": "",
               "model": "sdk_gphone_arm64",
               "passcode": "123456"}
}

test_desk_info = {
    "Logi-SJ": {
        "site": "Mobile QA",
        "user_desk": "SW-QA-Desk1",
        "nearest_desk": "SW-QA-Desk2",
        "second_nearest_desk": "SW-QA-Desk3",
        "different_floor_desk1": "Collab-Eng-01",
        "different_floor_desk2": "Collab-Eng-02",
        "different_area_desk1": "Desk1",
        "different_area_desk2": "Desk2",
        "coily_desk": "Desk1",
        "user_email": "gmobile.logi.user2@gmail.com",
        "other_email": "gmobile.logi.other2@gmail.com",
        "teammate_email": "gmobile.logi.teammate2@gmail.com",
        "google_email": "gmobile.logi.user2@gmail.com",
        "microsoft_email": "swqa_mobile@outlook.com"
    },
    "Logi-Auto": {
        "site": "Mobile QA",
        "user_desk": "auto-tune-qa-desk1",
        "nearest_desk": "auto-tune-qa-desk2",
        "second_nearest_desk": "auto-tune-qa-desk3",
        "different_floor_desk1": "auto-mobile-qa-desk1",
        "different_floor_desk2": "auto-mobile-qa-desk2",
        "different_area_desk1": "auto-tune-dev-desk1",
        "different_area_desk2": "auto-tune-dev-desk2",
        "coily_desk": "auto-tune-dev-desk1",
        "user_email": "gmobile.logi.user1@gmail.com",
        "other_email": "gmobile.logi.other1@gmail.com",
        "teammate_email": "gmobile.logi.teammate1@gmail.com",
        "google_email": "gmobile.logi.user1@gmail.com",
        "microsoft_email": "msn.mobile.user1@outlook.com"
    }
}

class TuneMobileConfig():

    @staticmethod
    def building():
        return building

    @staticmethod
    def site():
        return test_desk_info.get(building).get("site")

    @staticmethod
    def user_desk():
        return test_desk_info.get(building).get("user_desk")

    @staticmethod
    def nearest_desk():
        return test_desk_info.get(building).get("nearest_desk")

    @staticmethod
    def second_nearest_desk():
        return test_desk_info.get(building).get("second_nearest_desk")

    @staticmethod
    def different_floor_desk1():
        return test_desk_info.get(building).get("different_floor_desk1")

    @staticmethod
    def different_floor_desk2():
        return test_desk_info.get(building).get("different_floor_desk2")

    @staticmethod
    def different_area_desk1():
        return test_desk_info.get(building).get("different_area_desk1")

    @staticmethod
    def different_area_desk2():
        return test_desk_info.get(building).get("different_area_desk2")

    @staticmethod
    def coily_desk():
        return test_desk_info.get(building).get("coily_desk")

    @staticmethod
    def user_email():
        return test_desk_info.get(building).get("user_email")

    @staticmethod
    def other_email():
        return test_desk_info.get(building).get("other_email")

    @staticmethod
    def teammate_email():
        return test_desk_info.get(building).get("teammate_email")

    @staticmethod
    def google_email():
        return test_desk_info.get(building).get("google_email")

    @staticmethod
    def microsoft_email():
        return test_desk_info.get(building).get("microsoft_email")