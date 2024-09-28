import sys
if not sys.platform.startswith('dar'):
    from screen_recorder_sdk import screen_recorder
    from platform import processor
import os
import ctypes
import subprocess
import time
from abc import ABC, abstractmethod
from threading import Thread


class Recorder(ABC):
    def __init__(self, filepath: str, filename: str, x: int, y: int, w: int, h: int):
        self.filepath = filepath
        self.filename = filename
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def start_recording(self):
        pass

    @abstractmethod
    def stop_recording_and_save(self):
        pass


class MacRecorder(Recorder):
    def __init__(self, filepath: str, filename: str, x: int, y: int, w: int, h: int):
        super().__init__(filepath, filename, x, y, w, h)
        self.record = os.path.join(self.filepath, f'{self.filename}.mov')
        self.stop = False
        self.retry = 0

    def _start_recording(self):
        process = subprocess.Popen(["screencapture", "-R", f"{self.x},{self.y},{self.w},{self.h}", "-v", self.record],
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        while not self.stop:
            time.sleep(0.5)
        process.communicate(b'x')

    def start_recording(self):
        t = Thread(target=self._start_recording)
        t.daemon = True
        t.start()

    def stop_recording_and_save(self):
        self.stop = True

    def delete(self):
        try:
            os.remove(self.record)
        except FileNotFoundError:
            self.retry += 1
            if self.retry <= 3:
                time.sleep(5)
                self.delete()
            else:
                raise FileNotFoundError


class WindowsRecorder(Recorder):
    frame_rate = 60
    bit_rate = 8000000

    def __init__(self, filepath: str, filename: str, x: int, y: int, w: int, h: int):
        scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
        super().__init__(filepath, filename, int(x * scale_factor), int(y * scale_factor),
                         int(w * scale_factor), int(h * scale_factor))
        self.record = os.path.join(self.filepath, f'{self.filename}.mp4')
        self.hw_transforms = False if 'amd' in processor().split(" ")[0].lower() else True

    def delete(self):
        try:
            os.remove(self.record)
        except FileNotFoundError:
            print(f'File not found: {self.record}')

    def start_recording(self):
        screen_recorder.init_resources(screen_recorder.RecorderParams(desktop_num=0))
        screen_recorder.disable_log()
        screen_recorder.start_crop_video_recording(self.record, frame_rate=self.frame_rate,
                                                   bit_rate=self.bit_rate,
                                                   use_hw_transfowrms=self.hw_transforms,
                                                   srcLeft=self.x, srcTop=self.y,
                                                   srcRight=self.x+self.w, srcBottom=self.y+self.h)
        time.sleep(5)

    def stop_recording_and_save(self):
        screen_recorder.stop_video_recording()


def initialize_recorder(filepath: str, filename: str, x: int, y: int, w: int, h: int) -> Recorder:
    if sys.platform.startswith('dar'):
        return MacRecorder(filepath, filename, x, y, w, h)
    else:
        return WindowsRecorder(filepath, filename, x, y, w, h)


if __name__ == '__main__':
    logitune_dim = {'x': 2200, 'y': 740, 'w': 360, 'h': 660}
    recorder = WindowsRecorder('movie', 'test.dupajasia2', **logitune_dim)
    recorder.start_recording()
    if not input('Click enter to exit'):
        recorder.stop_recording_and_save()

