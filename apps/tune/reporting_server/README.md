# FastAPI Server

This is a FastAPI server, which provides functionality for creating directories, and uploading files to these directories.

Main purpose of this is creating reports' folders and uploading files for valid test report presentation.

Server also provides UI API documentation, which might help testing the server - in the browser submit `HOST_IP:PORT` and hit enter. 

(For now the valid URL is: http://swqa-dashboard:8000/)

Logs from server will be available under: `HOST_IP/assets/report_server_logs/logs.html` - but firstly you need to run the `html_creation.py` script. 

(For now the valid URL is: http://swqa-dashboard/assets/report_server_logs/logs.html)

## How it Works
The server has various HTTP methods for different functions:

- **GET "/":** This endpoint redirects you to the documentation page of the API.
- **POST "/create_dir/":** This endpoint creates a new directory. It requires a JSON body with a "name" field representing the name of the directory.
- **PUT "/upload_file/{directory}":** This endpoint uploads a file to the specified directory. The directory should already exist. The endpoint requires the file in a payload of the request.

The server also includes a detailed logging mechanism.

## Setup
Firstly, create virtual environment, then install packages from `server_requirements.txt`.
Next, setup `config.py` file with following information:
- REPORTS_DIR - path (can be relative and absolute) to the main reports folder
- HOST_IP - local IP address (or Domain if applicable) of the computer on which server and reports are set
- PORT - port on which API server will be available (default is 8000)
- SERVER_LOGS_DIR - relative or absolute path from server folder, where log files will be saved

## Running the Server
The FastAPI server can be simply run with the command:

`path/to/venv/python main.py`

To run updating logs:

`path/to/venv/python html_creation.py`

The best approach is to run the server on the startup of the computer, so it'll be available all the time the computer is up.
