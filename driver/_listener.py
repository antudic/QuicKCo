import ctypes
import win32
import enum

from ctypes import wintypes
from concurrent.futures import ThreadPoolExecutor

keyTranslator = win32.KeyTranslator()

# SET UP C BINDINGS (heavily inspired by github.com/moses-palmer/pynput)


# LowLevelKeyboardProc: https://docs.microsoft.com/en-us/previous-versions/windows/desktop/legacy/ms644985(v=vs.85)
# UnhookWindowsHookEx: https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-UnhookWindowsHookEx
# SetWindowsHookEx: https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowshookexa
# KBDLLHOOKSTRUCT: https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-kbdllhookstruct
# CallNextHookEx: https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-callnexthookex


class _KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ('vkCode', wintypes.DWORD),
        ('scanCode', wintypes.DWORD),
        ('flags', wintypes.DWORD),
        ('time', wintypes.DWORD),
        ('dwExtraInfo', ctypes.c_void_p)]

cObjects = {
    "LPKBDLLHOOKSTRUCT": ctypes.POINTER(_KBDLLHOOKSTRUCT),
    "UnhookWindowsHookEx": ctypes.windll.user32.UnhookWindowsHookEx,
    "SetWindowsHookEx": ctypes.windll.user32.SetWindowsHookExW,
    "CallNextHookEx": ctypes.windll.user32.CallNextHookEx,
    "GetMessage": ctypes.windll.user32.GetMessageW,
    "idHook": ctypes.c_int(13),
    "lpmsg": ctypes.byref(wintypes.MSG())
    }

cObjects["UnhookWindowsHookEx"].argtypes = (wintypes.HHOOK,)

cObjects["HOOKPROC"] = ctypes.WINFUNCTYPE(
    wintypes.LPARAM,
    ctypes.c_int32,
    wintypes.WPARAM,
    wintypes.LPARAM
    )

cObjects["SetWindowsHookEx"].argtypes = (
    ctypes.c_int,
    cObjects["HOOKPROC"],
    wintypes.HINSTANCE,
    wintypes.DWORD
    )

cObjects["CallNextHookEx"].argtypes = (
    wintypes.HHOOK,
    ctypes.c_int,
    wintypes.WPARAM,
    wintypes.LPARAM
    )

cObjects["GetMessage"].argtypes = (
    ctypes.c_voidp,
    wintypes.HWND,
    wintypes.UINT,
    wintypes.UINT)



# CREATE HELPER FUNCTION FOR DRIVER
executor = ThreadPoolExecutor()
# ^ default max_workers argument is the number of processors on the machine multiplied by 5
# ^ https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor

hookId = None

def parser(nCode, wParam, lParam):
    data = ctypes.cast(lParam, cObjects["LPKBDLLHOOKSTRUCT"]).contents
    
    key = keyTranslator(
        data.vkCode,
        data.scanCode,
        (not data.flags >> 7)
        )
    
    eventHandler(key)

def hookFunc(nCode, wParam, lParam):
    executor.submit(parser, nCode, wParam, lParam)
    return cObjects["CallNextHookEx"](0, nCode, wParam, lParam)

def hookFuncBlocking(nCode, wParam, lParam):
    executor.submit(parser, nCode, wParam, lParam)
    return 1

def start(suppress=False):
    global hookId
    
    if suppress: lpfn = cObjects["HOOKPROC"](hookFuncBlocking)
    else:        lpfn = cObjects["HOOKPROC"](hookFunc)
    
    hookId = cObjects["SetWindowsHookEx"](cObjects["idHook"], lpfn, None, 0)

    getMsg = cObjects["GetMessage"]
    lpmsg = cObjects["lpmsg"]
    while True: getMsg(lpmsg, None, 0, 0)
    # running the above line in a thread seems to be very dangerous from to my testing

def stop():
    if hookId: cObjects["UnhookWindowsHookEx"](hookId)
