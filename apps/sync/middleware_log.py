from base import base_settings
from common.platform_helper import get_custom_platform
from extentreport.report import Report


class MiddlewareLog():

    @staticmethod
    def get_ip_address(device_name):
        # opening middleware log file
        if get_custom_platform() == 'windows':
            middlware = base_settings.SYNC_MIDDLEWARE_WIN
        else:
            middlware = base_settings.SYNC_MIDDLEWARE_MAC
        file1 = open(middlware, "r")

        # setting flag
        ip_string = ""

        if device_name == "Rally Bar":
            device = "HostedKong"
        elif device_name == "Rally Bar Mini":
            device = "HostedDiddy"
        elif device_name == "Rally Bar Huddle":
            device = "HostedTiny"
        else:
            Report.logInfo('Device Not Found')
            return ""
        # Loop through the middleware log line by line
        for line in file1:
            # check Hosted Kong/Diddy is present in line or not
            if device in line:
                for line in file1:
                    # check address is present in line or not
                    if 'address' in line:
                        ip_string = line
                        break
                # Do not break here to get the last IP address
        # closing text file
        file1.close()
        # checking condition for string found or not
        if ip_string == "":
            Report.logInfo('IP Address Not Found')
            return ""
        else:
            ip = str(ip_string).split(":")
            if len(ip) == 2:
                ip_address = ip[1].replace(',', '').replace('"', '').strip()
            else:
                ip_address = None
                for i in range(len(ip)):
                    if 'dns1' in ip[i]:
                        ip_address = ip[i].replace('\\', '').replace('"', '').replace('dns1', '').replace(',', '').strip()
                        break
            Report.logInfo(f"IP address found - {ip_address}")
            return ip_address

