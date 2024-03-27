
import subprocess
from pathlib import Path

THIS_FOLDER = Path(__file__).parent

AHK_DLL = THIS_FOLDER / "observers/AutoHotkey.dll"
HID_DLL = THIS_FOLDER / "hid_listener/hidapi.dll"

APP_PATH = THIS_FOLDER / "st_companion.py"

command = (
    "pyinstaller --noconfirm --onefile --console "
    f"--add-data \"{AHK_DLL};.\" "
    f"--add-data \"{HID_DLL};.\" "
    f"{APP_PATH}"
)

subprocess.run(command, shell=True)
