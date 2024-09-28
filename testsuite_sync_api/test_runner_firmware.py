import unittest
from base import global_variables
from testsuite_sync_api.firmware_kong_sync_api import LogiSyncFirmwareAPIKong
from testsuite_sync_api.firmware_kong_error_messages import LogiSyncFirmwareErrorsAPIKong

tests_LogiSyncFirmwareAPIKong = unittest.TestLoader().loadTestsFromTestCase(LogiSyncFirmwareAPIKong)
tests_LogiSyncFirmwareErrorsAPIKong = unittest.TestLoader().loadTestsFromTestCase(LogiSyncFirmwareErrorsAPIKong)

suite_LogiSyncFirmwareAPIKong = unittest.TestSuite(tests_LogiSyncFirmwareAPIKong)
suite_LogiSyncFirmwareErrorsAPIKong = unittest.TestSuite(tests_LogiSyncFirmwareErrorsAPIKong)

global_variables.teardownFlag = False
unittest.TextTestRunner().run(suite_LogiSyncFirmwareAPIKong)
global_variables.teardownFlag = True #This should be just before the last suite
unittest.TextTestRunner().run(suite_LogiSyncFirmwareErrorsAPIKong)

