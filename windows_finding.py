import win32gui


def enum_windows_callback(hwnd, results):
    # 获取窗口标题
    window_text = win32gui.GetWindowText(hwnd)
    # 获取窗口类名
    class_name = win32gui.GetClassName(hwnd)
    results.append((hwnd, window_text, class_name))


def list_open_windows():
    results = []
    # 枚举所有顶级窗口
    win32gui.EnumWindows(enum_windows_callback, results)

    # 输出所有窗口的信息
    for hwnd, window_text, class_name in results:
        print(f"窗口句柄: {hwnd}, 窗口标题: {window_text}, 类名: {class_name}")


if __name__ == "__main__":
    list_open_windows()
