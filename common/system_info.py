import subprocess

from common.platform_helper import get_custom_platform
from extentreport.report import Report


class SystemInfo():

    @staticmethod
    def get_system_info():
        """
        Method to get Computer Tyoe, OS, OS Version, Memory on Windows system
        :param none
        :return computer_type, operating_system, os_version, memory
        """

        operating_system=''
        os_version = ''
        memory = ''
        system_model = ''
        system_manufatcurer = ''
        computer_type = ''
        try:
            if get_custom_platform() == "windows":
                sys_output = subprocess.check_output(['systeminfo']).decode('utf-8').split('\n')
                sys_info = []
                for item in sys_output:
                    sys_info.append(str(item.split("\r")[:-1]))

                for item in sys_info:
                    if 'OS NAME' in item.upper():
                        operating_system = item[2:-2].split(":")[1].strip()
                    if 'OS VERSION' in item.upper():
                        tag = item[2:-2].split(":")[0].strip()
                        if tag.upper() == 'OS VERSION':
                            os_version = item[2:-2].split(":")[1].strip()
                    if 'SYSTEM MANUFACTURER' in item.upper():
                        system_manufatcurer = item[2:-2].split(":")[1].strip()
                    if 'SYSTEM MODEL' in item.upper():
                        system_model = item[2:-2].split(":")[1].strip()
                    if 'TOTAL PHYSICAL MEMORY' in item.upper():
                        memory = item[2:-2].split(":")[1].strip()

                os_version = os_version.split(" ")[0]
                model = system_model.split(" ")[0]
                computer_type = f"{system_manufatcurer} {model}"
                memory = int(memory.replace(",", "").split(" ")[0])/1024
                memory = str(round(memory, 0))
            else:
                sys_output = subprocess.check_output(
                    ['system_profiler', 'SPSoftwareDataType', 'SPHardwareDataType']).decode('ascii').split('\n')
                for item in sys_output:
                    if 'SYSTEM VERSION' in item.upper():
                        os = item.split(':')[1].strip()
                        operating_system = os.split(' ')[0].strip()
                        os_version = os.split(' ')[1].strip()
                    if 'MODEL NAME' in item.upper():
                        computer_type = item.split(':')[1].strip()
                    if 'MEMORY' in item.upper():
                        memory = item.split(':')[1].strip()
        except Exception as e:
            Report.logException(str(e))
        return computer_type, operating_system, os_version, memory

