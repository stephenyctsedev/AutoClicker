import pyautogui
import time
import random

for z in range(100):
    pyautogui.press('num6')

    localtime = time.localtime()
    result = time.strftime("%I:%M:%S %p", localtime)
    print(str(z) + ', ' + str(result))
