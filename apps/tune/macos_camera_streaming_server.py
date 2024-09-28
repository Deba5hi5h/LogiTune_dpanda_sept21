import json
import socket
import subprocess

from contextlib import closing
from apps.tune.camera_streaming import CameraStreaming


class ServerMacCameraStreaming(CameraStreaming):
    """

    This class represents a server for streaming video from Mac cameras. It extends the `CameraStreaming` class.

    Attributes:
    - `host`: A string representing the host address of the server. Default value is 'localhost'.
    - `port`: An integer representing the port number on which the server will listen. Default value is 8973.
    - `_cameras`: A dictionary that maps unique camera names to their corresponding index in the available cameras list.
    - `_run_server`: A boolean flag indicating whether the server is running or stopped.

    Methods:
    - `__init__(self, host='localhost', port=8973)`: Initializes a new instance of the `ServerMacCameraStreaming` class.
      Sets the initial values for `host`, `port`, `_cameras`, and `_run_server`.

    - `start_server()`: Starts the server and listens for commands. Once a client is connected, it receives a command
      from the client and performs the requested action. The server supports the following commands:
      - `start_stream`: Starts streaming video from a specified camera. Responds to the client with a success status
        and the name of the camera.
      - `stop_stream`: Stops the video stream. Responds to the client with a success status.
      - `is_streaming`: Checks if the server is currently streaming video. Responds to the client with a boolean status
        indicating whether the server is streaming.

    - `_get_all_available_cameras() -> list`: Obtains a list of all available cameras on the Mac system.
      Returns a list of camera names in ascending order. The method uses the `system_profiler` command to get camera
      information in JSON format. It then processes the JSON data to extract the camera names and their
      corresponding indices, which are stored in the `_cameras` dictionary.

    """

    def __init__(self, host: str = 'localhost', port: int = 8973):
        super().__init__()
        self._host = host
        self._port = port
        self._cameras = dict()
        self._run_server = True

    def start_server(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self._host, self._port))
            s.listen()
            print('Server is listening for commands...')
            while self._run_server:
                with closing(s.accept()[0]) as client:
                    print(f'Connected with {str(client.getpeername())}')
                    msg_data = json.loads(client.recv(1024).decode('utf-8'))
                    command = msg_data.get('command')
                    if command == 'start_stream':
                        camera_name = msg_data.get('camera_name')
                        self.start_stream(camera_name)
                        response = {'start_stream': True, 'camera_name': camera_name}
                        client.send(json.dumps(response).encode('utf-8'))
                    elif command == 'stop_stream':
                        self.stop_stream()
                        response = {'stop_stream': True}
                        client.send(json.dumps(response).encode('utf-8'))
                        self._run_server = False
                    elif command == 'is_streaming':
                        response = {'is_streaming': self.is_streaming()}
                        client.send(json.dumps(response).encode('utf-8'))
            s.close()
        print('Server is stopped.')

    def _get_all_available_cameras(self) -> list:
        proc = subprocess.run(
            ["system_profiler", "SPCameraDataType", "-json"], capture_output=True, text=True,
            check=True
        )

        cameras = json.loads(proc.stdout)["SPCameraDataType"]
        cameras.sort(key=lambda item: item["spcamera_unique-id"])
        available_cameras = [cam.get('_name') for cam in cameras]
        self._cameras = {key: idx for idx, key in enumerate(available_cameras)}
        return available_cameras


if __name__ == '__main__':
    ServerMacCameraStreaming().start_server()
