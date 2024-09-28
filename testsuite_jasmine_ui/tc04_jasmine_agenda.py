from base.jasmine_base import JasmineBase
import unittest


class JasmineAgenda(JasmineBase):
    def test_4001_VC_135290_get_first_agenda_item_details(self):
        self.jasmine_tc_methods.tc_get_first_agenda_item_details()


if __name__ == "__main__":
    unittest.main()
