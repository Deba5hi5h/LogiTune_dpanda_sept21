import json
import os
import socket
import subprocess
import sys
import time
from abc import ABC, abstractmethod
from threading import Thread
from typing import Union
import cv2


class CameraStreaming(ABC):
    """
    CameraStreaming is an abstract base class for implementing camera streaming functionality.
    Subclasses must implement the _get_all_available_cameras method.

    Methods:
    - __init__: Constructor method that initializes the _cameras dictionary and sets _streaming_on
                to False.
    - start_stream: Starts streaming from the specified camera asynchronously.
    - _start_stream: Helper method that starts streaming from the specified camera.
    - stop_stream: Stops the streaming.
    - is_streaming: Returns whether the streaming is currently on or off.

    Attributes:
    - _cameras: A dictionary containing available cameras.
    - _streaming_on: A boolean indicating whether streaming is on or off.
    """
    def __init__(self):
        self._cameras = dict()
        self._streaming_on = False
        self._capture_released = True

    @abstractmethod
    def _get_all_available_cameras(self) -> list:
        pass

    def start_stream(self, camera_name: str) -> None:
        t = Thread(target=self._start_stream, args=(camera_name,))
        t.daemon = True
        t.start()
        self.wait_for_camera_to_start_streaming()

    def _start_stream(self, camera_name: str) -> None:
        try:
            self._get_all_available_cameras()
            capture = cv2.VideoCapture(self._cameras[camera_name])
            self._streaming_on = True
            print(f'Stream started for: {camera_name}')
            invalid_reads = 0
            while self._streaming_on:
                if self._capture_released:
                    self._capture_released = False
                valid_read, frame = capture.read()
                if not valid_read:
                    if invalid_reads > 10:
                        print('Invalid camera reads exceeded 10 times, stopping streaming')
                        break
                    print(f'Invalid camera read for "{camera_name}" '
                          f'- retrying {invalid_reads} time')
                    invalid_reads += 1
                    time.sleep(0.5)
            capture.release()
            self._capture_released = True

        except KeyError as e:
            print(f"Unable to find camera named: '{camera_name}'. "
                  f"Available cameras: {list(self._cameras.keys())}")
            raise e

    def stop_stream(self) -> None:
        self._streaming_on = False
        while not self._capture_released:
            time.sleep(0.5)

    def is_streaming(self) -> bool:
        """
            Returns whether the streaming is currently on or off.

            Returns:
                bool: True if streaming is on, False if streaming is off.

        """
        return self._streaming_on

    def wait_for_camera_to_start_streaming(self) -> None:
        while not self.is_streaming():
            time.sleep(0.5)


class WindowsCameraStreaming(CameraStreaming):
    """
    A class for streaming video from Windows cameras.

    This class extends the `CameraStreaming` class.

    Methods:
        _get_all_available_cameras: Get a list of all available cameras.

    """
    def __init__(self):
        super().__init__()

    def _get_all_available_cameras(self) -> list:
        import pygame
        from pygame.camera import list_cameras

        pygame.init()
        pygame.camera.init('_camera (MSMF)')
        available_cameras = pygame.camera.list_cameras()
        self._cameras = {key: idx for idx, key in enumerate(available_cameras)}
        pygame.quit()
        return available_cameras


class MacCameraStreaming:
    """
    This class provides methods for starting and stopping camera streaming on a Mac machine.
    Mac Camera Streaming class is workaround of Jenkins inability to start camera streaming on newest MacOS versions.
    Permissions on test machines might need to be granted, especially on newer MacOS versions.

    Attributes:
    - host (str): The host address of the streaming server. Default is 'localhost'.
    - port (int): The port number of the streaming server. Default is 8973.
    - _cameras (dict): A dictionary to store camera information.
    - _server_proc (subprocess.Popen): The subprocess object representing the running streaming server.

    Methods:
    - __init__(self, host='localhost', port=8973)
        Initializes a new instance of the MacCameraStreaming class.

    - start_stream(self, camera_name: str) -> dict
        Starts streaming from the specified camera.
        Returns a dictionary containing the response from the server.

    - stop_stream(self) -> dict
        Stops the camera streaming.
        Returns a dictionary containing the response from the server.

    - is_streaming(self) -> dict
        Checks if the camera is currently streaming.
        Returns a dictionary containing the response from the server.

    - _send_request(self, request: dict) -> dict
        Sends a request to the streaming server and receives a response.
        Returns a dictionary containing the response from the server.

    """
    def __init__(self, host: str = 'localhost', port: int = 8973):
        self._host = host
        self._port = port
        self._cameras = dict()
        self._server_proc = None

    def start_stream(self, camera_name: str) -> dict:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        osascript_command = [
            'osascript',
            '-e',
            'tell application "Terminal"',
            '-e',
            f'do script "python3 {os.path.join(base_dir, 'macos_camera_streaming_server.py')}; exit"',
            '-e',
            'end tell',
        ]
        self._server_proc = subprocess.Popen(osascript_command)
        time.sleep(2)
        response = self._send_request({'command': 'start_stream', 'camera_name': camera_name})
        print(f'Command: "start_stream" - {response}')
        return response

    def stop_stream(self) -> dict:
        osascript_command = [
            'osascript',
            '-e',
            'tell application "Terminal" to close every window'
        ]
        response = self._send_request({'command': 'stop_stream'})
        print(f'Command: "stop_stream" - {response}')
        self._server_proc.terminate()
        self._server_proc.wait()
        subprocess.Popen(osascript_command)
        return response

    def is_streaming(self) -> dict:
        response = self._send_request({'command': 'is_streaming'})
        print(f'Command: "is_streaming" - {response}')
        return response

    def _send_request(self, request: dict) -> dict:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self._host, self._port))
                s.sendall(json.dumps(request).encode('utf-8'))
                response = s.recv(1024)
                return json.loads(response.decode('utf-8'))
        except Exception as e:
            error_message = f"{repr(e)}: {e}"
            print(error_message)
            return {'error': error_message}


def initialize_camera_streaming() -> Union[WindowsCameraStreaming, MacCameraStreaming]:
    if sys.platform.startswith('win'):
        return WindowsCameraStreaming()
    else:
        return MacCameraStreaming()
