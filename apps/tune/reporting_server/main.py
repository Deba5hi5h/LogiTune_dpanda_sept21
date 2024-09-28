from datetime import datetime
import logging
import os
from typing import Optional

import aiofiles
import asyncio
from uvicorn import Config, Server
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from config import REPORTS_DIR, HOST_IP, PORT, SERVER_LOGS_DIR

if not os.path.exists(os.path.join(SERVER_LOGS_DIR, 'report_server_logs')):
    os.makedirs(os.path.join(SERVER_LOGS_DIR, 'report_server_logs'))

# Form the log file name
log_file_name = os.path.join(SERVER_LOGS_DIR, 'report_server_logs', f"{datetime.now().strftime('%Y%m%d%H%M%S')}_uvicorn.txt")

# Remove default handlers from uvicorn loggers
for logger_name in ["uvicorn.error", "uvicorn.access", "uvicorn"]:
    logger = logging.getLogger(logger_name)
    logger.handlers.clear()

# Configure log level
logger.setLevel(logging.INFO)

# Create file handler which logs INFO messages
fh = logging.FileHandler(log_file_name)
fh.setLevel(logging.INFO)

# Create stream handler for console output
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)

# Create a formatter and add it to the handler
formatter = logging.Formatter('[%(asctime)s][%(name)14s][%(levelname)s] - %(message)s')
fh.setFormatter(formatter)
sh.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(fh)
logger.addHandler(sh)

app = FastAPI()


class Directory(BaseModel):
    name: str


@app.get("/")
async def main():
    return RedirectResponse('/docs/')


@app.post("/create_dir/{main_folder}")
async def create_directory(main_folder: str, directory: Directory):
    directory_to_make = os.path.join(REPORTS_DIR, main_folder, directory.name)
    try:
        os.makedirs(directory_to_make)
        return {"status": "OK", "directory": os.path.join(main_folder, directory.name)}
    except FileExistsError:
        return {"status": "NOK", "error": f"directory '{directory.name}' already exists"}


@app.put("/upload_file/{main_folder}/{directory}")
async def create_upload_files(main_folder: str, directory: Optional[str] = None, file: Optional[UploadFile] = None):
    directory = directory if directory is not None else ''
    to_save = os.path.join(REPORTS_DIR, main_folder, directory, file.filename)
    timeout_duration = 30

    try:
        content = await asyncio.wait_for(file.read(), timeout=timeout_duration)
    except asyncio.TimeoutError:
        await file.close()
        raise HTTPException(status_code=408, detail="Request timeout: File upload took too long.")

    async with aiofiles.open(to_save, 'wb') as out_file:
        await out_file.write(content)
    await file.close()

    return {"status": "OK", "filename": os.path.join(main_folder, directory, file.filename)}


if __name__ == '__main__':
    server_config = Config(app="main:app", host=HOST_IP, port=PORT, log_config=None)
    server = Server(config=server_config)
    server.logger = logger
    server.run()
