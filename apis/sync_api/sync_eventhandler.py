"""
:Module Name: **Sync Event Handler**

===============================

This module handles Validating the protobuf Events recevived from the Proxy Server and Middleware.
This Class includes a list of events handling Product, Device, Provision & Firmware Status
"""
import logging
log = logging.getLogger(__name__)

FINAL_EVENT = True
NON_FINAL_EVENT = False

class SyncEventHandler:
    """
    This Class includes a list of events handling Product, Device, Provision & Firmware Status
    """
    def __init__(self):
        self.protobuf_dict = {
            "productUpdatedEvent":
                self.product_updated_event,
            "provisioningDataAvailableEvent":
                self.provisioning_data_available_event,
            "softwareUpdateReportEvent":
                self.software_update_report_event,
            "firmwareUpdateProgressEvent":
                self.firmware_update_progress_event,
            "firmwareUpdateStartedEvent":
                self.firmware_update_started_event,
            "firmwareUpdateErrorEvent":
                self.firmware_update_error_event,
            "firmwareUpdateCompletedEvent":
                self.firmware_update_completed_event,
            "productAvailableEvent":
                self.product_available_event,
            "productUnavailableEvent":
                self.product_unavailable_event,
            "deviceConnectedToProductEvent":
                self.device_connected_to_product_event,
            "deviceDisconnectedFromProductEvent":
                self.device_disconnected_from_product_event,
            "productErrorEvent":
                self.product_error_event,
            "devicePropertyChangedEvent":
                self.device_property_changed_event,
            "productConfigurationChangedEvent":
                self.product_configuration_changed_event,
            "productStateChangedEvent":
                self.product_state_changed_event,
            "clientConnectionEvent":
                self.client_connection_event,
            "firmwareUpdateSchedulingEvent":
                self.firmware_update_scheduling_event,
            "rightSightConfigurationChangedEvent":
                self.right_sight_configuration_changed_event,
            "videoSettingsConfigurationChangedEvent":
                self.video_settings_configuration_changed_event,
            "roomInformationChangedEvent":
                self.room_information_changed_event,
            "logiSyncConfigurationChangedEvent":
                self.logisync_configuration_changed_event,
            "bleConfigurationChangedEvent":
                self.ble_configuration_changed_event
        }

    def _find_key_in_dict(self, obj, key):
        """
        Find the key in the dict recursively
        :param obj:
        :param key:
        :return:
        """
        try:
            # If Key if found directly
            if key in obj:
                return obj[key]

            # Recursively find the Value of a key
            for k, v in obj.items():
                if isinstance(v, dict):
                    item = self._find_key_in_dict(v, key)
                    if item is not None:
                        return item
        except Exception as e:
            log.error("Need to Handle Error - {}".format(e))
            raise e

    def handle_protobuf_events(self, buffer:dict, event_list:list):
        """
        Parse the protobuf Events from the Protobuf Dictionary
        :param buffer:
        :param event_list:
        :return:
        """
        try:
            for _event in event_list:
                if self._find_key_in_dict(buffer, _event):
                    log.info("Found the Event {}".format(buffer))
                    return self.protobuf_dict[_event](_event)

            # Needs to return None
            return None, NON_FINAL_EVENT

        except Exception as e:
            log.error("Need to Handle  - {}".format(e))
            raise e

    def product_updated_event(self, event):
        """

        :param event:
        :return:
        """
        log.info("Parse PB Events method got product_updated_event")
        return event, NON_FINAL_EVENT

    def provisioning_data_available_event(self, event):
        """

        :param event:
        :return:
        """
        log.info("Parse PB Events method got provisioning_data_available_event")
        return event, NON_FINAL_EVENT

    def software_update_report_event(self, event):
        """

        :param event:
        :return:
        """
        log.info("Parse PB Events method got software_update_report_event")
        return event, NON_FINAL_EVENT

    def firmware_update_progress_event(self, event):
        """

        :param event:
        :return:
        """
        log.info("Parse PB Events method got firmware_update_progress_event")
        return event, NON_FINAL_EVENT

    def firmware_update_started_event(self, event):
        """

        :param event:
        :return:
        """
        log.info("Parse PB Events method got firmware_update_started_event")
        return event, NON_FINAL_EVENT

    def firmware_update_error_event(self, event):
        """

        :param event:
        :return:
        """
        log.info("Parse PB Events method got firmware_update_error_event")
        return event, NON_FINAL_EVENT

    def firmware_update_completed_event(self, event):
        """

        :param event:
        :return:
        """
        log.info("Parse PB Events method got firmware_update_completed_event")
        return event, FINAL_EVENT

    def product_available_event(self, event):
        """

        :param event:
        :return:
        """
        log.info("Parse PB Events method got product_available_event")
        return event, FINAL_EVENT

    def product_unavailable_event(self, event):
        """

        :param event:
        :return:
        """
        log.info("Parse PB Events method got product_unavailable_event")
        return event, FINAL_EVENT

    def device_connected_to_product_event(self, event):
        """

        :param event:
        :return:
        """
        log.info("Parse PB Events method got device_connected_to_product_event")
        return event, NON_FINAL_EVENT

    def device_disconnected_from_product_event(self, event):
        """

        :param event:
        :return:
        """
        log.info("Parse PB Events method got device_disconnected_from_product_event")
        return event, NON_FINAL_EVENT

    def product_error_event(self, event):
        """

        :param event:
        :return:
        """
        log.info("Parse PB Events method got firmware_update_progress_event")
        return event, NON_FINAL_EVENT

    def device_property_changed_event(self, event):
        """

        :param event:
        :return:
        """
        log.info("Parse PB Events method got device_property_changed_event")
        return event, NON_FINAL_EVENT

    def product_configuration_changed_event(self, event):
        """

        :param event:
        :return:
        """
        log.info("Parse PB Events method got product_configuration_changed_event")
        return event, NON_FINAL_EVENT

    def product_state_changed_event(self, event):
        """

        :param event:
        :return:
        """
        log.info("Parse PB Events method got product_state_changed_event")
        return event, NON_FINAL_EVENT

    def client_connection_event(self, event):
        """

        :param event:
        :return:
        """
        log.info("Parse PB Events method got client_connection_event")
        return event, NON_FINAL_EVENT

    def firmware_update_scheduling_event(self, event):
        """

        :param event:
        :return:
        """
        log.info("Parse PB Events method got firmware_update_scheduling_event")
        return event, NON_FINAL_EVENT

    def right_sight_configuration_changed_event(self, event):
        """
        :param event:
        :return:
        """
        log.info("Parse PB Events method got right_sight_configuration_changed_event")
        return event, NON_FINAL_EVENT

    def video_settings_configuration_changed_event(self, event):
        """
        :param event:
        :return:
        """
        log.info("Parse PB Events method got video_settings_configuration_changed_event")
        return event, NON_FINAL_EVENT

    def room_information_changed_event(self, event):
        """
        :param event:
        :return:
        """
        log.info("Parse PB Events method got room_information_changed_event")
        return event, NON_FINAL_EVENT

    def logisync_configuration_changed_event(self, event):
        """
        :param event:
        :return:
        """
        log.info("Parse PB Events method got room_information_changed_event")
        return event, NON_FINAL_EVENT

    def ble_configuration_changed_event(self, event):
        """

        :param event:
        :return:
        """
        log.info("Parse PB Events method ble_configuration_changed_event")
        return event, NON_FINAL_EVENT


class EventHandler:
    """
    Common event handler class which contains generic method for handling
    event loop

    """
    @staticmethod
    def event_listener_method(ws_conn, loop, ws_dict):
        """
        Method to execute event listener for protobuf API and get event response
        This method called in a thread in TC-201 (for reference), No other event
        loop method should be called once this is running.

        """
        event_response = loop.run_until_complete(ws_conn.event_listener())
        ws_dict["event_response"] = event_response
