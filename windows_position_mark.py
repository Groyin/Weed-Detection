import pyautogui
import time

def get_coordinates():
    print("请移动鼠标到窗口的左上角，然后按回车...")
    input()
    x1, y1 = pyautogui.position()
    print(f"左上角坐标: ({x1}, {y1})")

    print("请移动鼠标到窗口的右下角，然后按回车...")
    input()
    x2, y2 = pyautogui.position()
    print(f"右下角坐标: ({x2}, {y2})")

    return x1, y1, x2, y2

if __name__ == "__main__":
    x1, y1, x2, y2 = get_coordinates()
    print(f"窗口位置确定为: 左上角 ({x1}, {y1}), 右下角 ({x2}, {y2})  code: {x1}, {y1}, {x2}, {y2}")
