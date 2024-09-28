from apps.collabos.collabos_base import AppiumServiceCollabOS, CollabOsOpenApp
from apps.collabos.nintendo.pages.room_booking_main_page import (
    RoomBookingMainPage,
    RoomBookingDevicePinPage,
    LogitechSettingsPage,
    FloorMapPage
)
from base.global_variables import APPIUM_PORT_NINTENDO
from apps.collabos.nintendo.nintendo_connect import NintendoConnect
from common.decorators import Singleton
from common.framework_params import (
    NINTENDO_DEVICE_SN,
    NINTENDO_DESK_IP
)


@Singleton
class NintendoMethods(NintendoConnect):
    def __init__(self):
        self.appium_service = AppiumServiceCollabOS(
            appium_port=APPIUM_PORT_NINTENDO,
            device_ip=NINTENDO_DESK_IP,
            device_sn=NINTENDO_DEVICE_SN
        )

    home = RoomBookingMainPage()
    pin = RoomBookingDevicePinPage()
    logi_settings = LogitechSettingsPage()
    floor_map = FloorMapPage()

    def open_app(self, force=False):
        room_booking_app = CollabOsOpenApp(
            appium_service=self.appium_service,
            connect_process=lambda: self.connect_to_room_booking_app(
                port=APPIUM_PORT_NINTENDO,
                device_ip=NINTENDO_DESK_IP,
                device_sn=NINTENDO_DEVICE_SN
            ),
            force=force
        )

        room_booking_app.connect_to_android_app()

    def get_time_from_main_page(self):
        return self.home.get_time()
