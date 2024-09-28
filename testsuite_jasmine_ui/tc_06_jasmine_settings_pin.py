from base.jasmine_base import JasmineBase
import unittest


class JasmineSettingsPin(JasmineBase):
    def test_6001_VC_135290_configure_settings_pin(self):
        self.jasmine_tc_methods.tc_configure_settings_pin()


if __name__ == "__main__":
    unittest.main()
