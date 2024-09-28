import os
# All Global Variables are defined here
# Extent Report required variables
reportInstance = None
reportPath = None
extentReport = None
extent = None
setupFlag = True  # This is required when executing multiple test files
teardownFlag = True  # This is required when executing multiple test files

# Section for Dashboard variables
testStatus = "Pass"
passed = 0
failed = 0
skipped = 0
test_category = 'Functional'
retry_test = True
retry_count = 0
update_test_automation_field = False
dashboard_unmount = True

# Section for Email
email_flag = False
email_details = "<br>"
email_failed = False
email_to = "sveerbhadrappa@logitech.com,bchandrashekar@logitech.com,dkattegummula@logitech.com,plesniak@logitech.com,sboruthalupula@logitech.com,rdrozd@logitech.com"
# Number of ports in USB Switch
USB_SWITCH = 8

# App UI Specific
config = None  # AWS Configuration
jira = None  # Jira Instance
cycleName = None  # Jira Cycle Name
driver = None
collabos_driver = None

# Firmware api
firmware_api_device_name = None
firmware_api_device_conn = None
firmware_project = None
firmware_version = None

# Sync environment variables
SYNC_ROLE = 'OrgViewer'  # 'OrgViewer', 'OrgAdmin','SysAdmin', 'Readonly', 'ThirdParty'
SYNC_ENV = 'raiden-latest1'  # raiden-prod, raiden-qa, raiden-stable, kong, latest, staging, stable, qadev
# raiden-latest, raiden-staging, raiden-latest1, 'raiden-qa1','raiden-prodeu', 'raiden-prodfr', 'raiden-prodca'

# Sync App update channel
SYNC_FUTEN = 'futen-staging-qa' # 'futen-stable', 'futen-staging', 'futen-staging-qa', 'futen-staging-dev'
# Sync device firmware update channel
SYNC_FWOTA = 'futen-staging'  # futen-prod-qa, futen-prod-qa2, futen-staging, futen-prod
SYNC_ROOM = {'raiden-prod': 'Logi Kong QA', 'raiden-qa': 'VC-AUTOINFRA', 'raiden-stable': 'QA-TestOrg',
             'raiden-latest': 'VC-AUTOINFRA', 'raiden-staging': 'VC-AUTOINFRA', 'raiden-latest1': 'VC-AUTOINFRA',
             'raiden-qa1': 'VC-AUTOINFRA', 'raiden-stable1': 'VC-AUTOINFRA', 'raiden-prodeu': 'Logi QA EU',
             'raiden-prodfr': 'Logi QA FR', 'raiden-prodca': 'Logi QA CA', 'raiden-prod-aladdin': 'Logitech Aladdin_QA',
             'raiden-prod-logitech':'Logitech IT'}
SYNC_ROOM_READONLY = {'raiden-prod': 'QATestOrg', 'raiden-qa': 'EmailAlerts-Test', 'raiden-stable': 'Logi QA Stable',
                      'raiden-latest': 'QA-TestOrg', 'raiden-staging': 'QA-TestOrg', 'raiden-latest1': 'QA-TestOrg',
                      'raiden-qa1': 'QA-TestOrg', 'raiden-stable1': 'QA-Org', 'raiden-prodeu': 'QA-TestOrg',
                      'raiden-prodfr': 'Logi QA FR Mult','raiden-prodca': 'Logi QA CA- Multitenancy'}

# Proxy related variables
ENABLE_PROXY = False  # By default Proxy will be disabled. Set this to True from runner file for Proxy tests
PROXY_PAC = None
PAC_SINGLE_SERVER = "http://swqa-automation-mac.logitech.com/proxy.pac"
PAC_MULTIPLE_SERVER = "http://swqa-automation-mac.logitech.com/multipleproxy.pac"
PROXY_SERVERS = "172.28.79.86,172.28.79.148,172.28.78.218,172.28.78.167,172.25.11.83,172.27.14.10"
PROXY_EXCEPTIONS = ['ssm.us-west-2.amazonaws.com', 'chromedriver.storage.googleapis.com',
                    'qa-auto-repo.s3.us-west-2.amazonaws.com', 'qa-auto-repo.s3.us-east-1.amazonaws.com',
                    'jira.logitech.com', 'smtp.gmail.com']

# Device related parameters to pass across test suites
BRIGHTNESS = None
CONTRAST = None
SATURATION = None
SHARPNESS = None

# Tune environment variables
TUNE_UPDATE_CHANNEL = "qa"
TUNE_UPDATE_MANIFEST_URL_OLD = "https://updates-staging.vc.logitech.com/api/files/manifest/tune/latest"
TUNE_UPDATE_MANIFEST_URL = "https://updates-staging.vc.logitech.com/api/apps/manifest/latest"
TUNE_FW_UPDATE_MANIFEST_URL = "https://updates-staging.vc.logitech.com/api/firmware/manifest/latest"

#Tune Mobile variables
PLATFORM_NAME = None #Update this in Tune Mobile Base
PLATFORM_VERSION = None #Update this in Tune Mobile Base
HEADSET = None #Update this in Test Script

# Hsinchu variable
ZEPHYR_EXECUTION_PATH = None # Update this in Test Script for jira zephyr integration

ROOT_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

TUNE_DEBUG_PORT = 9222
APPIUM_PORT_COILY = 4725
APPIUM_PORT_NINTENDO = 4723

#Image processing
tesseract_cmd = r'/opt/homebrew/Cellar/tesseract/5.3.2_1/bin/tesseract' #Path where tesseract installed

# LogiSyncPersonalCollab tests purpose
tune_available_devices = []
