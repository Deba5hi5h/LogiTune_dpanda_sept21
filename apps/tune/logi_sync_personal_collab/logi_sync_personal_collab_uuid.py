import winreg
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class InstallInfo:
    name: Optional[str] = None
    product_id: Optional[str] = None
    version: Optional[str] = None
    uninstall: Optional[str] = None
    is_bundle: bool = False


class LogiSyncPersonalCollabWindowsInfo:

    def _get_logi_sync_personal_collab_installation_info(self) -> List[InstallInfo]:
        installed: List[InstallInfo] = []
        uninstall_keys = [
            "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
        ]
        for regkey in uninstall_keys:
            parent = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, regkey)
            try:
                index = 0
                while True:
                    subkey_name = winreg.EnumKey(parent, index)
                    index = index + 1
                    subkey = winreg.OpenKey(parent, subkey_name)
                    vindex = 0
                    found = False
                    info = InstallInfo()
                    try:
                        while True:
                            vname, vdata, _ = winreg.EnumValue(subkey, vindex)
                            vindex = vindex + 1
                            if vname == "DisplayName" and vdata.startswith("LogiSyncPersonalCollab"):
                                info.name = vdata.strip()
                                info.product_id = subkey_name
                                found = True
                            if vname == "QuietUninstallString":
                                info.uninstall = vdata.strip()
                            if vname == "DisplayVersion":
                                info.version = vdata.strip()
                            if vname == "BundleVersion":
                                info.is_bundle = True
                    except OSError:
                        pass
                    finally:
                        subkey.Close()
                    if found:
                        installed.append(info)
            except OSError:
                pass
            finally:
                parent.Close()
        return installed

    def get_product_id(self) -> Optional[str]:
        infos = self._get_logi_sync_personal_collab_installation_info()
        if len(infos) == 1:
            return infos[0].product_id
        return None

    def get_version(self) -> Optional[str]:
        infos = self._get_logi_sync_personal_collab_installation_info()
        if len(infos) == 1:
            return infos[0].version
        return None

    def is_installed(self) -> bool:
        infos = self._get_logi_sync_personal_collab_installation_info()
        return len(infos) > 0


