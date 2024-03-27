
import re
import ctypes

from pathlib import Path

import win32api
import win32con
import win32gui  # noqa

THIS_FOLDER = Path(__file__).parent

ahk = ctypes.cdll.LoadLibrary(str(THIS_FOLDER / "./AutoHotkey.dll"))
ahk.run = ahk.ahkExec

ahk.ahktextdll(u"")
ahk.run("RemoveToolTip:\nToolTip\nReturn\n")


class MissedRulesObserver:
    def notify(self, message: str) -> None:
        match = re.findall(r"Missed rule! (.+) -> (.+)", message)

        if not match:
            return

        sequence, transform = match[0]
        self.show_tooltip(f"Missed rule! {sequence} -> {transform}")

    def show_tooltip(self, text: str) -> None:
        x, y = self.get_tooltip_coordinates()

        ahk.run(f"ToolTip, {text}, {x}, {y}")
        ahk.run("SetTimer, RemoveToolTip, 1500")

    def get_tooltip_coordinates(self) -> tuple[int, int]:
        width, height = self.get_active_window_screen_dimensions()
        return width // 2 - 75, height // 2

    # noinspection PyUnresolvedReferences
    @staticmethod
    def get_active_window_screen_dimensions() -> tuple[int, int]:
        hwnd = win32gui.GetForegroundWindow()

        screen = win32api.MonitorFromWindow(
            hwnd, win32con.MONITOR_DEFAULTTONEAREST
        )

        monitor_info = win32api.GetMonitorInfo(screen)

        left, top, right, bottom = monitor_info['Monitor']
        screen_width = right - left
        screen_height = bottom - top

        return screen_width, screen_height
