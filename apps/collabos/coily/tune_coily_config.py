
SYNC_TIMEOUT = 90

base_driver = None
GOOGLE = 'google'
MICROSOFT = 'microsoft'
FORMAT_24H = '24'
FORMAT_AMPM = '12'


COILY_DEVICE_NAME = 'Logi Dock Flex'
NEVER_BLOCK_PERIPHERALS = True

UNKNOWN = 'Unknown'
OFFLINE = 'Offline'
IN_USE = "In Use"
IN_USE_AWAY = "In Use (away)"
AVAILABLE = "Available"


SYNC_PORTAL_STATUSES = {
    UNKNOWN: [-1],
    OFFLINE: [0, 8],
    IN_USE: [3, 6, 7, 10],
    IN_USE_AWAY: [4],
    AVAILABLE: [1, 2, 5, 9, 11]
}
