import paramiko

from extentreport.report import Report

ip = "172.28.78.218"
user="vsqa"
pwd="sqa1"


class RemoteReboot:
    @staticmethod
    def reboot_device(device_names) -> bool:
        """
        Method to reboot devices
        :param: device_names: device or list of devices separated by comma
        :return: True if reboot successful else False
        """
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, username=user, password=pwd)
            command = f"python C:\\Automation\\vc-qa-test\\vc-cloud-apps-automation-e2e\\common\\reboot_devices.py -d \"{device_names}\""
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
            error = ssh_stderr.read()
            print(error)
            if len(error) != 0:
                Report.logFail(str(error))
                return False
            output = ssh_stdout.read()
            print(output)
            if 'Device cannot be restarted' in str(output)\
                    or 'Failed to restart' in str(output)\
                    or 'Error connecting to WiFi' in str(output):
                Report.logFail(str(output))
                return False
            else:
                return True
        except Exception as e:
            Report.logException(str(e))
            return False