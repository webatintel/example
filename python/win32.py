import win32gui
import win32con

pattern = 'Untitled - Notepad'

def winEnumHandler(hwnd, ctx):
    title = win32gui.GetWindowText(hwnd)
    if title == pattern:
        print hex(hwnd)
        win32gui.SendMessage(hwnd, win32con.WM_CLOSE, 0, 0)

win32gui.EnumWindows(winEnumHandler, None)
