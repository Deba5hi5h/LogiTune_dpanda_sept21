from extentreport.report import Report


def get_payload_to_disable_rightsight(system_image_version: float) -> dict:
    """
    Get payload to disable rigsight when system image version is provided.

    :param system_image_version: System image version of device
    """
    try:
        if system_image_version < float(912.97):
            data = {'rightSight': {'on': 0}}

        elif system_image_version < float(914.303):
            data = {'rightSight': {'on': 0, 'version': 2}}

        elif system_image_version < float(915.192):
            data = {"rightSight": {"on": 0, "groupFramingSpeed": 1, "speakerFramingSpeed": 1,
                                   "speakerDetectionSpeed": 1, "version": 4}}
        elif system_image_version < float(916.622):
            data = {"rightSight": {"on": 0, "groupFramingSpeed": 1, "speakerFramingSpeed": 1,
                                   "speakerDetectionSpeed": 1, "version": 5}}
        elif system_image_version < float(919.93):
            data = {"rightSight": {"on": 0, "groupFramingSpeed": 1, "speakerFramingSpeed": 1,
                                   "speakerDetectionSpeed": 1, "version": 6}}
        else:
            data = {"rightSight": {"on": 0, "trackingMode": 0, "mode": 0, "pip": False, "groupFramingSpeed": 1,
                                   "speakerFramingSpeed": 1, "speakerDetectionSpeed": 1, "cameraZone":
                                   {"on": 0, "left": -1, "right": -1, "depth": -1}, "version": 7}}
        return data

    except Exception as e:
        Report.logException(f'{e}')
        raise e


def get_payload_to_set_group_view_on_call_start(system_image_version: float) -> dict:
    """
    Get payload to set group view and on call start.

    :param system_image_version: System image version of device
    """
    try:
        if system_image_version < float(912.97):
           data = {'rightSight': {'on': 1, 'mode': 1}}

        elif system_image_version < float(914.303):
            data = {'rightSight': {'on': 1, 'mode': 1, 'trackingMode': 0, 'version': 2}}

        elif system_image_version < float(915.192):
            data = {"rightSight": {"on": 1, "trackingMode": 0, "mode": 1, "groupFramingSpeed": 1,
                                   "speakerFramingSpeed": 1, "speakerDetectionSpeed": 1, "version": 4}}

        elif system_image_version < float(916.622):
            data = {"rightSight": {"on": 1, "trackingMode": 0, "mode": 1, "groupFramingSpeed": 1,
                                   "speakerFramingSpeed": 1, "speakerDetectionSpeed": 1, "version": 5}}

        elif system_image_version < float(919.93):
            data = {"rightSight": {"on": 1, "trackingMode": 0, "mode": 1, "groupFramingSpeed": 1,
                                  "speakerFramingSpeed": 1, "speakerDetectionSpeed": 1, "version": 6}}

        else:
            data = {"rightSight": {"on": 1, "trackingMode": 0, "mode": 1, "pip": False, "groupFramingSpeed": 1,
                                   "speakerFramingSpeed": 1, "speakerDetectionSpeed": 1, "cameraZone":
                                   {"on": 0, "left": -1, "right": -1, "depth": -1}, "version": 7}}
        return data

    except Exception as e:
        Report.logException(f'{e}')
        raise e


def get_payload_to_set_speaker_view_framing_speed_to_slower_speaker_detection_to_default(system_image_version: float) -> dict:
    """
    Get payload to set speaker view framing speed to slower and speaker detection to default.

    :param system_image_version: System image version of device
    """
    try:
        if system_image_version < float(915.192):
            data = {"rightSight": {"on": 1, "trackingMode": 1, "pip": True, "speakerDetectionSpeed": 1,
                                   "groupFramingSpeed": 0, "speakerFramingSpeed": 0, "version": 4}}

        elif system_image_version < float(916.622):
            data = {"rightSight": {"on": 1, "trackingMode": 1, "pip": True, "speakerDetectionSpeed": 1,
                                   "groupFramingSpeed": 0, "speakerFramingSpeed": 0, "version": 5}}

        elif system_image_version < float(919.93):
            data = {"rightSight": {"on": 1, "trackingMode": 1, "pip": True, "speakerDetectionSpeed": 1,
                                   "groupFramingSpeed": 0, "speakerFramingSpeed": 0, "version": 6}}

        else:
            data = {"rightSight": {"on": 1, "trackingMode": 1, "mode": 0, "pip": True,
                                   "groupFramingSpeed": 1, "speakerFramingSpeed": 0,
                                   "speakerDetectionSpeed": 1,
                                   "cameraZone": {"right": -1, "depth": -1, "left": -1, "on": 0},
                                   "version": 7}}
        return data

    except Exception as e:
        Report.logException(f'{e}')
        raise e


def get_payload_to_set_group_view_and_framing_speed_to_default(system_image_version: float) -> dict:
    """
    Get payload to set group view and framing speed to default.

    :param system_image_version: System image version of device
    """
    try:
        if system_image_version < float(915.192):
            data = {"rightSight": {"on": 1, "trackingMode": 0, "mode": 0, "speakerDetectionSpeed": 1,
                                   "groupFramingSpeed": 1, "speakerFramingSpeed": 1, "version": 4}}

        elif system_image_version < float(916.622):
            data = {"rightSight": {"on": 1, "trackingMode": 0, "mode": 0, "speakerDetectionSpeed": 1,
                                   "groupFramingSpeed": 1, "speakerFramingSpeed": 1, "version": 5}}

        elif system_image_version < float(919.93):
            data = {"rightSight": {"on": 1, "trackingMode": 0, "mode": 0, "speakerDetectionSpeed": 1,
                                   "groupFramingSpeed": 1, "speakerFramingSpeed": 1, "version": 6}}

        else:
            data = {"rightSight": {"on": 1, "trackingMode": 0, "mode": 0, "pip": False, "groupFramingSpeed": 1,
                                   "speakerFramingSpeed": 1, "speakerDetectionSpeed": 1,
                                   "cameraZone": {"right": -1, "depth": -1, "left": -1, "on": 0}, "version": 7}}
        return data

    except Exception as e:
        Report.logException(f'{e}')
        raise e

