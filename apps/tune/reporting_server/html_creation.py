import os
import time
from datetime import datetime

from config import SERVER_LOGS_DIR


def update_html_file_with_recent_server_logs():
    # Path where logs are stored
    log_directory = os.path.join(SERVER_LOGS_DIR, 'report_server_logs')

    # Get list of all .log files in logs directory
    log_files = [f for f in os.listdir(log_directory) if
                 os.path.isfile(os.path.join(log_directory, f)) and f.endswith(".txt")]

    # Sort files based on last modification time
    log_files.sort(key=lambda f: os.path.getmtime(os.path.join(log_directory, f)), reverse=True)

    # Starting tags for the HTML document
    # Note the inclusion of the Bootstrap CSS CDN for styling
    html_string = """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
        <title>Log Files</title>
    </head>
    <body class="bg-dark text-white">
        <div class="container">
            <h1 class="my-3">List of Log Files:</h1>
            <table class="table table-dark">
                <thead>
                    <tr>
                        <th scope="col">Modification time</th>
                        <th scope="col">File name</th>
                        <th scope="col">Size (MB)</th>
                    </tr>
                </thead>
                <tbody>
    """

    # Create a row for each log file (with a link to the log file) and add it to the HTML string
    for log_file in log_files:
        modification_time = datetime.fromtimestamp(
            os.path.getmtime(os.path.join(log_directory, log_file)))
        formatted_time = modification_time.strftime('%Y-%m-%d %H:%M:%S')

        # Calculate file size in megabytes
        file_size = os.path.getsize(os.path.join(log_directory, log_file)) / (1024 * 1024)

        html_string += f'                <tr><td>{formatted_time}</td><td><a href="{log_file}" target="_blank" class="text-white">{log_file}</a></td><td>{file_size:.2f} MB</td></tr>\n'

    # Closing tags for the HTML document
    html_string += """
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """

    # Write the HTML string to a file
    with open(os.path.join(log_directory, "logs.html"), "w") as html_file:
        html_file.write(html_string)

    print("HTML file has been generated!")


if __name__ == '__main__':
    while True:
        update_html_file_with_recent_server_logs()
        time.sleep(600)
