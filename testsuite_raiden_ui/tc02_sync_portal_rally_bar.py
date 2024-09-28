import unittest

from apps.raiden.raiden_config.raiden_config import RaidenConfig
from apps.raiden.sync_portal_tests import SyncPortalTests
from base import global_variables
from base.base_ui import UIBase
from apis.raiden_api import raiden_helper


class SyncPortalRallyBar(UIBase):
    raiden_tests = SyncPortalTests()
    UIBase.logi_tune_flag = True
    device_name = "Rally Bar"

    @classmethod
    def setUpClass(cls, start_winappdriver=True) -> None:
        super(SyncPortalRallyBar, cls).setUpClass()
        ip_address = RaidenConfig.get_ip_address(device_name=cls.device_name)
        raiden_helper.override_collabos_raiden_parameters(device_name=cls.device_name,
                                                          device_ip=ip_address,
                                                          env=global_variables.SYNC_ENV)

    def test_2001_VC_148703_provision_rally_bar_disconnect_reconnect(self):
        self.raiden_tests.tc_provision_device_disconnect_reconnect(device_name=self.device_name)



if __name__ == "__main__":
    unittest.main()
