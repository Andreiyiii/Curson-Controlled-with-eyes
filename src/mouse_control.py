import pyautogui
pyautogui.PAUSE = 0

def move(x, y):
    pyautogui.moveTo(x, y)


def click():
    print("Click!")
    pyautogui.click()