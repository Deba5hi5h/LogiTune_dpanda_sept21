import logging
import os
import subprocess
import time

from ppadb.client import Client
from time import sleep

from apis.sync_api.device_firmware_utils.download_component import DownloadImages

log = logging.getLogger(__name__)
directory = os.path.dirname(__file__)


class AndroidBase:

    def __init__(self, platform, ip):
        self.platform = platform
        self.ip = ip
        self.device = self.__get_device_by_ip(ip)

    def __get_device_by_sn(self, serial=None, retries=60, timeout=1):
        client = Client()
        max_tries = retries
        tries = 0
        while tries < max_tries:
            tries += 1
            try:
                if serial == None:
                    device = client.devices()[0]
                else:
                    device = client.device(serial)
                device.wait_boot_complete()
                return device
            except AttributeError:
                pass
            except TimeoutError:
                pass
            except RuntimeError:
                pass
            except IndexError:
                pass

            sleep(timeout)

        if serial == None:
            raise Exception("No device connected.... sorry")
        else:
            raise Exception("No device with sn: " + serial + " connected.... sorry")

    def __get_device_by_ip(self, ip):
        client = Client()
        try:
            client.remote_connect(ip, 5555)
            device = client.device(f"{ip}:5555")
            return device
        except AttributeError:
            pass
        except TimeoutError:
            pass
        except RuntimeError:
            pass
        except IndexError:
            pass

        raise Exception(f"Cannot connect to IP: {ip}")

    def is_device_available(self, serial):
        client = Client()
        if client.device(serial):
            return True
        return False

    def is_device_available_by_ip(self):
        client = Client()
        if client.remote_connect(self.ip, 5555):
            return True
        return False

    def device_reboot(self):
        self.device.reboot()

    def install_android_image(self, target_ver):
        current_version = self.get_current_version("Android")
        log.debug(f"Current Android version is: {current_version}")

        if target_ver != current_version:
            log.debug(f"Target Android version should be: {target_ver}")

            log.debug(f"Reboot device to bootloader mode.")
            self.device.shell("reboot bootloader")
            time.sleep(5)

            download_helper = DownloadImages()
            is_device_locked = self.__check_if_device_locked()
            if is_device_locked == None:
                assert False, "Not possible to determine if device is locked or not!"
            log.debug(f"Device locked: {is_device_locked}")
            if download_helper.download_and_unzip_android_image(target_ver, True, is_signed=is_device_locked):

                log.debug(f"Install image in android device.")
                if self.platform == 'windows':
                    if is_device_locked:
                        dir_path = f"{directory}\\files\\SSB_0UWW_{target_ver}\\out\\out_img\\KAD\\results\\Image\\V{target_ver}\\0UWW\\"
                    else:
                        dir_path = f"{directory}\\files\\0UWW_{target_ver}\\out\\out_img\\KAD\\results\\Image\\V{target_ver}\\0UWW\\"

                    res = subprocess.check_output(
                        f"cd {dir_path} && fastboot_script.bat",
                        stdin=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True)
                    return "Rebooting " in res.decode('utf-8'), True

                elif self.platform == 'macos':
                    if is_device_locked:
                        dir_path = f"{directory}/files/SSB_0UWW_{target_ver}/out/out_img/KAD/results/Image/V{target_ver}/0UWW/"
                    else:
                        dir_path = f"{directory}/files/0UWW_{target_ver}/out/out_img/KAD/results/Image/V{target_ver}/0UWW/"
                    res = subprocess.check_output(
                        f"cd {dir_path} && chmod +x fastboot_script.sh && ./fastboot_script.sh",
                        stderr=subprocess.STDOUT, shell=True)
                    return "Rebooting" in res.decode('utf-8'), True
                else:
                    log.error('Platform Not Supported')

            return False, False
        return True, False

    def __check_if_device_locked(self):
        res = subprocess.check_output("fastboot oem device-info", stdin=subprocess.DEVNULL,
                                      stderr=subprocess.STDOUT, shell=True)
        if 'Device unlocked: true' in res.decode('utf-8'):
            return False
        elif 'Device unlocked: false' in res.decode('utf-8'):
            return True
        else:
            return None

    def get_current_version(self, component_name):
        if component_name == "Android" or component_name == "Audio":
            res = self.device.shell(f"fwk update getSubsystemCurrentVersion {component_name}")
        else:
            res = self.device.shell(f"fwk update getSubsystemCurrentVersion STM_{component_name}")
        res = res.split(" ")[-1].rstrip()
        return res

    def update_component_with_file(self, comp_name, comp_version):
        current_version = self.get_current_version(comp_name)
        log.debug(f"Current {comp_name} is: {current_version}")
        if comp_version != current_version:
            log.debug(f"Target {comp_name} should be: {comp_version}")
            d_comp = DownloadImages()

            if d_comp.download_component_by_version(comp_name, comp_version):
                abspath = os.path.abspath(__file__)
                dname = os.path.dirname(os.path.dirname(abspath))
                dir_path = f"{dname}/device_firmware_utils/files/"

                if comp_name == "Audio":
                    file_name = f"{comp_name}_{comp_version}.itb"
                    self.device.push(dir_path + file_name, f'/sdcard/Download/{file_name}')
                    log.debug(f"Installing {comp_name}...")
                    res = self.device.shell(f"fwk update updateWithFile {comp_name} /sdcard/Download/{file_name}")
                    log.debug(res)
                    # time needed to install Audio component
                    time.sleep(500)
                    cur_comp = self.get_current_version(comp_name)
                    log.debug(f"{comp_name} with {cur_comp} installed.")
                else:
                    file_name = f"{comp_name}_{comp_version}.bin"
                    self.device.push(dir_path + file_name, f'/sdcard/Download/{file_name}')
                    res = self.device.shell(f"fwk update updateWithFile STM_{comp_name} /sdcard/Download/{file_name}")
                    log.debug(f"response from installation of {comp_name}: {res}")
                    # time needed to install Audio component
                    time.sleep(15)
                    cur_comp = self.get_current_version(comp_name)
                return cur_comp == comp_version, True
            return False, False
        return True, False
