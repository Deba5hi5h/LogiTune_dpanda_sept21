import pyautogui
import sys

x = sys.argv[1]
y = sys.argv[2]

pyautogui.moveTo(int(x), int(y))
