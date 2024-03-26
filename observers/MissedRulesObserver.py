
import re
import ctypes

from pathlib import Path
from sequence_transform_companion.site_packages import mss

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
        screens = mss.mss().monitors[1:]

        values = sorted([screen["left"] for screen in screens])
        x = self.get_mouse_pos()[0]

        range_start = self.find_range(values, x)
        width, height = [
            (screen["width"], screen["height"])
            for screen in screens if screen["left"] == range_start
        ][0]

        return width // 2 - 75, height // 2

    @staticmethod
    def get_mouse_pos() -> tuple[int, int]:
        class POINT(ctypes.Structure):
            _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

        point = POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
        return point.x, point.y

    @staticmethod
    def find_range(values, x) -> int:
        for i in range(len(values) - 1):
            if values[i] <= x <= values[i + 1]:
                return values[i]

        if x >= values[-1]:
            return values[-1]
