import os

# REPORTS_DIR - relative or absolute path from server folder, where reports will be uploaded
REPORTS_DIR = os.path.join('D:', os.sep)

# HOST_IP - IP address of the host computer (will be used by clients to connect to server)
HOST_IP = 'http://swqa-dashboard/'

# PORT - Port number, on which server will be available for the client
PORT = 8000

# SERVER_LOGS_DIR - relative or absolute path from server folder, where log files will be saved
SERVER_LOGS_DIR = os.path.join('..', 'wwwroot', 'wwwroot', 'assets')
