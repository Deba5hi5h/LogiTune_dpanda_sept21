import os
import time
from pathlib import Path
import subprocess
from base import global_variables

class Proxy():
    @staticmethod
    def set_proxy_ip() -> None:
        """
        Method to set Proxy Settings using IP Address and Port.
        Adds Firewall outbound rule to allow Proxy Servers

        :param none
        :return none
        """
        Proxy.add_outbound_rule_for_proxy_servers()
        rootPath = Path(os.path.dirname(__file__)).parent
        time.sleep(1)
        process = subprocess.run(str(rootPath) + "\\WinApp\\proxy.bat set ip",shell=True)
        if Proxy._check_log_msg("ip_success"):
            print("Proxy IP and Port set successfully")
        else:
            raise Exception('Proxy Setup Failed')

    @staticmethod
    def set_proxy_pac_single_server() -> None:
        """
        Method to set Proxy Settings using PAC file (Single server).
        Adds Firewall outbound rule to allow Proxy Servers

        :param none
        :return none
        """
        Proxy.add_outbound_rule_for_proxy_servers()
        rootPath = Path(os.path.dirname(__file__)).parent
        time.sleep(1)
        process = subprocess.run(str(rootPath) + "\\WinApp\\proxy.bat set pac single", shell=True)
        if Proxy._check_log_msg("pac_success"):
            print("Proxy PAC with single server set successfully")
        else:
            raise Exception('Proxy PAC with single server setup Failed')

    @staticmethod
    def set_proxy_pac_multiple_servers() -> None:
        """
        Method to set Proxy Settings using PAC file (Multiple servers).
        Adds Firewall outbound rule to allow Proxy Servers

        :param none
        :return none
        """
        Proxy.add_outbound_rule_for_proxy_servers()
        rootPath = Path(os.path.dirname(__file__)).parent
        time.sleep(1)
        process = subprocess.run(str(rootPath) + "\\WinApp\\proxy.bat set pac multiple", shell=True)
        if Proxy._check_log_msg("pac_success"):
            print("Proxy PAC with multiple servers set successfully")
        else:
            raise Exception('Proxy PAC with multiple servers setup Failed')

    @staticmethod
    def reset_proxy() -> None:
        """
        Method to reset Proxy Settings

        :param none
        :return none
        """
        rootPath = Path(os.path.dirname(__file__)).parent
        process = subprocess.run(str(rootPath) + "\\WinApp\\proxy.bat reset",shell=True)
        if Proxy._check_log_msg("reset_success"):
            print("Proxy successfully reset")
        else:
            raise Exception('Proxy reset Failed')

    @staticmethod
    def add_outbound_rule_for_hosts() -> None:
        """
        Method to add Firewall outbound rule to allow hosts defined in global_variables.PROXY_EXCEPTIONS

        :param none
        :return none
        """
        rootPath = Path(os.path.dirname(__file__)).parent
        ip = None
        for host in global_variables.PROXY_EXCEPTIONS:
            result = subprocess.run(['ping', host, '-n', '1'], stdout=subprocess.PIPE)
            if ip is None:
                ip = (str(result).split('Reply from '))[1].split(': bytes')[0]
            else:
                ip = ip + ',' + (str(result).split('Reply from '))[1].split(': bytes')[0]
        process = subprocess.run(f'{str(rootPath)}\\WinApp\\firewall_rule.bat {ip}', shell=True)

    @staticmethod
    def add_outbound_rule_for_proxy_servers() -> None:
        """
        Method to add Firewall outbound rule to allow hosts defined in global_variables.PROXY_SERVERS

        :param none
        :return none
        """
        rootPath = Path(os.path.dirname(__file__)).parent
        time.sleep(1)
        firewall_file_path = f'{str(rootPath)}\\WinApp\\firewall_rule.bat'
        ip_addresses = f'Allow_Proxy_Servers,{global_variables.PROXY_SERVERS}'
        process = subprocess.run(f'{firewall_file_path} {ip_addresses}', shell=True)

    @staticmethod
    def _check_log_msg(msg) -> bool:
        """
        Method to add Firewall outbound rule to allow hosts defined in global_variables.PROXY_SERVERS

        :param none
        :return none
        """
        time.sleep(5)
        rootPath = Path(os.path.dirname(__file__)).parent
        file1 = open(str(rootPath) + "\\WinApp\\tmp_read.txt", "r")
        flag = False
        for line in file1:
            # check ip_success is present in line or not
            if msg in line:
                flag = True
                break
        file1.close()
        return flag