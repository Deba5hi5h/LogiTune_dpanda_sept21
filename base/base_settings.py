import os

#Settings for Framework. Do not change
IMPLICIT_WAIT = 30
EXPLICIT_WAIT = 20
BROWSER = "chrome"
GOOGLE = 'google'
MICROSOFT = 'microsoft'
TEST_USER_AUTH = 'sa-vc-jenkins:jirateamonly'
DASHBOARD_FOLDER = "\\\\swqa-dashboard\\"
PORTAL_TIMEOUT = 15
SYNC_APP_PATH_WIN = "C:\\Program Files (x86)\\Logitech\\LogiSync\\frontend\\Sync.exe"
SYNC_APP_PATH_MAC = '/Applications/Sync.app/Contents/MacOS/Sync'
SYNC_MIDDLEWARE_WIN = "C:\\ProgramData\\Logitech\\LogiSync\\LogiSyncMiddleware.log"
SYNC_MIDDLEWARE_MAC = '/Users/Shared/LogiSync/LogiSyncMiddleware.log'
SYNC_UTIL_PATH_WIN = "C:\\Program Files (x86)\\Logitech\\LogiSync\\sync-agent\\LogiSyncUtil.exe"
TUNES_APP_PATH_WIN = "C:\\Program Files (x86)\\Logitech\\LogiTune\\LogiTune.exe"
TUNES_APP_PATH_WIN_NEW = "C:\\Program Files\\Logitech\\LogiTune\\LogiTune.exe"
TUNES_APP_PATH_MAC = "/Applications/LogiTune.app/Contents/MacOS/LogiTune"
TUNES_APP_PATH_MAC_NEW = "/Applications/Logi Tune.app/Contents/MacOS/LogiTune"
TUNEAPP_NAME = "Logi Tune"
LOGITUNES_PROD_EP = r'https://updates.vc.logitech.com/api/files/manifest/tune/latest'
# LOGITUNES_PROD_EP = r'https://updates-staging.vc.logitech.com/api/files/manifest/tune/latest'
LOGITUNE_HEADER = {"Accept": "*/*", 'x-api-key': 'x9tcGmNGROyEPeK8'}
TUNEAPP_PATH = {
        'source': {
            'windows': 'vc-sw-release/vc-apps-tune',
            'mac': 'vc-sw-release/vc-apps-tune'
        },
        'destination': {
            'windows': os.path.join(str(os.getenv('LCITEST')),
                                    'binaries/Tuneapp/Win/'),
            'mac': os.path.join(str(os.getenv('LCITEST')),
                                'binaries/Tuneapp/Mac/')
        }
    }
TUNE_SETTINGS_PATH_WIN = r"C:\ProgramData\Logitech\Tune\settings.json"
TUNE_SETTINGS_PATH_MAC = r"/Users/Shared/logitune/settings.json"