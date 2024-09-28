from base.jasmine_base import JasmineBase
import unittest


class JasmineFloorMap(JasmineBase):
    def test_5001_VC_135292_view_floor_map_containing_the_meeting_room(self):
        self.jasmine_tc_methods.tc_view_floor_map_containing_the_meeting_room()


if __name__ == "__main__":
    unittest.main()
